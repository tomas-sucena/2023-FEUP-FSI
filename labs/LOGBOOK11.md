# Public-Key Infrastructure (PKI)

# Setup

Before starting the tasks themselves, we had to set up an HTTPS web server. To that end, we added the following entry to the `etc/hosts` file of our virtual machine:

```
10.9.0.80   www.l11g04.com
```

# Task 1: Becoming a CA

> A Certificate Authority (or **CA** for short) is a trusted entity that issues **digital certificates**, which are used to certify the ownership of a <u>public key</u> by the named subject of the certificate.

There are two types of CAs:

* **Normal -** The certificates they issue are generally signed by another CA.
* **Root -** The certificates they issue are <u>unconditionally trusted</u>, thus not needing another signature.

Our first task was to become a **root CA**.

## Configuration the Server

We were going to rely on `OpenSSL` to create certificates, meaning we needed a **configuration file**. The default configuration file is located in `/usr/lib/ssl/openssl.cnf`, so we copied it to our working directory like so:

```bash
cp /usr/lib/ssl/openssl.cnf .
```

Next, we uncommented a line so we could allow the creation of certificates with the same subject.

```shell
unique_subject	= no	# Set to 'no' to allow creation of
					    # several certs with same subject.
```

The guide recommended we create an empty file for our "index.php", so we typed the command below:

```bash
touch index.php
```

Finally, we had to create a "serial" file with a single number in string format, so we did it like so:

```bash
echo 2023 > serial
```

While it was not necessary, we noticed the example directory provided by the guide had a folder named "certs" which contained the configuration file, so we decided to do the same ourselves:

```bash
mkdir certs
mv openssl.cnf certs
```


