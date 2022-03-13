# pypy3 solve.py

import chal
import sys, time

t = time.time()

ALLOWED = b"_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM{}"

N_EVT = 0
def tracer(frame, event, arg=None):
    global N_EVT
    N_EVT += 1
sys.settrace(tracer)

def SideChannel(b:bytes)->int:
    global N_EVT
    N_EVT = 0
    chal.verify(b)
    return N_EVT

flag = []
while True:

    for c in ALLOWED:
        d = abs(SideChannel(flag+[c,0]) - SideChannel(flag+[c,1]))
        print(f"{chr(c)} {d}   ", end="\r")
        if d > 1000: break

    flag += [c]
    flagpt = bytes(flag).decode('utf-8')
    print(f"{flagpt}" + " "*15)

    if chal.verify(flag):
        break

print(f"DONE {time.time()-t}s")

# C
# CT
# CTF
# CTFS
# CTFSG
# CTFSG{
# CTFSG{I
# CTFSG{I_
# CTFSG{I_r
# CTFSG{I_re
# CTFSG{I_res
# CTFSG{I_resp
# CTFSG{I_respe
# CTFSG{I_respec
# CTFSG{I_respect
# CTFSG{I_respect_
# CTFSG{I_respect_U
# CTFSG{I_respect_Ur
# CTFSG{I_respect_Ur_
# CTFSG{I_respect_Ur_C
# CTFSG{I_respect_Ur_Cu
# CTFSG{I_respect_Ur_Cun
# CTFSG{I_respect_Ur_Cunn
# CTFSG{I_respect_Ur_Cunni
# CTFSG{I_respect_Ur_Cunnin
# CTFSG{I_respect_Ur_Cunning
# CTFSG{I_respect_Ur_Cunning_
# CTFSG{I_respect_Ur_Cunning_B
# CTFSG{I_respect_Ur_Cunning_BU
# CTFSG{I_respect_Ur_Cunning_BUT
# CTFSG{I_respect_Ur_Cunning_BUT_
# CTFSG{I_respect_Ur_Cunning_BUT_n
# CTFSG{I_respect_Ur_Cunning_BUT_no
# CTFSG{I_respect_Ur_Cunning_BUT_no}
# DONE 228.14983677864075s