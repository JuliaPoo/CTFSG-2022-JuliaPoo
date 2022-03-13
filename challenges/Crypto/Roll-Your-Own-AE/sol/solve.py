import requests
import base64
from threading import Thread

URL = "http://192.168.1.112:7777"
n_requests = 0


def get_cookie(username: bytes):

    global n_requests
    n_requests += 1

    r = requests.post(URL, data={b'username': username})
    return base64.b64decode(r.cookies['user'])


def test_cookie(cookie):

    global n_requests
    n_requests += 1

    cookie = base64.b64encode(cookie).decode('utf-8')
    r = requests.get(URL, cookies={'user': cookie})
    content = r.content.decode('utf-8')

    if "An error occurred!" not in content:
        return 0  # No error
    if "`data` has invalid length" in content:
        return 1  # Length invalid
    if "`data` does not have a valid signature" in content:
        return 2  # Length valid

    return 3  # Should not be encountering this case


def pad(data: bytes):
    i = -len(data) % 16
    return data + b'\0'*i


def job(c: int, send: bytes):
    global job_ret
    if job_ret:
        return
    case = test_cookie(send)
    if case == 2:
        job_ret = c  # Valid length! value of `c` has been leaked!


allowed = b'0123456789_qwertyuiopasdfghjklzxcvbnm?'
known = ord(b'=')
k = 6

flag = ""
idx = 0
while True:

    enc = get_cookie(b'A'*(64-idx))
    salt = enc[:16]
    curr = enc[16*k:16*k+32]

    threads = []
    job_ret = None
    for c in allowed:
        i = c*0x100 + known - 16
        send = salt + curr + b'\0'*i
        send = pad(send)
        threads.append(Thread(target=job, args=(c, send)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    known = job_ret
    # None of `allowed` matches. End of flag.
    if not known:
        break

    flag += chr(known)
    idx += 1
    print(flag, end="\r")


print("Flag: CTFSG{%s}" % flag)
print("Number of requests made:", n_requests)
