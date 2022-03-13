# Xor Can't Be That Hard

Some simple bit fengshui.

# Description (public)

```
XorXorXorXorXorXorXorXorXorXorXorXorXorXorXorXor
```

# Setup Guide 

1. Provide files in `dist/` folder to players

# Solution

Key length can be found by guessing the key length from 10 to 0x1000. To check if the key length guessed is correct, correlate the MSB of two ciphertext blocks. The MSB should be the same. This stems from the plaintext MSB always being 0.

The actual key can be recovered by taking all bytes of the ciphertext that got xored by a given key byte, and ensuring that all those bytes can be decrypted into `allowed_chars`.

Solve script in `sol/solve.py`.

# Flag

`CTFSG{81aee17d64bd59cd167ffce34523060f7e2bcac0}`


