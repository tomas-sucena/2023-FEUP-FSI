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
$input_uname = $_GET[’username’];
$input_pwd = $_GET[’Password’];
$hashed_pwd = sha1($input_pwd);
...
$sql = "SELECT id, name, eid, salary, birth, ssn, address, email,
        nickname, Password
    FROM credential
    WHERE name= ’$input_uname’ and Password=’$hashed_pwd’";

$result = $conn -> query($sql);
```

This sql query, makes it so, if there is no verification of the user input, one could make an SQL injection attack. We will exploit this to complete our task. We will also use it as a reference to make the attack.

### Task 2.1: SQL Injection Attack from webpage

We must log in into the Admin's account without knowing its password. To do so, we need to input a username so that the password condition in the SQL query is ignored.

We chose to make the username `admin' #`. The `admin'` portion makes it so it gets us the admin's credentials while the `#` makes it so it comments out the remainder of the SQL code, thus not verifying the password. There was no need to input anything into the password field as it is ignored.

With this, we successfully logged in as the admin.

(img)
(img)
