import hashlib
import re

class SHACBC:

    def __init__(self, key:bytes, block_size:int):
        self.bz = block_size
        self.key = key
        
    def _gethash(self, block:bytes):
        return hashlib.shake_128(self.key+block).digest(self.bz)
        
    def _pad(self, pt:bytes):
        padlen = (-len(pt))%self.bz
        return pt + b'\0'*padlen
    
    def encrypt(self, pt:bytes):

        ct = b""
        prev_ct_blk = b"\0"*self.bz
        pt = self._pad(pt)
        pt = [pt[i*self.bz : (i+1)*self.bz] for i in range(len(pt)//self.bz)]
        
        for blk in pt:
            xored = bytes([x^y for x,y in zip(prev_ct_blk, blk)])
            prev_ct_blk = self._gethash(xored)
            ct += prev_ct_blk

        return ct

    def decrypt(self, ct:bytes):

        "Oh no"

flag = open('flag').read()
match = re.match(r"^CTFSG\{([a-zA-Z ]+)\}$", flag)
assert match, "`flag` doesn't follow flag format!"

naked_flag = match.group(1)
naked_flag = naked_flag.encode('utf-8')

key = open('key', 'rb').read()

s  = SHACBC(key, 4)
pt = naked_flag*100000
ct = s.encrypt(pt)

open('flag.enc', 'wb').write(ct)