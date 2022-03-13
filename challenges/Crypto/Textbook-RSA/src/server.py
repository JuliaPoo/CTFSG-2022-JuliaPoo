from typing import Tuple

from Crypto.Util.number import bytes_to_long, getPrime
from os import urandom
from hashlib import shake_128

from flag import flag

e = 1+(1 << 16)
def xor_bytes(a, b): return type(a)([x ^ y for x, y in zip(a, b)])


def gen(strength: int) -> Tuple[int, int]:

    p = getPrime(strength)
    q = getPrime(strength)
    n = p*q
    phi = n - p - q + 1
    d = pow(e, -1, phi)

    return n, d


def pad(msg: bytes) -> bytes:

    # Yea I made the padding really hard to attack,
    # so don't attack it

    assert len(msg) < 60

    l = 76-len(msg)-8
    msg = bytearray(
        msg + urandom(8) + bytes([l]*l)
    )
    msg[:38] = xor_bytes(msg[:38], shake_128(msg[38:]).digest(38))
    msg[38:] = xor_bytes(msg[38:], shake_128(msg[:38]).digest(38))
    return bytes(msg)


def unpad(msg: bytes) -> bytes:
    msg = bytearray(msg)
    msg[38:] = xor_bytes(msg[38:], shake_128(msg[:38]).digest(38))
    msg[:38] = xor_bytes(msg[:38], shake_128(msg[38:]).digest(38))
    msg = msg[:-msg[-1]-8]
    return bytes(msg)


def rsa_enc(pub: int, msg: int) -> int:
    assert msg < pub, "Error encrypting!"
    return pow(msg, e, pub)


def rsa_dec(pub: int, priv: int, msg: int) -> int:
    assert msg < pub and priv < pub, "Error decrypting"
    return pow(msg, priv, pub)


def main():

    pflag = bytes_to_long(pad(flag))

    # 306>305 so it doesn't error out on
    # rsa_dec(pub2, priv2, enc_priv1)
    pub1, priv1 = gen(305)
    pub2, priv2 = gen(306)

    enc_flag = rsa_enc(pub1, pflag)
    enc_priv1 = rsa_enc(pub2, priv1)

    print("enc_flag =", hex(enc_flag))
    print("enc_priv1 =", hex(enc_priv1))
    print("pub1 =", hex(pub1))
    print("pub2 =", hex(pub2))

    while True:

        while not (user_in := input("enc_priv1: ")).isdigit():
            ...
        user_in = int(user_in)

        dflag = 0
        try:
            dec_priv1 = rsa_dec(pub2, priv2, user_in)
            dflag = rsa_dec(pub1, dec_priv1, enc_flag)
        except AssertionError as e:
            print(f"[x] Error! {e}")
            continue

        if dflag == pflag:
            break

        print("[*] Wrong!")

    print("[*] Byeeee ^-^")
    print("[*] Remember to get the flag on your way out!")


if __name__ == "__main__":
    main()
