import os
import string
import random
from itertools import cycle
from hashlib import sha1

allowed_chars = string.ascii_lowercase + '_- .!?'
allowed_chars = allowed_chars.encode('utf-8')

xor_enc = lambda pt,key: [x^y for x,y in zip(pt, cycle(key))]

pt  = [allowed_chars[i&31] for i in os.urandom(0x100000)]
key = os.urandom(random.randint(10,0x1000))

ct = xor_enc(pt, key)

open('flag', 'w').write("CTFSG{%s}"%sha1(bytes(pt)).hexdigest())
open('ct', 'wb').write(bytes(ct))