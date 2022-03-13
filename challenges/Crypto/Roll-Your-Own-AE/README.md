# Roll Your Own AE

Leaking of secret via the length field (decryption oracle).
Based on the [The Cryptographic Doom Principle](https://moxie.org/2011/12/13/the-cryptographic-doom-principle.html).

# Description (public)

```
Okay so you've heard of AE? It's so in right now.
Even Signal uses AES-CBC HMAC-SHA256.
I too, wanna use AES-CBC HMAC-SHA256, 
but python doesn't really have one built in.

EZ, I made mah own.
With some goodies too!

1. Random IVs!
2. Salted keys!
3. Unknown padding! (No padding oracles here!)

This is obviously so secure right now.

http://<host>:<port>
```

# Dependencies  

* Docker engine

# Setup Guide

Update public description with the IP and Port

Move into `./src` folder and run:

```
docker build -t ae .
docker run -d -p "0.0.0.0:<port>:5555" -h "ae" --name="ae" ae
```

Provide files in `dist` to players.

## Solution

The encrypted cookie takes the form:

```
Encrypted message format:
    final_encrypt  = [salt:16][iv:16][encrypted_data]
    encrypted_data = AESCBC(PAD([len:2][data][hmac:32]))
    hmac           = HMACSHA256([len:2][data])
```

Notice that in order for the server get the hmac, it has to decrypt `len`?

The server then errors out `data has invalid length` or `data does not have a valid signature`
depending on if the `len` field is valid.

Furthermore, and variable "name" field in the cookie and also AES-CBC allows
the player to offset the flag in the `data` field such that it gets decrypted an intepreted as 
the `len` field.

The player can hence leak the flag character by character based on the server errors, leaking
the flag in about 1000 requests.

## Flag

`CTFSG{d0_n0t_r0ll_y0ur_0wn_ae_ev4r}`