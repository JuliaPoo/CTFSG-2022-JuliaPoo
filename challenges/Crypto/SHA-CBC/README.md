# SHA-CBC

Leak information about the plaintext entirely through collisions.

# Description (public)

```
Luz attempted to implement SHA-CBC. It's like AES-CBC but with SHAKE-128 instead.
Luz got as far as implementing the encryption before Luz realised:
SHAKE-128 isn't symmetric like AES is.
Luz can't write the decryption at all.
Even if Luz knew the key.

Luz, being overzealous, Luz encrypted the flag and threw it away.

Have fun recovering it.
```

# Setup Guide 

1. Provide files in `dist/` folder to players

# Solution

`enc.py` uses CBC block cipher mode on a 4 bytes block size, which is very prone to key exhausion.

When two cipher text blocks are identical, there are three reasons for collisions.

1. Output collision in the block cipher
2. Collision in the input of the block cipher whereby the ciphertext blocks
that contributed to the input are different.
3. Collision in the input of the block cipher whereby the ciphertext blocks
that contributed to the input are the same.

Only collisions resulting from (2) leaks information about the ciphertext
```
input = prev_plaintext_blk ^ curr_ciphertext_blk
input1 = input2 = pt_blk1 ^ ct_blk1 = pt_blk2 ^ ct_blk2
    ==> pt_blk1 ^ pt_blk2 = ct_blk1 ^ ct_blk2
```

Collisions are expected to happen once ever `2^(blklen*4 - 1) = 32768` blocks assuming random oracle.

However, after a while, due to the repetitiveness of the plaintext, the ciphertext will also start
to repeat itself ~`R = 2^(blklen*4 - 1) * lcm(blklen, flaglen) / blklen = 2064384` assuming random oracle,
leading to many many (useless) collisions by reason (3).
In practice this number is way smaller or I have made a mistake. This sets a bound to how much info
one can recover from the ciphertext regardless of how many times the flag was repeated, since once the
ciphertext starts repeating no new info can be gained.

The expected number of collisions due to (2) is hence `~ lcm(blklen, flaglen) / (2*blklen) = 31.5`,
which is enough to recover the flag.

While reason (3) can be removed by removing the ciphertext parts that collide with the same index in the flag,
reason (1) and (2) are indistinguishable. Only a subset of these collisions (reason 2)
lead to satisfiable constraints that result in the flag.

The player would have to depth-first-search for the subset of constraints that are satisfiable
and lead to one solution.

`sol\solve.py` contains the solve script.

# Flag

`CTFSG{Oh I gUesS I hAVe alwAys likEd pOurIng ThingS inTo oTher ThiNgs}`


