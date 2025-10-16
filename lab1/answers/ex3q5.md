# Lab 1 Ex 3 Question 5

Now that we know about the calling convention, let's play with it. With a debugger, you can choose to change whatever registers you want, whenever you want. Using ONLY the `set` command in `gdb`, try calling a function that isn't called in `ex3.c`, with arguments chosen by you. Make it obvious that you chose the arguments.

**[Q5]**: Did you get a `SIGSEGV` in `printf()`? What causes it? `pwndbg` hints at the reason.

## Answer

```bash
pwndbg> n
ALIN
23              puts("Oh, ads incoming. Hope you have uBlock on...");
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]───────────────────────────────────────────────────
*RAX  1
 RBX  0
*RCX  0
*RDX  0
*RDI  0x7fffffffcfb0 ◂— 0
*RSI  0xa
*R8   0x73
 R9   0x77
*R10  0
*R11  0x7ffff7d9f3c0 (_nl_C_LC_CTYPE_class+256) ◂— 0x2000200020002
 R12  0x7fffffffd708 —▸ 0x7fffffffda9c ◂— '/home/aapostol/workspace/osds/lab1/bin/ex3'
 R13  0x4011d9 (main) ◂— push rbp
 R14  0x403e08 (__do_global_dtors_aux_fini_array_entry) —▸ 0x401120 (__do_global_dtors_aux) ◂— endbr64 
 R15  0x7ffff7ffd000 (_rtld_local) —▸ 0x7ffff7ffe210 ◂— 0
 RBP  0x7fffffffd5f0 ◂— 1
 RSP  0x7fffffffd4f0 ◂— 0x4e494c41 /* 'ALIN' */
*RIP  0x401207 (main+46) ◂— mov edi, 0x402108
────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────────────────────────
   0x4011ee <main+21>    lea    rax, [rbp - 0x100]        RAX => 0x7fffffffd4f0 ◂— 0
   0x4011f5 <main+28>    mov    rsi, rax                  RSI => 0x7fffffffd4f0 ◂— 0
   0x4011f8 <main+31>    mov    edi, __dso_handle+243     EDI => 0x4020fb (__dso_handle+243) ◂— 0x7335353225 /* '%255s' */
   0x4011fd <main+36>    mov    eax, 0                    EAX => 0
   0x401202 <main+41>    call   __isoc99_scanf@plt          <__isoc99_scanf@plt>
 
 ► 0x401207 <main+46>    mov    edi, __dso_handle+256     EDI => 0x402108 (__dso_handle+256) ◂— 'Oh, ads incoming. Hope you have uBlock on...'
   0x40120c <main+51>    call   puts@plt                    <puts@plt>
 
   0x401211 <main+56>    call   rand@plt                    <rand@plt>
 
   0x401216 <main+61>    mov    ecx, eax
   0x401218 <main+63>    movsxd rax, ecx
   0x40121b <main+66>    imul   rax, rax, 0x66666667
─────────────────────────────────────────────────────────────────────[ SOURCE (CODE) ]──────────────────────────────────────────────────────────────────────
In file: /home/aapostol/workspace/osds/lab1/ex3.c:23
   18 
   19 int main() {
   20         char name[256];
   21         puts("What's your name?");
   22         scanf("%255s", name);
 ► 23         puts("Oh, ads incoming. Hope you have uBlock on...");
   24         advertisment(rand() % 10, name);
   25         return 0;
   26 }
─────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffd4f0 ◂— 0x4e494c41 /* 'ALIN' */
01:0008│-0f8 0x7fffffffd4f8 ◂— 0
02:0010│-0f0 0x7fffffffd500 ◂— 0x3e9
03:0018│-0e8 0x7fffffffd508 ◂— 0x2001004
04:0020│-0e0 0x7fffffffd510 —▸ 0x7fffffffd5f0 ◂— 1
05:0028│-0d8 0x7fffffffd518 —▸ 0x7ffff7fc7000 ◂— 0x3010102464c457f
06:0030│-0d0 0x7fffffffd520 ◂— 0x25 /* '%' */
07:0038│-0c8 0x7fffffffd528 ◂— 0x25 /* '%' */
───────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► 0         0x401207 main+46
   1   0x7ffff7c295d0 __libc_start_call_main+128
   2   0x7ffff7c29680 __libc_start_main_impl+128
   3         0x401095 _start+37
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> set $rdi = name
pwndbg> p $rdi
$1 = 140737488344304
pwndbg> set $rsp = $rsp - 8
pwndbg> set *(int*)$rsp = 0x401250
pwndbg> set $rip = print_msg
pwndbg> continue
Continuing.
-==[ ALIN ]==-
[Inferior 1 (process 8072) exited normally]
pwndbg> 
```