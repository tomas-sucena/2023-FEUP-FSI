# Environment Variable and Set-UID Lab

## Task 1: Manipulating Environment Variables

As described in the task, by using the `env` command, the console printed out all the environment variables of the system.

Then, using `export`, we created a new environment variable, COLOR, whose value we set to "blue".

![Alt text](images/image-1.png)

After ensuring that COLOR had been correctly set, we proceeded to remove it using `unset`. To confirm that it had been successfully deleted, we used `printenv` again and verified that it did not print "blue" anymore.

![Alt text](images/image-2.png)

## Task 2: Passing Environment Variables from Parent Process to Child Process

As requested in the guide, we compiled and ran myprintenv.c twice.

* Firstly, we ran the script as it was provided. Since it was meant to print the environment variables of a **child** process, we saved its output in a file named "child".
* Next, we altered the script by changing the lines that were commented, making it so it would now print the environment variables of the **parent** process. Because of this, we saved the output of the modified script in a file named "parent".

By using the `diff` command with the two files, we noticed there was no difference. 

![Alt text](images/image-4.png)

As such, we concluded that child processes inherit the environment variables of their parent.

## Task 3: Environment Variables and execve()

The guide lets us know that `execve()` is a function that allows us to load and execute a new command, all the while the process's data is completely replaced by the process of the command ran.

To test the behaviour of this command, we compiled and ran myenv.c twice.

* Firstly, we ran the script without modifying it, which meant the third parameter of `execve()` was set to `NULL`. To our surprise, nothing was output.

![Alt text](images/image-5.png)

* Next, we changed the script so that the third parameter of `execve()` was now `environ`. This time, running the program printed the environment variables.

Through this experiment, we found out that the third parameter of `execve()` (named `envp` in the Linux manual) is a pointer to the execution environment we want to pass to the new program. Since `envp` is `NULL` by default, we can conclude that `execve()` does NOT automatically inherit the environment variables of the calling process.

## Task 4: Environment Variables and system()

The guide informs us that `system()`, unlike `execve()`, does not directly execute a command. Instead, it requests the shell to do it.

The behaviour of `system()` can be summarized like this:

* `system()` calls `execl()` to execute `/bin/sh`.
* `execl()` calls `execve()` and passes it the `environ` variable, which, as we discovered in the previous task, is an array containing the environment variables of the calling process.

In simple terms, `system()` wraps a call to `execve()`, ensuring the environment variables are inherited by the latter. So, any command executed with `system()` should retain the execution environment of the calling process.

To verify this hypothesis, we copied the code present in this section of the guide into a script called "task4.c" and executed it. 

![Alt text](images/image-6.png)

Predictably, the environment variables were printed, thus validating our conclusion.


