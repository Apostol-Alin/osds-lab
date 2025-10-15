# Lab 1 Ex 2 Question 3

**[Q3]**: Check `gdb` with your binary. How does `vmmap` look after running `mmap`? You can step through each line of code with `next` or `n`. You can step through each assembly instruction with `next instruction` or `ni`.

To see each line of assembly being executed by `foo()`, you can step into the function pointer call with `step instruction`, or `si`.

## Answer

Before running mmap:

```bash
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
             Start                End Perm     Size Offset File
          0x400000           0x401000 r--p     1000      0 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x401000           0x402000 r-xp     1000   1000 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x402000           0x403000 r--p     1000   2000 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x403000           0x404000 r--p     1000   2000 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x404000           0x405000 rw-p     1000   3000 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x405000           0x426000 rw-p    21000      0 [heap]
    0x7ffff7c00000     0x7ffff7c28000 r--p    28000      0 /usr/lib64/libc.so.6
    0x7ffff7c28000     0x7ffff7d9d000 r-xp   175000  28000 /usr/lib64/libc.so.6
    0x7ffff7d9d000     0x7ffff7df5000 r--p    58000 19d000 /usr/lib64/libc.so.6
    0x7ffff7df5000     0x7ffff7df9000 r--p     4000 1f5000 /usr/lib64/libc.so.6
    0x7ffff7df9000     0x7ffff7dfb000 rw-p     2000 1f9000 /usr/lib64/libc.so.6
    0x7ffff7dfb000     0x7ffff7e08000 rw-p     d000      0 [anon_7ffff7dfb]
    0x7ffff7fb7000     0x7ffff7fbc000 rw-p     5000      0 [anon_7ffff7fb7]
    0x7ffff7fc1000     0x7ffff7fc5000 r--p     4000      0 [vvar]
    0x7ffff7fc5000     0x7ffff7fc7000 r-xp     2000      0 [vdso]
    0x7ffff7fc7000     0x7ffff7fc9000 r--p     2000      0 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffff7fc9000     0x7ffff7ff0000 r-xp    27000   2000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffff7ff0000     0x7ffff7ffb000 r--p     b000  29000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffff7ffb000     0x7ffff7ffd000 r--p     2000  34000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffff7ffd000     0x7ffff7fff000 rw-p     2000  36000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffffffdd000     0x7ffffffff000 rw-p    22000      0 [stack]
0xffffffffff600000 0xffffffffff601000 --xp     1000      0 [vsyscall]
```

After running mmap, the output of vmmap is this:

```bash
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
             Start                End Perm     Size Offset File
          0x400000           0x401000 r--p     1000      0 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x401000           0x402000 r-xp     1000   1000 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x402000           0x403000 r--p     1000   2000 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x403000           0x404000 r--p     1000   2000 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x404000           0x405000 rw-p     1000   3000 /home/aapostol/workspace/osds/lab1/bin/ex2
          0x405000           0x426000 rw-p    21000      0 [heap]
    0x7ffff7c00000     0x7ffff7c28000 r--p    28000      0 /usr/lib64/libc.so.6
    0x7ffff7c28000     0x7ffff7d9d000 r-xp   175000  28000 /usr/lib64/libc.so.6
    0x7ffff7d9d000     0x7ffff7df5000 r--p    58000 19d000 /usr/lib64/libc.so.6
    0x7ffff7df5000     0x7ffff7df9000 r--p     4000 1f5000 /usr/lib64/libc.so.6
    0x7ffff7df9000     0x7ffff7dfb000 rw-p     2000 1f9000 /usr/lib64/libc.so.6
    0x7ffff7dfb000     0x7ffff7e08000 rw-p     d000      0 [anon_7ffff7dfb]
    0x7ffff7fb7000     0x7ffff7fbc000 rw-p     5000      0 [anon_7ffff7fb7]
    0x7ffff7fc0000     0x7ffff7fc1000 rwxp     1000      0 [anon_7ffff7fc0]
    0x7ffff7fc1000     0x7ffff7fc5000 r--p     4000      0 [vvar]
    0x7ffff7fc5000     0x7ffff7fc7000 r-xp     2000      0 [vdso]
    0x7ffff7fc7000     0x7ffff7fc9000 r--p     2000      0 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffff7fc9000     0x7ffff7ff0000 r-xp    27000   2000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffff7ff0000     0x7ffff7ffb000 r--p     b000  29000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffff7ffb000     0x7ffff7ffd000 r--p     2000  34000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffff7ffd000     0x7ffff7fff000 rw-p     2000  36000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffffffdd000     0x7ffffffff000 rw-p    22000      0 [stack]
0xffffffffff600000 0xffffffffff601000 --xp     1000      0 [vsyscall]
```