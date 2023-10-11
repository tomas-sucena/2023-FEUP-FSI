# Environment Variable and Set-UID Lab

## Task 1: Manipulating Environment Variables

As described in the task, by using the `env` command, the console printed out all the environment variables of the system.
Then, using `export`, we set a new environment variable, COLR, whose value we set to "blue". After verifying it had been correctly set, we proceeded to remove it using `unset`.

## Task 2: Passing Environment Variables from Parent Process to Child Process

We ran the provided program, transfering its output to a file "F1". As requested in the guide, we changed the commented lines and transfered the output to another file, "F2".
Afterwards, by using the command `diff` with the two files, we noticed there was no difference. This is so, because the child process will have the same environment variables as the parent.

## Task 3: Environment Variables and execve()

The task lets us know that `execve` is a function that allows us to load and execute a new command, all the while the process's data is completely replaced by the process of the command ran.
Through the provided program, we find out that, should the third parameter of |execve| be set to NULL, the new program will not automatically inherit environment variables. By setting the third parameter to to the variable "environ" instead, the program will then inherit environment variables.

## Task 4: Environment Variables and system()

Similarly to `execve`, `system` also executes a new command, however, by requesting the shell to do it.
Through the provided program, we verified that the environment variables of the calling process are passed to the new process, as predicted by the guide. 
