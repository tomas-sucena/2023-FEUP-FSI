# Format Strings

> Add definition

## Setup

Before starting the tasks themselves, we had to deactivate a couple of security mechanisms Unix uses to prevent memory exploitation.

### Address Space Layout Randomization

> Address Space Layout Randomization (or `ASLR` for short) is a security measure that consists in randomly arranging the positions of a process's key address spaces, such as the base of the executable and the positions of the **stack**, **heap** and libraries.

Since this mechanism difficults guessing exact addresses, which is vital to perform format string attacks, we disabled it with the following command:

```bash
$ sudo sysctl -w kernel.randomize_va_space=0
```

### Non-executable Stack

> `Non-executable stack` is one of many executable-space protection mechanisms which marks the **stack** as non-executable, meaning all writable addresses stored on it cannot be executed.

Since one of our tasks was to exploit the format-string vulnerability to inject code into the program's stack and execute it, we deactivated it during compilation using the `-z execstack` flag.

Our compilation command was the following:

```bash
$ gcc -DBUF_SIZE=100 -z execstack -o format format.c
```

## Task 0: Understanding the Program

The vulnerable program we had to exploit in this lab was called "format.c". Its behaviour can be summarized like so:

1. Reads at most 1500 characters of user input and stores them in a character array called "buf".

```c
char buf[1500];
int length = fread(buf, sizeof(char), 1500, stdin);
```

2. Calls the function "myprintf()", passing it the "buf" variable.

```c
myprintf(buf);
```

3. "myprintf()" calls `printf()`, passing it its first argument. In this case, since "myprintf()" was called with "buf", the format string will be "buf".

```c
void myprintf(char *msg)
{
    // This line has a format-string vulnerability
    printf(msg);
}
```

The format-string vulnerability is present in "myprintf()", because the call to `printf()` this function encapsulates does not sanitize its content. So, considering `printf()` assumes the data needed to fill the placeholders are stored in the function's stack frame, if "myprintf()" were to be called with a string with placeholders, the program would print values present in the stack frame. 

As such, by construction a proper payload, executing "myprintf()" could lead to the divulgation of sensitive program data or the execution of malicious code.

## Task 1: Crashing the Program

Our first task was to crash the vulnerable program. We started by opening two terminals, one for running the server and another for communicating with it.

According to the guide, the server would output a message if it returned successfully upon printing our input, so we decided to test that by sending it a harmless message.

| Payload  | Server Response             |
|----------|-----------------------------|
| 'hi'     | ![Alt text](images/7-1.png) |

Now that we were aware of the output we did *not* want to receive, we started constructing our payload. Our first idea was to send the string `"%d"`, because it would force the program to find an integer in the value immediately above the format string on the stack. Since there would be no integer above our format string, the program should crash.

However, our hypothesis did not turn out to be correct, as proven by the output below:

| Payload  | Server Response             |
|----------|-----------------------------|
| '%d'     | ![Alt text](images/7-2.png)        |

This happened because the program interpreted the bytes above the format string as an integer, even if they represented something else entirely.

Next, we decided to send the `"%s"` string, thus making the program search for a pointer to a string in the value stored above the format string. We thought this approach would be more reliable, given that the program cannot simply interpret random values as pointers like it did with integers. 

The result of our experiment was as follows:

| Payload  | Server Response             |
|----------|-----------------------------|
| '%s'     | ![Alt text](images/7-3.png) |

Since neither our payload nor the "Returned properly" message were output, that means we managed to crash the program!

## Task 2: Printing Out the Memory

![Alt text](image.png)

### 2.A: Stack

The next task was to print data stored in the program's stack. More specifically, we had to print the first four bytes of our input, which would be stored somewhere on the stack.

Our plan was simple: input a string followed by several `%x` format specifiers. This would cause the program to print the values stored in the stack. As such, all we would have to do would be to find the hexadecimal value of our string.

In order to easily identify our string in the output, we decided that 0xAAAAAAAA would be its first four bytes. As for the number of format specifiers we would need, we opted to start with 100 and planned on increasing them if necessary.

Since creating the payload manually would be quite tedious, due to the amount of format specifiers we would have to write, we modified the "exploit.py" script that was provided in this lab.

```python
#!/usr/bin/python3
import sys

payload = bytearray.fromhex("A" * 8) + b"\n" + b" %x " * 100

# Save the format string to file
with open('badfile', 'wb') as f:
    f.write(payload)
```

Upon running the script, we sent our payload to the server and obtained the following response:

| Payload  | Server Response             |
|----------|-----------------------------|
| badfile  | ![Alt text](images/7-4.png) |

By counting the amount of spaces between values, we concluded that our payload was the 64th value printed. Thus, we needed exactly 64 `%x` specifiers: 63 for printing the intermediate values and another one for the first four bytes of our string.

### 2.B: Heap

The objective of the next task was to print a secret message stored in the heap. The only information we were given was its address, which was printed by the server upon each request like so:

![Alt text](images/7-5.png)

Having discovered in the previous section that our input was stored in the 64th value above the format string, we had the means to design a payload that would force the program to fetch it and access the content pointed by it.

In fact, if we wrote the address of the secret message followed by 63 `%x` format specifiers, we would be pointing to the memory region of our input. Then, by using a `%s` format specifier, the program would the input - the address of the message - and access its memory location, outputting its content.

Once again, we modified "exploit.py" so that it would concoct our payload. To make it easier to read the output, we decided to add line breaks before and after the secret message.

```python
address = 0x080b4008 # the address of the secret message
payload = address.to_bytes(4, byteorder='little') + b"%x" * 63 + b"\n%s\n"

# Save the format string to file
with open('badfile', 'wb') as f:
    f.write(payload)
```

After running the script, we send the payload to the server and received the following output:

| Payload  | Server Response             |
|----------|-----------------------------|
| badfile  | ![Alt text](images/7-6.png) |

There it lay, the most secret of messages: "A secret message"!
