# Buffer Overflow

## Setup

Before starting the tasks themselves, we had to deactivate a couple of security mechanisms Unix uses to prevent buffer overflows.

### Address Space Randomization

Ubuntu and other Linux-based operating systems randomize the starting address of the heap and the stack, which difficults guessing exact addresses. 

To disable this measure, we ran the following command:

```shell
sudo sysctl -w kernel.randomize_va_space=0
```

### Configuring /bin/sh

In most recent Ubuntu releases, the `/bin/sh/` symbolic link points to the `/bin/dash/` shell. This program, as well as `bash`, have a countermeasure against `Set-UID` programs: if they detected they are being executed in a `Set-UID` program, they immediately switch the user ID to the process's real user ID, therefore dropping the privilege.

## Task 1
