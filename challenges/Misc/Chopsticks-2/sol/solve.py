from nclib import Netcat

import os
os.system("python ../src/build_strat.py build_ext --inplace")

from strat import *

def ru(nc, b):
    """Receive until"""

    r = b""
    while b not in r:
        r += nc.recv(1)
    #print(r.decode())
    return r

def init_game():

    nc = Netcat(("192.168.139.128", 5555))
    _ = ru(nc, b">>> ")
    nc.send_line(b"yes")

    return nc


def get_game_state(nc):

    cnt = ru(nc, b">>> ")
    def get_char_aft(pref): return cnt[cnt.index(pref)+len(pref)]
    return (
        int(chr(get_char_aft(b"A:"))),  # Number of feathers
        int(chr(get_char_aft(b"B:"))),  # Number of feathers
        int(chr(get_char_aft(b"C:"))),  # Number of feathers
        int(chr(get_char_aft(b"D:"))),  # Number of feathers
        int(b"Your turn!" not in cnt)  # Player's turn (You are player 0)
    )


def send_game_move(nc, move):

    num, (a,b) = move
    nc.send_line(num.encode())
    ru(nc, b">>> ")
    nc.send_line(f"{a}-{b}".encode())
    ru(nc, b"; ")


def unreduce_state(state1, rstate2):

    a, b, c, d, turn = state1
    x, y, z, w, t = rstate2

    if turn == 0:  # Player 0 moved

        if a+b == x+y and c+d != z+w:  # Player 0 attacked player 1

            state2 = rstate2
            if a != x:
                state2 = (*state2[:2][::-1], *state2[2:4], state2[-1])
            if c != z and d != w:
                state2 = (*state2[:2], *state2[2:4][::-1], state2[-1])
            x, y, z, w, t = state2

            if c != z:  # z got attacked
                if z == 0:  # killed
                    if c+a >= NHANDS:
                        return state2, ("1", ("A", "C"))
                    if c+b >= NHANDS:
                        return state2, ("1", ("B", "C"))
                    raise Exception(f"Huh {(state1, rstate2)}")
                diff = z-c
                if diff == a:
                    return state2, ("1", ("A", "C"))
                if diff == b:
                    return state2, ("1", ("B", "C"))
                raise Exception(f"Huh {(state1, rstate2)}")
            # w got attacked
            if w == 0:
                if d+a >= NHANDS:
                    return state2, ("1", ("A", "D"))
                if d+b >= NHANDS:
                    return state2, ("1", ("B", "D"))
                raise Exception(f"Huh {(state1, rstate2)}")
            diff = w-d
            if diff == a:
                return state2, ("1", ("A", "D"))
            if diff == b:
                return state2, ("1", ("B", "D"))
            raise Exception(f"Huh {(state1, rstate2)}")

        if a+b == x+y and c+d == z+w:  # Player 0 split
            state2 = rstate2
            if c != z:
                state2 = (*state2[:2], *state2[2:4][::-1], state2[-1])
            x, y, z, w, t = state2
            return state2, ("2", (str(x), str(y)))

        # From here, a+b != x+y, meaning an attack on themselves
        assert c+d == z+w

        state2 = rstate2
        if c != z:
            state2 = (*state2[:2], *state2[2:4][::-1], state2[-1])
        if a != x and b != y:
            state2 = (*state2[:2][::-1], *state2[2:4], state2[-1])
        x, y, z, w, t = state2

        if a != x:  # a got attacked
            if x == 0:
                if a+b >= NHANDS:
                    return state2, ("1", ("B", "A"))
                raise Exception(f"Huh {(state1, rstate2)}")
            if x-a == b:
                return state2, ("1", ("B", "A"))
            raise Exception(f"Huh {(state1, rstate2)}")

        if b != y:  # b got attacked
            if y == 0:
                if a+b >= NHANDS:
                    return state2, ("1", ("A", "B"))
                raise Exception("Huh")
            if y-b == a:
                return state2, ("1", ("A", "B"))
            raise Exception(f"Huh {(state1, rstate2)}")

        raise Exception(f"Huh {(state1, rstate2)}")

    ns1 = (c, d, a, b, 1 ^ turn)
    nrs2 = (z, w, x, y, 1 ^ t)
    ns2, desc = unreduce_state(ns1, nrs2)

    x, y, z, w, t = ns2
    state2 = (z, w, x, y, 1 ^ t)
    n, (i0, i1) = desc
    nm = {"A": "C", "B": "D", "C": "A", "D": "B"}
    i0 = nm[i0] if i0 in nm else i0
    i1 = nm[i1] if i1 in nm else i1
    return state2, (n, (i0, i1))


def reduce_state(state):
    return (*sorted(state[:2]), *sorted(state[2:4]), state[-1])


def is_won(state):
    return sum(state[2:4]) == 0

nc = init_game()

visited = set()
while True:

    state = get_game_state(nc)
    print(f"Pat: {reduce_state(state)}")

    rstate = reduce_state(state)
    visited.add(rstate)

    jules_confidence, rstate = evaluate_possible(rstate, 9, visited)
    visited.add(rstate)
    state, move = unreduce_state(state, rstate)
    print(f"Jul: {reduce_state(state)} {move}")
    print("Jule's Confidence: ", jules_confidence/INF)

    send_game_move(nc, move)

    if is_won(state):
        print("We win!!!")
        break

cnt = ru(nc, b"End.")
print(cnt.decode())

# Pat: (1, 1, 1, 1, 0)
# Jul: (1, 2, 1, 1, 1) ('1', ('A', 'B'))
# Jule's Confidence:  0.07000000000000002
# Pat: (1, 2, 1, 2, 0)
# Jul: (2, 3, 1, 2, 1) ('1', ('B', 'A'))
# Jule's Confidence:  0.08235942050080036
# Pat: (2, 3, 2, 3, 0)
# Jul: (2, 3, 2, 3, 1) ('2', ('2', '3'))
# Jule's Confidence:  0.07000000000000002
# Pat: (2, 3, 3, 5, 0)
# Jul: (2, 3, 0, 3, 1) ('1', ('A', 'D'))
# Jule's Confidence:  0.1114579285714286
# Pat: (2, 3, 1, 2, 0)
# Jul: (1, 4, 1, 2, 1) ('2', ('1', '4'))
# Jule's Confidence:  0.07422300636093018
# Pat: (1, 6, 1, 2, 0)
# Jul: (3, 4, 1, 2, 1) ('2', ('3', '4'))
# Jule's Confidence:  0.05571428571428572
# Pat: (3, 4, 1, 2, 0)
# Jul: (3, 4, 1, 6, 1) ('1', ('B', 'D'))
# Jule's Confidence:  0.15000000000000002
# Pat: (3, 4, 2, 5, 0)
# Jul: (3, 4, 0, 2, 1) ('1', ('A', 'D'))
# Jule's Confidence:  0.26881364534550006
# Pat: (3, 4, 1, 1, 0)
# Jul: (3, 4, 1, 1, 1) ('2', ('3', '4'))
# Jule's Confidence:  0.7
# Pat: (3, 5, 1, 1, 0)
# Jul: (3, 5, 1, 4, 1) ('1', ('A', 'D'))
# Jule's Confidence:  0.746709285714286
# Pat: (0, 3, 1, 4, 0)
# Jul: (0, 3, 0, 1, 1) ('1', ('A', 'D'))
# Jule's Confidence:  1.0
# Pat: (0, 4, 0, 1, 0)
# Jul: (1, 3, 0, 1, 1) ('2', ('1', '3'))
# Jule's Confidence:  1.0
# Pat: (1, 4, 0, 1, 0)
# Jul: (1, 4, 0, 1, 1) ('2', ('1', '4'))
# Jule's Confidence:  1.0
# Pat: (1, 5, 0, 1, 0)
# Jul: (3, 3, 0, 1, 1) ('2', ('3', '3'))
# Jule's Confidence:  1.0
# Pat: (3, 4, 0, 1, 0)
# Jul: (2, 5, 0, 1, 1) ('2', ('2', '5'))
# Jule's Confidence:  1.0
# Pat: (3, 5, 0, 1, 0)
# Jul: (0, 5, 0, 1, 1) ('1', ('B', 'A'))
# Jule's Confidence:  1.0
# Pat: (0, 6, 0, 1, 0)
# Jul: (0, 6, 0, 0, 1) ('1', ('B', 'C'))
# Jule's Confidence:  1.0
# We win!!!
# ...
# +-------+-----------------------------------------+
# | /\ /\ | You: ^-^                                |
# |((-v-))|                                         |
# |():::()|                            { You win! } |
# +--VVV--+-----------------------------------------+
#    +...............+     :     +...............+
#    :               :     :     :    /    /    /:
#    :               :     :     : ,=/\ ,=/\ ,=/\:
#    :               : A:0 : B:6 :,=/\/,=/\/,=/\/:
#    :               :     :     :(,\/ (,\/ (,\/ :
#    :               :     :     :,=/\/,=/\/,=/\/:
#    :               :     :     :(,\/ (,\/ (,\/ :
#    +...............+     :     +...............+
#  .................................................
#    +...............+     :     +...............+
#    :               :     :     :               :
#    :               :     :     :               :
#    :               :     :     :               :
#    :               : C:0 : D:0 :               :
#    :               :     :     :               :
#    :               :     :     :               :
#    +...............+     :     +...............+
# +-------+-----------------------------------------+
# | /\_/\ | Pat: Nice! CTFSG{Ch0pst!ck5_m4STeR!11!_ |
# |( o.o )| aim48djam3}                             |
# | > ^ < |                          { They lost! } |
# +-------+-----------------------------------------+
# 
# End.