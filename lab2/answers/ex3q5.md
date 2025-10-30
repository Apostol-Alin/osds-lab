# Lab 2 ex 3 q 5

**[Q5]**: How many bytes are between the beginning of our vulnerable buffer and the return address?

## Answer

8 bytes from long + 4 (+4) from int + 32 bytes = 48 + 8 bytes from old_rbp = 56 bytes 