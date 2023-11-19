# Format Strings

This CTF consists in two very similar challenges. In each of them, we had to exploit a program with a format-string vulnerability in order to read an array which contained the flag, appropriately named "flag".

Each challenge came with a folder which contained a few files. The most relevant were the following:

* **main.c** - the source code of the vulnerable program
* **program** - the executable corresponding to the vulnerable program

## 1st flag

### Analysis

#### Source Code

Before attempting to exploit the program, we had to properly understand its source code. To that end, we inspected "main.c".

The script can be summarized as follows:

1. Create a global character array, "flag", with size 40.

```c
#define FLAG_BUFFER_SIZE 40

char flag[FLAG_BUFFER_SIZE];
```

2. Open the file "flag.txt" and, if it exists, store its content in the "flag" array.

```c
FILE *fd = fopen("flag.txt","r");

if(fd != NULL) {
    fgets(flag, FLAG_BUFFER_SIZE, fd);
}
```

3. Create a character array named "buffer" with size 32.

```c
char buffer[32];
```

4. Read at most 32 bytes of user input and store them in "buffer".

```c
scanf("%32s", &buffer);
```

5. Call `printf()` with "buffer" as an argument.

```c
printf(buffer);
```

There was also the following if-statement at the end of "main.c":

```c
if(0) {
    printf("I like what you got!\n%s\n", flag);
} else {
    printf("\nDisqualified!\n");
}
```

If the condition were to succeed, it would print the "flag" array, thus revealing the flag. However, since 0 always evaluates to **false**, that cannot happen. So, we had to find another way to get "flag" to be printed.

#### Executable

When performing a PWN attack, not only is it important to understand the source code of the program but it is also crucial to ascertain how its executable was set up. That is, we should be aware of any security measures that could prevent us from exploiting it.

To that end, we ran `checksec`, which is a bash script for checking the properties of executables, as such:

```bash
$ checksec program
```

The output of the command above was the following:

![Alt text](images/7-1.png)

As such, we acquired the following information:

* There is a **canary** protecting the stack, which means buffer overflows will be detected.

> A **stack canary** is a secret value placed on the **stack** which changes every time the program is started. Prior to a function return, it is checked and, if it appears to have been modified, the program returns immediately.

* The executable is not a `PIE`, which means the positions of the executable are NOT **randomized**.

> A **Position-independent executable** (or `PIE` for short) is a binary that executes properly regardless of its **absolute address** (i.e. independently of where it is placed in memory).

So, taking into account our analysis of the source code and the executable, we realized that we could make the program print the "flag" array by inputing a format string that:
* Started the **address** of "flag".
* Had a certain amount of `%x` format specifiers.
* End with a `%s` format specifier.

The logic behind this payload was simple: considering the call to `printf()` was unsanitized, we could exploit that by making the program successively print the values stored in memory using `%x` specifiers. Eventually, it would reach the memory region where our input was stored. Then, the final specifier, `%s`, would make the program treat our input as an **address** and print the content it points to.

### Preparing the Payload

Now that we were aware of what to do, we had to first figure out the amount of `%x` specifiers we would need to reach our input. We decided to do so by inputting a string followed by 100 `%x` specifiers.

Since the guide provided a script for crafting the payload - "exploit_example.py" - we opted to use it like so:

```python
from pwn import *

p = remote("ctf-fsi.fe.up.pt", 4004)
payload = bytearray.fromhex("A" * 8) + b"%x" * 100

p.recvuntil(b"got:")
p.sendline(payload)
p.interactive()
```

Upon running the script, we obtained the following output:

![Alt text](images/7-2.png)

Much to our dismay, the first value that was printed from memory was our input. That meant that we would not need any `%x` specifiers after all. 

While at first we were quite surprised by this, after giving it some more thought, it made sense: it had to do with the layout of the **stack**. 

> The **stack frame** of a function is laid out as follows, in ascending order of memory addresses: <u>local variables</u>, <u>frame pointer</u>, <u>return address</u> and <u>function parameters</u>.

In fact, the stack frame of the `printf()` function would be located below the stack frame of the `main()` function. Since local variables are stored in the lower addresses, the value above `printf()` was none other than the only local variable `main()` declared - "buffer", the array used to store our input.
