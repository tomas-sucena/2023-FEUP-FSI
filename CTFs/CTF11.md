# RSA

This CTF consisted in deciphering the flag, which had been poorly encrypted using plain **RSA**.

This system requires the following values:
* Two **prime numbers**, `p` and `q`.
* Their product, `n` ($n = p \times q$).
* An exponent, `e`, such that $1 < e < (p-1)(q-1)$.
* `d`, such that $d \times e \equiv 1 \mod\ (p-1)(q-1)$.

The keys would then be the tuples below:
* **Public key -** $(n, e)$
* **Private key -** $(n, d)$

The strength of the RSA cipher comes from the fact that, given the product `n`, it is computationally unfeasible to deduce the two prime numbers, `p` and `q`, which are required to decrypt the message.

However, in this challenge, it is disclosed that $p \approx 2^{512}$ and $q \approx 2^{513}$, meaning that the possible values for the prime numbers were greatly diminished.

## Analysis

The guide provided the Python script that served as the backend of this CTF. Its behaviour can be summarized as follows:

1. Read the file which contains the flag.

```python
FLAG_FILE = '/flags/flag.txt'

...

with open(FLAG_FILE, 'r') as fd:
	un_flag = fd.read()
```

2. Get the parameters which will be used in the cipher.

```python
(p, q, n, phi, e, d) = getParams()
```

3. Output the **public key** (i.e. the exponent `e` and the product `n`).

```python
print("Public parameters -- \ne: ", e, "\nn: ", n)
```

4. Encrypt the flag and output it.

```python
print("ciphertext:", hexlify(enc(un_flag.encode(), e, n)).decode())
```

While it was useful to understand the output we would receive when connecting to the server, we were more interested in the auxiliary functions which supported the script. They are presented below:

* **enc() -** Given a plaintext message, the exponent `e` and the product `n`, encrypts the message.

```python
def enc(x, e, n):
    int_x = int.from_bytes(x, "little")
    y = pow(int_x,e,n)
    return hexlify(y.to_bytes(256, 'little'))
```

* **dec() -** Given an encrypted message, `d` and the product `n`, decrypts the message.

```python
def dec(y, d, n):
    int_y = int.from_bytes(unhexlify(y), "little")
    x = pow(int_y,d,n)
    return x.to_bytes(256, 'little')
```

We swiftly realized that, if we could discover the **primes** `p` and `q` used to encrypt the flag, we would be able to use the "dec()" function to decrypt the ciphertext.

## Computing Primes

As seen in the section above, the key to solving this challenge was the computation of **prime numbers**. Since we would be working with very big integers, we would need an algorithm that could quickly yet reliably determine whether a number is prime.

For that purpose, the guide recommended the [Miller-Rabin algorithm](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test). Upon searching online, we found the following [Python implementation](https://gist.github.com/Ayrx/5884790) of said algorithm:

```python
def miller_rabin(n, k):

    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    # If number is even, it's a composite number

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
            
    return True
```

We placed it in a new Python script named "primes.py", which can be found [here](etc/primes.py). In addition, we also created a simple function which, given an integer, returns the next prime number.

```python
def nextPrime(num):
    num += 1 if num % 2 == 0 else 2

    while not miller_rabin(num, 40):
        num += 2
    
    return num
```

## Preparing the Script

Before writing our code, we needed a few variables: the **public key**, constituted by the exponent `e` and the product `n`, and the **ciphertext**. By connecting to the server, we obtained them as follows:

![Alt text](images/11-1.png)

Next, we started writing our script. Its behaviour can be summarized like so:

1. Define the decryption function.

```python
from binascii import hexlify, unhexlify
from primes import nextPrime

def dec(y, d, n):
    int_y = int.from_bytes(unhexlify(y), "little")
    x = pow(int_y,d,n)
    return x.to_bytes(256, 'little')
```

**Note:** We were having difficulties importing the decryption function from the "challenge.py" script, so we decided to just copy it directly into our script.

2. Initialize the variables whose values we obtained from the server - the **public key** and the **ciphertext**.

```python
# public key
e = 65537
n = 359538626972463181545861038157804946723595395788461314546860162315465351611001926265416954644815072042240227759742786715317579537628833244985694861278987734749889467798189216056224155419337614971247810502667407426128061959753492358794507740889756004921248165191531797899658797061840615258162959755571367021109

ciphertext = "3334303164633363353339356539353130346566343665363638653537333831323930653036646532336666633036636166396164656265373334636531323430653138623237613166313636343362316661663330643038623331613561633136386261313636373064636633373261633366633436656532636664636335616333303431626334396630306431346462353165643831653065343233653866333933353737636231336266303431353738343835303261663564613638316164623534356165646339663433306435656437313234373064323635656136366130653664626634653838626237313366336638393736363934363636393130313030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030"
```

3. Compute the **primes** used to encrypt the flag.

```python
# compute the primes
p = initial_p = nextPrime(2 ** 512)
q = nextPrime(2 ** 513)

while True:
	while p * q < n:
		p = nextPrime(p)
		continue
		
	if p * q == n:
		break
		
	q = nextPrime(q)
	p = initial_p # reset p
```

Firstly, we assigned `p` and `q` the closest primes to $2^{512}$ and $2^{513}$, respectively. Then, for every pair of `p` and `q`, we compared their product with `n`. If both values were equal, that meant we had found our primes.

4. Compute `d`.

```python
# compute d
d = pow(e, -1, (p - 1) * (q - 1))
```

5. Decrypt the ciphertext using the **private key** - the tuple $(n, d)$. Then, print it.

```python
# decrypt the message
msg = dec(unhexlify(ciphertext), d, n).decode()

# print the message
print(msg)
```

**Note:** Unlike in the previous CTF, we did not have to rely on <ins>regular expressions</ins> to figure out whether the decrypted message corresponded to the flag, because finding the prime numbers - `p` and `q` - sufficed.

The finalized script can be found [here](etc/exploit-CTF11.py).

## Attack!

It was finally time to attack. Upon running our script, we obtained the following output:

![Alt text](images/11-2.png)

We got the flag: `flag{6272e91117b4bf55bfba6bc22a783f29}`!
