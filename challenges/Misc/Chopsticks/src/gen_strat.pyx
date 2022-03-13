import pickle
import random
from collections import Counter

# state = (a,b,c,d,turn)
init_state = (1,1,1,1,0)
NHANDS = 7

def is_win(state):
    a,b,c,d,turn = state
    if a+b == 0: return True, 1
    if c+d == 0: return True, 0
    return False, None

def add_move(a,b):
    x = a+b
    if x >= NHANDS: return 0
    return x
    #return (a+b)%10

def gen_possible(state, _cache={}):
    
    win, player = is_win(state)
    if win: return []
    if state in _cache: return _cache[state][:]
    
    a,b,c,d,turn = state
    ret = []
    if turn == 0:
        n = a+b
        if a!=0: ret += [(i,n-i,c,d,1) for i in range(1,NHANDS) if 1<n-i<NHANDS and 1<i<NHANDS and i<=n-i]
        if c!=0: ret += [(a,b,*sorted((add_move(c,j),d)),1) for j in (a,b) if j!=0]
        if d!=0: ret += [(a,b,*sorted((c,add_move(d,j))),1) for j in (a,b) if j!=0]
        if a!=0: ret += [(*sorted((j,add_move(b,a))),c,d,1) for j in (a,b)]
    else:
        n = c+d
        if c!=0: ret += [(a,b,i,n-i,0) for i in range(1,NHANDS) if 1<n-i<NHANDS and 1<i<NHANDS and i<=n-i]
        if a!=0: ret += [(*sorted((add_move(a,j),b)),c,d,0) for j in (c,d) if j != 0]
        if b!=0: ret += [(*sorted((a,add_move(b,j))),c,d,0) for j in (c,d) if j != 0]
        if c!=0: ret += [(a,b,*sorted((j,add_move(c,d))),0) for j in (c,d)]
        
    ret = [*set(ret)]
    _cache[state] = ret
    return ret[:]

def get_winning_strategy(player, dbg=False, _state=None, _visited=None, _cache=None, _d=0):
    
    if _state == None:
        _state = init_state
    if _visited == None:
        _visited = set([_state])
    if _cache == None:
        _cache = {}

    turn = _state[-1]
    if dbg: print("  "*_d + str(turn) + ": " + str(_state))
        
    w,p = is_win(_state)
    if w:
        w = p==player
        if dbg: print("  "*_d + [">_<", "^-^"][w])
        if w: 
            return True, _state, set([_state])
        return False, None, None
    
    ns = [*(set(gen_possible(_state)) - _visited)]
    if len(ns) == 0:
        return 0, None, None

    if _state in _cache:
        ret, v, d = _cache[_state]
        if d.isdisjoint(_visited) and \
            v.issubset(_visited):
            return 1, ret, d
    
    if turn == player: # Player can pick!
        
        for s in ns:
            nv = _visited.copy(); nv.add(s)
            w, strat, d = get_winning_strategy(player, dbg, s, nv, _cache, _d+1)
            if not w: continue
            dep = d.copy(); dep.add(s)
            _cache[_state] = (s, strat), _visited, dep
            return True, (s, strat), dep
        return False, None, None
    
    # It's not player's turn...
    strategy = {}
    dep = set()
    for s in ns:
        
        nv = _visited.copy(); nv.add(s)
        w, strat, d = get_winning_strategy(player, dbg, s, nv, _cache, _d+1)
        if not w:
            return False, None, None
        strategy[s] = strat
        dep = dep | d    
        
    _cache[_state] = strategy, _visited, dep
    return True, strategy, dep

def get_best_losing_strategy(player, dbg=False, _state=None, _visited=None, _cache=None, _d=0):
    
    if _state == None:
        _state = init_state
    if _visited == None:
        _visited = set([_state])
    if _cache == None:
        _cache = {}

    turn = _state[-1]
    if dbg: print("  "*_d + str(turn) + ": " + str(_state))
        
    w,p = is_win(_state)
    if w:
        w = p==player
        if dbg: print("  "*_d + [">_<", "^-^"][w])
        if w: 
            return 1, _state, set([_state])
        return 0, None, None
    
    ns = [*(set(gen_possible(_state)) - _visited)]
    if len(ns) == 0:
        return turn != player, _state, set([_state])

    if _state in _cache:
        ret, v, d = _cache[_state]
        if _visited.isdisjoint(d) and \
            v.issubset(_visited):
            return 1, ret, d

    if turn == player: # Player can pick!
        
        scores = []
        strats = []
        for s in ns:
            nv = _visited.copy(); nv.add(s)
            w, strat, d = get_best_losing_strategy(player, dbg, s, nv, _cache, _d+1)
            scores.append(w); strats.append(strat)
            if w == 1:
                dep = d.copy(); dep.add(s)
                _cache[_state] = (s,strat), _visited, dep
                return 1, (s,strat), dep
        
        bs = max(scores)
        idx = scores.index(bs)
        return bs, (ns[idx], strats[idx]), None
    
    # It's not player's turn...
    strategy = {}
    score = 0
    nwin = 0
    dep = set()
    for s in ns:
        
        nv = _visited.copy(); nv.add(s)
        w, strat, d = get_best_losing_strategy(player, dbg, s, nv, _cache, _d+1)
        score += w
        strategy[s] = strat
        
        if w == 1:
            nwin += 1
            dep = dep | d
        
    if nwin==len(ns):
        _cache[_state] = strategy, _visited, dep
        return 1, strategy, dep
    
    return score/len(ns), strategy, dep

def play_game(strat0, strat1):
    
    s = init_state
    turn = s[-1]
    assert turn == 0
    visited = set([s])
    strats = [strat0, strat1]
    
    nturns = 0
    while True:
        
        win,wp = is_win(s)
        if win: return wp, nturns
        
        moves = set(gen_possible(s)) - visited
        if len(moves) == 0:
            return -1, nturns
        
        strat = strats[turn]
        s = strat(s, visited); visited.add(s)
        #print(f"{turn}: {s}")
        assert s in moves
        
        turn ^= 1; nturns += 1

def get_perfect_player_strat(perfect_player):
    
    if perfect_player == 0:
        _curr_strat0 = [{init_state: pickle.load(open("p0_perfect.strat", "rb"))}]
    else:
        _curr_strat1 = [pickle.load(open("p1_perfect.strat", "rb"))]

    def turn0(state, visited):
        
        assert state[-1] == 0
        assert state in _curr_strat0[0], (state, _curr_strat0[0].keys())
        ret, _curr_strat0[0] = \
            _curr_strat0[0][state]
        
        assert ret not in visited
        return ret

    def turn1(state, visited):
        
        assert state[-1] == 1
        assert state in _curr_strat1[0], (state, _curr_strat1[0].keys())
        ret, _curr_strat1[0] = \
            _curr_strat1[0][state]
        
        assert ret not in visited
        return ret

    return [turn0, turn1][perfect_player]

def play_random_game(perfect_player):
    
    strats = [None, None]
    strats[perfect_player] = get_perfect_player_strat(perfect_player)
    strats[1^perfect_player] = \
        lambda s,v: (lambda ns: random.choice(ns) if len(ns) else None)([*set(gen_possible(s)) - v])
    
    return play_game(*strats)

def play_perfect_game():

    return play_game(
        get_perfect_player_strat(0), 
        get_perfect_player_strat(1))

def verify_perfect(perfect_player):

    ngames = 10000

    print(f"Testing Perfect Player {perfect_player}")
    wins, nturns = [],[]
    for _ in range(ngames):
        w,t = play_random_game(perfect_player)
        wins.append(w); nturns.append(t)

    assert any(w==perfect_player for w in wins), \
        f"Player {perfect_player} did not win all random games {Counter(wins)}"
    print(f"Average game length: {sum(nturns)/len(nturns)}")

def verify_losing(losing_player, expected_win_rate):

    ngames = 10000

    print(f"Testing Losing Player {losing_player}")
    wins, nturns = [],[]
    for _ in range(ngames):
        w,t = play_random_game(losing_player)
        wins.append(w); nturns.append(t)

    nwins = sum(w==losing_player for w in wins)
    assert nwins < expected_win_rate*ngames*10, \
        f"Player {losing_player} ain't good enough {Counter(wins)}"
    print(f"Average game length: {sum(nturns)/len(nturns)}")
    print(f"Win rate: {nwins/len(wins)}")
    print(f"Average game length: {sum(nturns)/len(nturns)}")

def main():

    perfect_player = 0
    losing_player = 1^perfect_player

    #b,strat,_ = get_winning_strategy(perfect_player)
    #assert b, "Player {perfect_player} has no winning strategy!"
    #pickle.dump(strat, open(f"~p{perfect_player}_perfect.strat", "wb"))
    verify_perfect(perfect_player)

    #b,strat,_ = get_best_losing_strategy(losing_player)
    b = 0.9999338624338625
    print(f"Player {losing_player} expected win rate: {b}")
    print(f"Player {losing_player} loses every {int(1/(1-b) + .5)} games to a random player")
    #pickle.dump(strat, open(f"~p{losing_player}_perfect.strat", "wb"))
    verify_losing(losing_player, b)

    print("Playing perfect game")
    w,t = play_perfect_game()
    assert w == perfect_player, f"Player {perfect_player} lost to Player {losing_player}!"
    print(f"Perfect game length: {t}")

if __name__ == "__main__": main()