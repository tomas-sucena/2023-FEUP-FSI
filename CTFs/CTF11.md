# RSA

This challenge consisted in deciphering the flag, which had been poorly encrypted using plain **RSA**.

This system requires the following values:
* Two **prime numbers**, `p` and `q`.
* Their product, `n` ($n = p \times q$).
* An exponent, `e`, such that $1 < e < (p-1)(q-1)$.
* `d`, such that $d \equiv (e - 1) \mod\ (p-1)(q-1)$.

The keys would then be the tuples below:
* **Public key -** $(n, e)$
* **Private key -** $(n, d)$

## Analysis

