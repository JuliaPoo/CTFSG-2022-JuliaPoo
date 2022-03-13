from itertools import cycle
import string
from hashlib import sha1

ct = open("../dist/ct", 'rb').read()
allowed_chars = string.ascii_lowercase + '_- .!?'
allowed_chars = allowed_chars.encode()

def is_key_len(ct_msb, klen):
    for x,y in zip(ct_msb[:klen], ct_msb[klen:2*klen]):
        if x!=y: return False
    return True

ct_msb = [x >> 7 for x in ct[:0x20000]]
klen = 10
while not is_key_len(ct_msb, klen): 
    klen += 1
print("Key length:", klen)

# p^k = c
# Find for possible p, the possible k given c
c_to_k = {}
for p in allowed_chars:
    for k in range(0x100):
        c = p^k
        if c not in c_to_k:
            c_to_k[c] = set()
        c_to_k[c].add(k)

# Recover the key
key = []
for kidx in range(klen):
    data = ct[kidx::klen]
    k = c_to_k[data[0]].copy()
    for c in data[1:]:
        k &= c_to_k[c]
    assert len(k) == 1, "Not enough info!"
    key.append(list(k)[0])

# Recover secret
pt = [c^k for c,k in zip(ct, cycle(key))]
flag = "CTFSG{%s}"%sha1(bytes(pt)).hexdigest()
print(flag)