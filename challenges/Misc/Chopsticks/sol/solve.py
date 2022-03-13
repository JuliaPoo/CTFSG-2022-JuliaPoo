from nclib import Netcat
import pickle
import re

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
                    if c+a >= 7:
                        return state2, ("1", ("A", "C"))
                    if c+b >= 7:
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
                if d+a >= 7:
                    return state2, ("1", ("A", "D"))
                if d+b >= 7:
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
                if a+b >= 7:
                    return state2, ("1", ("B", "A"))
                raise Exception(f"Huh {(state1, rstate2)}")
            if x-a == b:
                return state2, ("1", ("B", "A"))
            raise Exception(f"Huh {(state1, rstate2)}")

        if b != y:  # b got attacked
            if y == 0:
                if a+b >= 7:
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


def get_perfect_player_strat():
    
    _curr_strat0 = [{(1,1,1,1,0): pickle.load(open("p0_perfect.strat", "rb"))}]
    def turn0(state, visited):
        
        assert state[-1] == 0
        assert state in _curr_strat0[0], (state, _curr_strat0[0].keys())
        ret, _curr_strat0[0] = \
            _curr_strat0[0][state]
        
        assert ret not in visited
        return ret

    return turn0

def is_won(state):
    return sum(state[2:4]) == 0


nc = init_game()
strat = get_perfect_player_strat()

while True:

    state = get_game_state(nc)
    print(f"Pat: {state}")

    rstate = reduce_state(state)
    visited = set([rstate])

    rstate = strat(rstate, visited)
    visited.add(rstate)
    state, move = unreduce_state(state, rstate)
    print(f"You: {state} {move}")

    send_game_move(nc, move)

    if is_won(state):
        print("We win!!!")
        break

cnt = ru(nc, b"End.")
print(cnt.decode())