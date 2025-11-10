# Lab 2 Ex 1 Question 1

### What is a buffer overflow?

Simply put, a buffer overflow is when you try to copy more data into a memory location (buffer) than that memory is supposed to hold. For example, if you try to input MORE than 8 characters into a buffer of 8 characters, the copy operations to that buffer *might* continue copying past the end of it. What *past the end* means is that the extra bytes will be copied *up* the stack. The following image presents an example of a buffer overflow that overwrites adjacent value `is_admin` on the stack:

**[Q1]**: Can you imagine a scenario where this would affect a program's behavior?


### Answer

If, for example, the `is_admin` is checked to be something different that 0 to give priviledges to the user. We can enter an input longer that 8 bytes in such a way that we can make the buffer responsible to hold the value of the `is_admin` variable something different than 0.