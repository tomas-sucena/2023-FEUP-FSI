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

### Task 2.2: SQL injection from command line

To perform this attack from a command line is fairly similar to doing so in a webpage. Since the website gets our inputs to username and password, then using HTML POST with our arguments, we can simply create a link that has the same effect. Let's take a look at the example:

```sh
$ curl 'www.seed-server.com/unsafe_home.php?username=alice&Password=11'
```

We can simply modify the link above to have the arguments we passed in Task 2.1. Something to take in mind when creating this link is that we can not simply have specials characters, such as `#`, in the link. With this said, all we have to do is transform our `' #` into `%27%20%23`. With this said, we just have to run the following command to execute the attack:

```sh
$ curl 'www.seed-server.com/unsafe_home.php?username=admin%27%20%23'
```

(img)

If we grab this HTML code and put it in a file, then loading it into the browser, we can more easily see the results of our attack.

(img)

### Task 2.3: Append a new SQL statement

In the website, we attempted to run 2 statements with a SQL injection attack by attempting to log in into the website with the username `admin'; DROP TABLE credential; #`, which should have dropped the table credential, removing the data. However, this did not happen. Instead we were presented with an error message:

(img)

This is so because this website is protected from multiple SQL statements by using the PHP function `query` over `multi_query`. The latter allows for multiple queries to be ran on its parameter. The function `query`, however, prevents this behavior, by only allowing a single query to happen. 
