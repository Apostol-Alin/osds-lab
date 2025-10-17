# Lab 2 ex 1 q 2

## Exercise 1 - Buffer Overflow to bypass authentication

For the first exercise (`ex1.c`), we will be using the scenario you imagined at the previous question. The stack contains a variable that maintains the admin status of the current user. A user is made admin only if they know a secret password.
Don't forget to use `make ex1` to build the exercise.

**[Q2]**: Can you bypass the check that "grants you access", without knowing the secret password?

Yes, I can:

```bash
./bin/ex1
AAAAAAAAA # This is entered as an input
Access granted!
```