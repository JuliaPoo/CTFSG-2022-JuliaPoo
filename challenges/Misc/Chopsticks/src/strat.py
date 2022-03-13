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
