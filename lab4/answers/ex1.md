How to get offset between `puts` and `/bin/sh` from libc:

```bash
pwndbg> info address puts
Symbol "puts" is at 0x7ffff7c783d0 in a file compiled without debugging.
pwndbg> search "/bin/sh" libc
Searching for value: '/bin/sh'
libc.so.6       0x7ffff7db7171 0x68732f6e69622f /* '/bin/sh' */
pwndbg> p  0x7ffff7db7171 - 0x7ffff7c783d0
$3 = 1306017 # THIS IS AN INTEGER
```

How to get offset between `puts` and `system` from libc:

```bash
pwndbg> info address puts
Symbol "puts" is at 0x7ffff7c783d0 in a file compiled without debugging.
pwndbg> info address system
Symbol "system" is at 0x7ffff7c4b980 in a file compiled without debugging.
pwndbg> p 0x7ffff7c783d0 - 0x7ffff7c4b980
$1 = 182864 # THIS IS AN INTEGER
```

0x7ffff7e05379
0x7ffff7c783d0

1626025