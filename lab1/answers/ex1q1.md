# Lab 1 Ex 1 Question 1

**[Q1]**: Where is each section mapped? You can try using the `search` command in `pwndbg` (or `search-pattern` in `GEF`) to search for contents such as the string `Where is this located?` found in the source file `ex1.c`. That will help you determine where each section is. Experiment with more types by changing the source code and recompiling.

Additionally, try searching for other ways of matching memory segments with sections.

## Answer

Based on the result of the code snippet below I can say that `.data` section is located between 0x404000 and 0x405000.
Because the only executable section is the `.text` section, I can say that it is located between 0x401000 and 0x402000.

```bash
pwndbg> search "Where is this located?"
Searching for value: 'Where is this located?'
ex1             0x404030 'Where is this located?'
```
We are left with `.bss` and `.rodata` section. To find out about the whereabouts of them I am going to make some changes to the source code:

```c
#include <stdio.h>

char useful[] = "Where is this located?";

int global_int;

void bar(int n, char *p) {
	for (int i = 0; i < n; i++) {
		puts(useful);
	}
}

int main() {
	const char * const_string = "CEVA";
	while (1) {}
}
```

Then we have this output from searching the string "CEVA" in pwndbg:

```bash
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
             Start                End Perm     Size Offset File
          0x400000           0x401000 r--p     1000      0 /home/aapostol/workspace/osds/lab1/bin/ex1
          0x401000           0x402000 r-xp     1000   1000 /home/aapostol/workspace/osds/lab1/bin/ex1
          0x402000           0x403000 r--p     1000   2000 /home/aapostol/workspace/osds/lab1/bin/ex1
          0x403000           0x404000 r--p     1000   2000 /home/aapostol/workspace/osds/lab1/bin/ex1
          0x404000           0x405000 rw-p     1000   3000 /home/aapostol/workspace/osds/lab1/bin/ex1
    0x7f9d38200000     0x7f9d38228000 r--p    28000      0 /usr/lib64/libc.so.6
    0x7f9d38228000     0x7f9d3839d000 r-xp   175000  28000 /usr/lib64/libc.so.6
    0x7f9d3839d000     0x7f9d383f5000 r--p    58000 19d000 /usr/lib64/libc.so.6
    0x7f9d383f5000     0x7f9d383f9000 r--p     4000 1f5000 /usr/lib64/libc.so.6
    0x7f9d383f9000     0x7f9d383fb000 rw-p     2000 1f9000 /usr/lib64/libc.so.6
    0x7f9d383fb000     0x7f9d38408000 rw-p     d000      0 [anon_7f9d383fb]
    0x7f9d38414000     0x7f9d38418000 rw-p     4000      0 [anon_7f9d38414]
    0x7f9d3841d000     0x7f9d3841f000 r--p     2000      0 /usr/lib64/ld-linux-x86-64.so.2
    0x7f9d3841f000     0x7f9d38446000 r-xp    27000   2000 /usr/lib64/ld-linux-x86-64.so.2
    0x7f9d38446000     0x7f9d38451000 r--p     b000  29000 /usr/lib64/ld-linux-x86-64.so.2
    0x7f9d38451000     0x7f9d38453000 r--p     2000  34000 /usr/lib64/ld-linux-x86-64.so.2
    0x7f9d38453000     0x7f9d38455000 rw-p     2000  36000 /usr/lib64/ld-linux-x86-64.so.2
    0x7ffea0f8b000     0x7ffea0fad000 rw-p    22000      0 [stack]
    0x7ffea0fb9000     0x7ffea0fbd000 r--p     4000      0 [vvar]
    0x7ffea0fbd000     0x7ffea0fbf000 r-xp     2000      0 [vdso]
0xffffffffff600000 0xffffffffff601000 --xp     1000      0 [vsyscall]
pwndbg> search "CEVA"
Searching for value: 'CEVA'
ex1             0x402010 0x41564543 /* 'CEVA' */
ex1             0x403010 0x41564543 /* 'CEVA' */
```
So, the `.rodata` section is between 0x402000 and 0x404000. I can presume that the `.bss` section is located where the `data` section is located.
