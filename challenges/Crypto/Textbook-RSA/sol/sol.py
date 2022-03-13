from hashlib import shake_128
from Crypto.Util.number import long_to_bytes
from typing import Tuple
from nclib import Netcat
from libnum.ranges import Ranges

NC = ("192.168.139.128", 7777)

# Let p be priv1,
#     c be enc_priv1,
#     d be priv2,
#     n2 be pub2,
#     n1 be pub1

# c^d = p
# (x^e c)^d = x^ed c^d = xp
# If it does not error from xl to xh-1, but does so at xh,
# then xl*p - n2*k < n1 <= xh*p - n2*k:
#
#    Upper:
#    xh*p - n2*k >= n1, k <= (xh*p - n1) / n2, p >= (n1 + n2*k) / xh
#        Since 0 < p < n2, 0 <= k <= (xh*p - n1) / n2 < xh - n1/n2
#
#    Lower:
#    xl&p - n2*k < n1, _, p < (n1 + n2*k) / xl
#
#    For 0 < k < x - n1/n2:
#       (n1 + n2*k) / xh <= p < (n1 + n2*k) / xl


def ru(nc: Netcat, b: bytes) -> bytes:
    """recieve until"""

    s = b""
    while b not in s:
        s += nc.recv(1)
    return s[:-len(b)]


def init_nc() -> Netcat:
    return Netcat(NC)


def get_constants_from_server(nc: Netcat) -> Tuple[int, int, int, int]:

    ctn = ru(nc, b"enc_priv1: ").decode()
    ctn = ctn.split("\n")
    enc_flag = int(ctn[0].split("=")[1], 16)
    enc_priv1 = int(ctn[1].split("=")[1], 16)
    pub1 = int(ctn[2].split("=")[1], 16)
    pub2 = int(ctn[3].split("=")[1], 16)
    return enc_flag, enc_priv1, pub1, pub2


nquery = 0
def test_waters(nc: Netcat, x: int) -> int:

    global nquery
    nquery += 1
    tosend = (pow(x, 0x10001, n2)*c) % n2

    nc.send(str(tosend).encode() + b"\n")
    res = ru(nc, b"enc_priv1: ").decode().strip()

    if res == "[x] Error! Error decrypting":
        return 0
    if res == "[*] Wrong!":
        return 1
    return 2


def get_x(nc: Netcat, start: int) -> Tuple[int, int]:

    x = 0
    while True:

        res = test_waters(nc, x+start)
        if x == 0 and res == 0:
            start += 1
            continue

        if res == 0:
            break

        x += 1

    return start, x+start


def improve_range(nc: Netcat, start: int, r: Ranges) -> Tuple[int, Ranges]:

    xl, xh = get_x(nc, start)

    nr = Ranges()
    for rl, rh in r._segments:

        # (n1 + n2*kl)/xl + 1 > rl
        # kl > ((rl-1)*xl - n1) / n2
        kl = ((rl-1)*xl - n1) // n2 + 1

        # ((n1 + n2*kh)//xh + 1 < rh
        # kh < ((rh-1)*xh - n1) / n2
        kh = ((rh-1)*xh - n1) // n2

        for k in range(kl, kh+1):
            al, ah = (n1 + n2*k)//xh + 1, (n1 + n2*k)//xl
            al, ah = max(rl, al), min(rh, ah)
            nr = nr | Ranges((al, ah))

    return xh, nr


def xor_bytes(a, b): return type(a)([x ^ y for x, y in zip(a, b)])
def unpad(msg: bytes) -> bytes:
    msg = bytearray(msg)
    msg[38:] = xor_bytes(msg[38:], shake_128(msg[:38]).digest(38))
    msg[:38] = xor_bytes(msg[:38], shake_128(msg[38:]).digest(38))
    msg = msg[:-msg[-1]-8]
    return bytes(msg)


def rsa_dec(pub: int, priv: int, msg: int) -> int:
    assert msg < pub and priv < pub, "Error decrypting"
    return pow(msg, priv, pub)


nc = init_nc()
f, c, n1, n2 = get_constants_from_server(nc)

growth = int(n2//n1)
while True:

    assert growth >= 2, "[x] Ratio between n1 and n2 not big enough!"

    r = Ranges((0, n1))
    xh = 2
    i = 0

    succ = True
    while r.len > 1 << 10:

        lr = len(r._segments)
        bl = xh.bit_length()
        print(f"{i} {lr} {bl} ~{int(bl/602*100+.5)}% {nquery} queries \r", end="")
        i += 1

        if lr >= 20:  # Growth rate too fast!
            print(f"[*] Growth rate `{growth}` too big!")
            print(f"[*] Potential unlucky run, consider rerunning if it takes too long.")
            growth -= 1
            succ = False
            break

        xh, r = improve_range(nc, xh, r)
        xh = xh*growth

    if succ:
        break

print(f"[*] Queried server {nquery} times!")

for p in r:
    flag = rsa_dec(n1, p, f)
    flag = unpad(long_to_bytes(flag))
    if b"CTFSG" in flag:
        break

print("[*] Flag:", flag.decode())
