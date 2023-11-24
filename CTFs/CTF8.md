# SQL Injection

In this CTF we need to exploit the website using a SQL injection to log in, without knowing the user's username and password.

# Exploration

After entering the website, we find ourselves in its login page. To attain the flag, we know we must login, despite having no credentials.

In the provided `index.php` file, we may also see the query used in the login:

```php
$username = $_POST['username'];
$password = $_POST['password'];
               
$query = "SELECT username FROM user WHERE username = '".$username."' AND password = '".$password."'";
```

Given both username and password are not hashed, we are likely to be capable of executing an SQL injection attack on this website.

# Execution

We wonder if the form is protected against code execution, by using a single quote to close the input's string.

To our surprise, it is not protected for that exploit, so we developed a SQL query to let us access the website without knowing the credentials of a user.

Given we are aware of how the query is performed, a username such as `' OR 1=1;--` should be enough to exploit this vulnerability.

Replaced, it will look like this:

``"SELECT username FROM user WHERE username = '' OR 1=1;--' AND password = ''";`

It is important to note that we use `--` in order to comment the remainder of the query, thus making it skip the password condition, while successfully logging us in as any user.

![img](images/sqlinjection.png)

When we submit the form, we successfully get flag

![img](images/sqlinjection_flag.png)
