# Lab 1 Ex 3 Question 4

**[Q4]**: Can you identify the arguments of a function call in the disassembly?

Now that we know about the calling convention, let's play with it. With a debugger, you can choose to change whatever registers you want, whenever you want. Using ONLY the `set` command in `gdb`, try calling a function that isn't called in `ex3.c`, with arguments chosen by you. Make it obvious that you chose the arguments.

## Answer

As sugested we can use `objdump` to see that the arguments of the function are stored into the `rax` and `edx` registres:

```bash
  401246:       48 89 c6                mov    %rax,%rsi
  401249:       89 d7                   mov    %edx,%edi
  40124b:       e8 2b ff ff ff          callq  40117b <advertisment> (File Offset: 0x117b)
```