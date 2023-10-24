# Buffer Overflow

This CTF consists in two very similar challenges. In each of them, we had to exploit a program with a buffer overflow vulnerability in order to access a file named "flag.txt", which, as the name implies, contained the flag.

Each challenge came with a folder which contained a few files. The most relevant were the following:

* **main.c** - the source code of the vulnerable program
* **program** - the executable corresponding to the vulnerable program

## 1st flag

### Analysis

Before attempting to exploit the program, we had to properly understand its source code. As such, we opened "main.c" and started thoroughly scrutinizing it.

The script itself was pretty simple. It can be summarized as follows:

1. Create two character arrays, "meme_file" and "buffer", with sizes 8 and 32, respectively.

```c
char meme_file[8] = "mem.txt\0";
char buffer[32];
```

2. Read 40 characters of user input and store them in the "buffer" array.

```c
scanf("%40s", &buffer);
```

3. Open the file whose name is given by the "meme_file" variable.

```c
FILE *fd = fopen(meme_file,"r");
```

4. Attempt to read from the file, if it exists, and store its content on "buffer". Then, print "buffer".

```c
while(1){
    if(fd != NULL && fgets(buffer, 32, fd) != NULL) {
        printf("%s", buffer);
    } else {
        break;
    }
}
```

**Note:** This step is equivalent to printing the content of the file, given it exists.

Upon analyzing this script, it became glaringly obvious that we could overwrite the contents of "meme_file" by purposefully overflowing the "buffer". This is because the two variables are side by side in **memory** and, since "buffer" is initialized after "meme_file", the end of "buffer" corresponds to the start of "meme_file".

### Test

