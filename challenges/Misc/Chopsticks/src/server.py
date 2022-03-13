from strat import *

import numpy as np
import time

import os, pathlib
os.chdir(pathlib.Path(__file__).parent)
import sys
sys.stderr = object

game_banner = r"""
 __ .            ,     .     
/  `|_  _ ._  __-+-* _.;_/ __
\__.[ )(_)[_)_)  | |(_.| \_) 
----------|---------------------------                  
            _,'|             _.-''``-...___..--';)
           /  \'.      __..-' ,      ,--...--'''
          <-    .`--'''       `     /'
           `-';'               ;   ; ;     .---+
     __...--''     ___...--_..'  .;.'         /
 .  (,__....----'''       (,..--''          ./.
  '------------------------------------------------
                         ascii art: www.asciiart.eu

+-------------------------------------------------+
| Rules:                                          |
| This game is similar to the game Chopsticks:    |
|   en.wikipedia.org/wiki/Chopsticks_(hand_game)  |
|                                                 |
| * Each person starts with two boxes, with 1     |
|   feather.                                      |
| * If any box has at least 1 feather, it is live |
| * If any box has no feathers, it is dead        |
| * If any box contains more than 6 feathers, it  |
|   is dead, and has all its feathers taken out.  |
| * If a player has both boxes dead, the player   |
|   loses.                                        |
| * At each turn, a player can either:            |
|   * Attack: Add all feathers from one box to    |
|     another (their own or another player's)     |
|       * You can't attack to and from a dead box |
|   * Split: Split the feathers between their     |
|     own boxes.                                  |
|       * A split that results in one box having  |
|         one or zero feathers is not allowed.    |
|       * A split can only happen if both boxes   |
|         are live.                               |
| * Loops are disallowed                          |
|   * The game will prevent you from entering a   |
|     state already visited.                      |
+-------------------------------------------------+
"""[1:-1]

p0_banner = r"""
+-------+-----------------------------------------+
| /\_/\ |                                         |
|( o.o )|                                         |
| > ^ < |                                         |
+-------+-----------------------------------------+
"""[1:-1]

p1_banner = r"""
+-------+-----------------------------------------+
| /\ /\ |                                         |
|((-v-))|                                         |
|():::()|                                         |
+--VVV--+-----------------------------------------+
"""[1:-1]

feather = r"""
(`/\ 
`=\/\
 `=\/
    \
"""[1:-1]


def interactive_get_possible_attacks(state):

    a, b, c, d, t = state
    names = "ABCD"
    if t == 0:
        return sorted([
            f"{ja}-{ia}"
            for i, ia in zip([a, b, c, d], names)
            for j, ja in zip([a, b], names[:2])
            if ia != ja and i != 0 and j != 0
        ])
    return sorted([
        f"{ja}-{ia}"
        for i, ia in zip([a, b, c, d], names)
        for j, ja in zip([c, d], names[2:])
        if ia != ja and i != 0 and j != 0
    ])

def interactive_get_possible_split(state):

    split = lambda total: [
            f"{i}-{total-i}" for i in range(1, total) if 1 < i < NHANDS and 1 < total-i < NHANDS]
    a,b,c,d,t = state
    if t == 0:
        if min(a,b) == 0: return []
        return split(a+b)
    if min(c,d) == 0: return []
    return split(c+d)

interactive = {
    "Question": (
        "yes/no",
        ["yes", "no"]
    ),
    "M": (
        "[1:Attack] [2:Split]",
        ["1", "2"]
    ),
    "M_A": (
        "E.g. Type A-C if you wanna attack C with A",
        interactive_get_possible_attacks
    ),
    "M_S": (
        "E.g. Type 1-2 if you wanna split your boxes into 1 and 2",
        interactive_get_possible_split
    )
}


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
                        return state2, ("attacked", ("A", "C"))
                    if c+b >= NHANDS:
                        return state2, ("attacked", ("B", "C"))
                    raise Exception(f"Huh {(state1, rstate2)}")
                diff = z-c
                if diff == a:
                    return state2, ("attacked", ("A", "C"))
                if diff == b:
                    return state2, ("attacked", ("B", "C"))
                raise Exception(f"Huh {(state1, rstate2)}")
            # w got attacked
            if w == 0:
                if d+a >= NHANDS:
                    return state2, ("attacked", ("A", "D"))
                if d+b >= NHANDS:
                    return state2, ("attacked", ("B", "D"))
                raise Exception(f"Huh {(state1, rstate2)}")
            diff = w-d
            if diff == a:
                return state2, ("attacked", ("A", "D"))
            if diff == b:
                return state2, ("attacked", ("B", "D"))
            raise Exception(f"Huh {(state1, rstate2)}")

        if a+b == x+y and c+d == z+w:  # Player 0 split
            state2 = rstate2
            if c != z:
                state2 = (*state2[:2], *state2[2:4][::-1], state2[-1])
            x, y, z, w, t = state2
            return state2, ("split", (str(x), str(y)))

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
                    return state2, ("attacked", ("B", "A"))
                raise Exception(f"Huh {(state1, rstate2)}")
            if x-a == b:
                return state2, ("attacked", ("B", "A"))
            raise Exception(f"Huh {(state1, rstate2)}")

        if b != y:  # b got attacked
            if y == 0:
                if a+b >= NHANDS:
                    return state2, ("attacked", ("A", "B"))
                raise Exception("Huh")
            if y-b == a:
                return state2, ("attacked", ("A", "B"))
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


def desc_to_str(desc):

    desc, (a, b) = desc
    if desc == "split":
        return f"{desc} my boxes {a}-{b}"
    return f"{desc} {b} with {a}"


def to_str(ret):
    return "\n".join(bytes(l).decode() for l in ret)


def art_to_np(art):
    lines = art.split("\n")
    lines = [[*map(ord, l)] for l in lines]
    return np.array(lines, dtype=np.uint8)


def n_feathers(n: int):

    art = art_to_np(feather)
    ay, ax = art.shape

    nr = 2
    c = 2
    h = (nr-1)*c + ay+2
    w = ax*3+2

    ret = np.zeros((h, w), dtype=np.uint8)+ord(" ")
    for i in range(n):
        x, y = i % 3, i//3
        x, y = x*ax, y*c
        ret[1+y:1+y+ay, 1+x:1+x+ax] = art

    ret[0, :] = ord(".")
    ret[-1, :] = ord(".")
    ret[:, 0] = ord(":")
    ret[:, -1] = ord(":")
    ret[0, 0] = ord("+")
    ret[0, -1] = ord("+")
    ret[-1, -1] = ord("+")
    ret[-1, 0] = ord("+")

    #print("\n".join(bytes(l).decode() for l in ret))
    return ret


def gen_player_state(hand, labels):

    padx = 2
    pady = 0

    _a, _b = hand
    a, b = n_feathers(_a), n_feathers(_b)
    ay, ax = a.shape
    ret = np.zeros((ay+pady, 51), dtype=np.uint8)+ord(" ")
    ry, rx = ret.shape
    ret[pady:pady+ay, 1+padx:1+padx+ax] = a
    ret[pady:pady+ay, 50-padx-ax:50-padx] = b
    #ret[:,0] = ord("|")
    #ret[:,-1] = ord("|")
    ret[:, rx//2] = ord(":")
    s = f"{labels[0]}:{_a}"
    ret[ry//2, rx//2-1-len(s):rx//2-1] = [*map(ord, s)]
    s = f"{labels[1]}:{_b}"
    ret[ry//2, rx//2+2:rx//2+2+len(s)] = [*map(ord, s)]

    #print("\n".join(bytes(l).decode() for l in ret))
    return ret


def flip_player_state(hand, labels):

    r = gen_player_state(hand, labels)
    m = {ord(i[0]): ord(i[1]) for i in ["/\\", "\\/", "`,", ",`"]}

    ry, rx = r.shape
    for x in range(rx):
        for y in range(ry):
            c = r[y, x]
            if c in m:
                r[y, x] = m[c]
        r[:, x] = r[:, x][::-1]

    #print("\n".join(bytes(l).decode() for l in r))
    return r


def gen_game_state(state):

    a, b, c, d, t = state

    p0 = flip_player_state((a, b), "AB")
    p1 = gen_player_state((c, d), "CD")

    ret = np.array(
        [list(i) for i in p0] +
        [[*map(ord, " " + "."*49 + " ")]] +
        [list(i) for i in p1], dtype=np.uint8)

    #print("\n".join(bytes(l).decode() for l in ret))
    return ret


def gen_player(player_banner, dialogue, meta):

    ret = art_to_np(player_banner)
    meta = "{ %s }" % meta
    assert len(dialogue) <= 39*2
    assert len(meta) <= 39

    da, db = [ord(i) for i in dialogue[:39]], [ord(i) for i in dialogue[39:]]
    ret[1, 10:10+len(da)] = da
    ret[2, 10:10+len(db)] = db

    ret[3, -2-len(meta):-2] = [ord(i) for i in meta]

    #print("\n".join(bytes(l).decode() for l in ret))
    return ret


def gen_game_screen(state, p0_dialogue, p0_meta, p1_dialogue, p1_meta):

    t = state[-1]
    p0 = gen_player(p0_banner, p0_dialogue, p0_meta)
    p1 = gen_player(p1_banner, p1_dialogue, p1_meta)
    g = gen_game_state(state)

    ret = np.array(
        [*map(list, p1)] +  # Player 1 is on the top!
        [*map(list, g)] +
        [*map(list, p0)]
    )

    #print("\n".join(bytes(l).decode() for l in ret))
    return ret


def print_comment(comment):

    lc = len(comment)
    for i in range(lc//49+1):
        print(" ;"[i == 0] + f" {comment[i*49:i*49+49]}", flush=True)


def game_init():

    print(game_banner, end="\n"*2)
    s = gen_game_screen(init_state,
                        "Pat: Hi! I hear you wanna play w/ me?", "...",
                        "You: ...", "..."
                        )
    print(to_str(s), end="\n"*2, flush=True)

    pr, ps = interactive["Question"]
    print_comment(f"{pr}")
    while (i := input(">>> ")) not in ps:
        print_comment(f"Expected input to be in {ps}")

    # Aww they don't wanna play
    if i == "no":
        s = gen_game_screen(init_state,
                            "Pat: Okay byeee!!", "...",
                            f"You: {i}", "..."
                            )
        print(to_str(s), end="\n"*2, flush=True)
        return False

    # They wanna play!
    s = gen_game_screen(init_state,
                        "Pat: Okay! You'll start first!", "...",
                        f"You: {i}", "Your turn!"
                        )
    print(to_str(s), end="\n"*2, flush=True)

    return True


def game_player_turn(state, visited):

    assert state[-1] == 0  # Player should have started first

    pr, ps = interactive["M"]
    print_comment(f"{pr}")
    while (i := input(">>> ")) not in ps:
        print_comment(f"Expected input to be in {ps}")

    def perform_attack(state, move):
        a, b = move.split("-")
        ai, bi = "ABCD".index(a), "ABCD".index(b)
        nstate = [*state]
        nstate[bi] = add_move(nstate[ai], nstate[bi])
        nstate[-1] ^= 1  # Change turn
        nstate = tuple(nstate)
        return nstate

    def perform_split(state, move):
        a, b = move.split("-")
        ai, bi = int(a), int(b)
        nstate = [*state]
        nstate[0] = ai
        nstate[1] = bi
        nstate[-1] ^= 1  # Change turn
        nstate = tuple(nstate)
        return nstate

    rpos = [*set(gen_possible(reduce_state(state))) - visited]
    rattack_pos = [(i,reduce_state(perform_attack(state, i))) for i in interactive["M_A"][1](state)]
    rsplit_pos = [(i,reduce_state(perform_split(state, i))) for i in interactive["M_S"][1](state)]
    ps_attack = [i for i,ns in rattack_pos if ns in rpos]
    ps_split = [i for i,ns in rsplit_pos if ns in rpos]

    if i == '1':  # Attack
        desc = "attacked"
        pr, ps = interactive["M_A"]
        ps = ps_attack
        if len(ps) == 0:
            print_comment("Nothing to attack! See the rules.")
            return game_player_turn(state, visited)

        print_comment(f"{pr}")
        while (i := input(">>> ")) not in ps:
            print_comment(f"Expected input to be in {ps}")

        nstate = perform_attack(state, i)

        a, b = i.split("-")
        return nstate, (desc, (a, b))

    if i == '2':  # Split

        desc = "split"
        pr, ps = interactive["M_S"]
        ps = ps_split
        if len(ps) == 0:
            print_comment("Nothing to split! See the rules.")
            return game_player_turn(state, visited)

        print_comment(f"{pr}")
        while (i := input(">>> ")) not in ps:
            print_comment(f"Expected input to be in {ps}")

        nstate = perform_split(state, i)

        a, b = i.split("-")
        return nstate, (desc, (a, b))

    raise Exception("Huh")


def game_prog():

    stt = init_state
    pat = get_perfect_player_strat(1)
    vis = set([stt])

    while True:

        w, winner = is_win(stt)
        if w:
            break

        turn = stt[-1]
        rstt = reduce_state(stt)
        rpos = gen_possible(rstt)
        if len(rpos) == 0:
            print_comment("No possible moves!")
            return 1 ^ turn, stt

        if turn == 1:  # Pat's turn

            print_comment("Pat is thinking...")
            time.sleep(3)

            rstt = pat(rstt, vis)
            assert rstt not in vis and rstt in rpos, (rstt, vis, rpos)
            vis.add(rstt)
            # Convert to stt
            stt, desc = unreduce_state(stt, rstt)
            s = gen_game_screen(stt,
                                f"Pat: I've {desc_to_str(desc)}.", "...",
                                "You: ...", "Your turn!"
                                )
            print(to_str(s), end="\n"*2, flush=True)
            #print(f"{turn}: {stt}")

        else:  # Player's turn

            stt, desc = game_player_turn(stt, vis)

            rstt = reduce_state(stt)
            assert rstt not in vis and rstt in rpos, (rstt, vis, rpos)
            vis.add(rstt)
            s = gen_game_screen(stt,
                                "Pat: ...", "Their turn...",
                                f"You: I've {desc_to_str(desc)}.", "..."
                                )
            print(to_str(s), end="\n"*2, flush=True)
            #print(f"{turn}: {stt}")

            #rstt = (lambda ns: random.choice(ns) if len(ns) else None)([*set(gen_possible(rstt)) - vis])
            #assert rstt not in vis and rstt in rpos, (rstt, vis, rpos)
            # vis.add(rstt)
            # Convert to stt
            #stt, desc = unreduce_state(stt, rstt)
            # s = gen_game_screen(stt,
            #    "Pat: ...", "Their turn",
            #    f"You: I've {desc_to_str(desc)}.", "..."
            # )
            #print(to_str(s), end="\n"*2)
            #print(f"{turn}: {stt}")

    return winner, stt


def game_fini(winner, stt):

    from flag import flag

    if winner == 1:
        s = gen_game_screen(stt,
                            "Pat: Ah it's okay, try again next time.", "They win!",
                            f"You: ;-;", "You lost..."
                            )
        print(to_str(s), end="\n"*2, flush=True)
        return False

    s = gen_game_screen(stt,
                        f"Pat: Nice! {flag}", "They lost!",
                        f"You: ^-^", "You win!"
                        )
    print(to_str(s), end="\n"*2, flush=True)

    print("End.", flush=True)
    return True


def game():

    if not game_init():
        return False

    winner, stt = game_prog()

    print_comment("...")
    time.sleep(4)
    return game_fini(winner, stt)


if __name__ == "__main__":
    game()
