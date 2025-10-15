# Lab 1 Ex 1 Question 2

**[Q2]**: Try finding the address of `bar()` in gdb and printing its disassembly.

What about the other files in `vmmap`? You are for sure familiar with the concepts of *libraries*. Most of the other segments are mapped libraries, but there are also some other special memory segments, like the `stack` or the `heap`, which are not actually filled up with useful values all the time. The other segments are all mapped from files, while these special segments have their memory reserved for *dynamic use*. All these segments are actually allocated using the [mmap](https://www.man7.org/linux/man-pages/man2/mmap.2.html) syscall. We'll talk about the `stack` and the `heap` later. First, let's have some fun with `mmap`.

## Answer

Since `bar()` is a function, it is translated into bytecode so it's address should be between 0x401000 and 0x402000.
Using gdb we can query where it is exactly:

```bash
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
             Start                End Perm     Size Offset File
          0x400000           0x401000 r--p     1000      0 /home/aapostol/workspace/osds/lab1/bin/ex1
          0x401000           0x402000 r-xp     1000   1000 /home/aapostol/workspace/osds/lab1/bin/ex1
          0x402000           0x403000 r--p     1000   2000 /home/aapostol/workspace/osds/lab1/bin/ex1
          0x403000           0x404000 r--p     1000   2000 /home/aapostol/workspace/osds/lab1/bin/ex1
          0x404000           0x405000 rw-p     1000   3000 /home/aapostol/workspace/osds/lab1/bin/ex1
    0x7f0e42400000     0x7f0e42428000 r--p    28000      0 /usr/lib64/libc.so.6
    0x7f0e42428000     0x7f0e4259d000 r-xp   175000  28000 /usr/lib64/libc.so.6
    0x7f0e4259d000     0x7f0e425f5000 r--p    58000 19d000 /usr/lib64/libc.so.6
    0x7f0e425f5000     0x7f0e425f9000 r--p     4000 1f5000 /usr/lib64/libc.so.6
    0x7f0e425f9000     0x7f0e425fb000 rw-p     2000 1f9000 /usr/lib64/libc.so.6
    0x7f0e425fb000     0x7f0e42608000 rw-p     d000      0 [anon_7f0e425fb]
    0x7f0e4260c000     0x7f0e42610000 rw-p     4000      0 [anon_7f0e4260c]
    0x7f0e42615000     0x7f0e42617000 r--p     2000      0 /usr/lib64/ld-linux-x86-64.so.2
    0x7f0e42617000     0x7f0e4263e000 r-xp    27000   2000 /usr/lib64/ld-linux-x86-64.so.2
    0x7f0e4263e000     0x7f0e42649000 r--p     b000  29000 /usr/lib64/ld-linux-x86-64.so.2
    0x7f0e42649000     0x7f0e4264b000 r--p     2000  34000 /usr/lib64/ld-linux-x86-64.so.2
    0x7f0e4264b000     0x7f0e4264d000 rw-p     2000  36000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffc6caf6000     0x7ffc6cb18000 rw-p    22000      0 [stack]
    0x7ffc6cb61000     0x7ffc6cb65000 r--p     4000      0 [vvar]
    0x7ffc6cb65000     0x7ffc6cb67000 r-xp     2000      0 [vdso]
0xffffffffff600000 0xffffffffff601000 --xp     1000      0 [vsyscall]
pwndbg> info address bar
Symbol "bar" is a function at address 0x401126.
```

Other examples:

```bash
pwndbg> info address puts
Symbol "puts" is at 0x7f0e424783d0 in a file compiled without debugging.
pwndbg> info address useful
Symbol "useful" is static storage at address 0x404030.
```

Since `puts` is a function defined in the *stdio.h* library, it should be located between 0x7f0e42428000 and 0x7f0e4259d000 and it is :).