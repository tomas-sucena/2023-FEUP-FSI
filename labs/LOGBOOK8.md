# SQL Injection
## Task 1: Get Familiar with SQL Statements

As instructed in this task, we firstly opened the shell using the command `docksh`, passing it the value we obtained using `dockps`. Afterwards, we opened the MySQL container by using the command `mysql -u root -pdees`. Then, we opened the provided database, `sqllab_users`, by using the command `use sqllab_users;` inside the MySQL container.

(img)

By using the command `show tables`, we found the table `credential`, as expected.

(img)

In order to view the contents of this table, we used the following SQL query:

```sql
select * from credential;
```
Which gave us profile information for all users. 

(img)

Because we only want the profile information of the user Alice, all we had to do was to change the query and so we got the profile information for Alice.

```sql
select * from credential where name = "Alice";
```

(img)

## Task 2: SQL Injection Attack on SELECT Statement

To get started with this task, we found it especially important to look at the provided code snippet.

```php
$input_uname = $_GET['username'];
$input_pwd = $_GET['Password'];
$hashed_pwd = sha1($input_pwd);
...
$sql = "SELECT id, name, eid, salary, birth, ssn, address, email,
        nickname, Password
    FROM credential
    WHERE name= ’$input_uname’ and Password=’$hashed_pwd’";

$result = $conn -> query($sql);
```

This SQL query makes it so, if there is no verification of the user input, one could make an SQL injection attack. We will exploit this to complete our task. We will also use it as a reference to make the attack.

### Task 2.1: SQL Injection Attack from webpage

We must log in into the Admin's account without knowing its password. To do so, we need to input a username so that the password condition in the SQL query is ignored.

We chose to make the username `admin' #`. The `admin'` portion makes it so it gets us the admin's credentials while the `#` makes it so it comments out the remainder of the SQL code, thus not verifying the password. There was no need to input anything into the password field as it is ignored.

With this, we successfully logged in as the admin.

(img)
(img)


## Task 3: SQL Injection Attack on UPDATE Statement

> In SQL, `UPDATE` statements are used to modify existing records in a table.

Our final tasks consisted in exploiting an SQL injection vulnerability present in the Edit Profile page. As its name suggests, this page contains a simple input form for altering the profile information of an account, as shown below:

![Alt text](image-1.png)

The guide also discloses the code fragment that processes the user input. Once again, it contains an unsanitized database query:

```php
$hashed_pwd = sha1($input_pwd);
$sql = "UPDATE credential SET
    nickname=’$input_nickname’,
    email=’$input_email’,
    address=’$input_address’,
    Password=’$hashed_pwd’,
    PhoneNumber=’$input_phonenumber’
    WHERE ID=$id;";
$conn->query($sql);
```

### 3.1: Modifying our salary

Our next objective was to update our salary. That is, upon logging in to an account, we had to use the input form to alter its database entry.

To that end, we logged in to Alice's account by repeating the attack from [before](#task-21-sql-injection-attack-from-webpage), except instead of 'admin' we wrote 'alice':

![Alt text](image-2.png)

Immediately after logging in, we were redirected to a page which contained Alice's profile information, including her salary: **20000**.

![Alt text](image-3.png)

Now that we were familiar with the value we had to change, we navigated to the Edit Profile page. However, as seen above, there was no form for altering the salary. Thankfully, the guide revealed that the salaries are stored in a column appropriately named "salary", so we had all the information we needed.

Considering that each assignment in the query (i.e. `value=’$input_value’`) was in a separate line, our payload had the following restrictions:
* Contain a backtick, so as to close the SQL string in the query.
* Have a clause which updates the `salary` column (i.e. `salary=...`).
* Have a hashtag at the end to comment the last backtick.

With that in mind, we chose the following payload:

![Alt text](image-4.png)

After inputting, we checked Alice's profile again.

![Alt text](image-5.png)

And _voilá_, Alice was now 50x richer!
