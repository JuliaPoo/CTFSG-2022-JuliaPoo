# Textbook RSA

RSA encrypts the flag and RSA encrypts again the private key for the previous encryption.
Gives the player the public keys and the encrypted flag and keys.

Player can leak the flag via the server's error messages.

# Description (public)

```
Two times the RSA mean two times the security.

`nc <ip> <port>`
```

# Dependencies  

* Docker engine

# Setup Guide

Update public description with the IP and Port

Move into the `./src` folder and run:

```
dos2unix **
docker build -t textbookrsa .
docker run -d -p "0.0.0.0:<port>:9999" -h "textbookrsa" --name="textbookrsa" textbookrsa
```

Provide files in `dist` to players.

# Solution

One can leak out the flag via the error message. By sending `enc_priv1*x^e` for some integer `x > 1`, 
so that the server will decrypt `priv1` to be `p1' = x*priv1 % pub2`, the server will either reply `Wrong` 
if `p1' < pub1` and `Error` otherwise.

This can be used to form constraints to perform Bleichenbacher's attack. (./sol/sol.py)[./sol/sol.py] contains the script for the attack.

# Flag

`CTFSG{https://arxiv.org/abs/1802.03367?salt=290nlk01nx}`
