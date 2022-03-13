import pickle
import random
from collections import Counter
from math import log

import sys
sys.setrecursionlimit(10000)

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

def gen_possible(state, _cache={}):
    
    win, player = is_win(state)
    if win: return set()
    if state in _cache: return _cache[state].copy()
    
    a,b,c,d,turn = state
    ret = []
    if turn == 0:
        n = a+b
        ret += [(i,n-i,c,d,1) for i in range(1,NHANDS) if 0<n-i<NHANDS and 0<i<NHANDS and i<=n-i]
        if c!=0: ret += [(a,b,*sorted((add_move(c,j),d)),1) for j in (a,b) if j!=0]
        if d!=0: ret += [(a,b,*sorted((c,add_move(d,j))),1) for j in (a,b) if j!=0]
        if a!=0: ret += [(*sorted((j,add_move(b,a))),c,d,1) for j in (a,b)]
    else:
        n = c+d
        ret += [(a,b,i,n-i,0) for i in range(1,NHANDS) if 0<n-i<NHANDS and 0<i<NHANDS and i<=n-i]
        if a!=0: ret += [(*sorted((add_move(a,j),b)),c,d,0) for j in (c,d) if j != 0]
        if b!=0: ret += [(*sorted((a,add_move(b,j))),c,d,0) for j in (c,d) if j != 0]
        if c!=0: ret += [(a,b,*sorted((j,add_move(c,d))),0) for j in (c,d)]
        
    ret = set(ret)
    _cache[state] = ret
    return ret.copy()

def gen_win_states(player):
    
    if player == 0:
        return [
            (i,j,0,0,1) for i in range(NHANDS) for j in range(i,NHANDS)
        ][1:]
    
    return [
        (0,0,i,j,0) for i in range(NHANDS) for j in range(i,NHANDS)
    ][1:]

INF = 1.1
def gen_lookup_scores(player, _state=None, _cache=None, _visited=None):
    
    if _state == None: _state = init_state
    if _cache == None: _cache = {}
    if _visited == None: _visited = set()
    
    s = _state; t = s[-1]
    
    w,p = is_win(s)
    if w:
        sc = [-1,1][p == player] * INF
        _cache[s] = sc
        return sc, _cache
    if s in _cache:
        return _cache[s], _cache
    if s in _visited:
        return 0, _cache # Idk
    _visited = _visited.copy()
    _visited.add(s)
    
    ns = gen_possible(s)

    if t==player:
        ms = 0
        for n in ns:
            sc, _cache = gen_lookup_scores(player, n, _cache, _visited)
            ms = max(ms, sc)  
        _cache[s] = ms
        return ms, _cache
    
    ms = []
    for n in ns:
        sc, _cache = gen_lookup_scores(player, n, _cache, _visited)
        ms += [sc]

    midx = ms.index(min(ms))
    w = .7
    sc = (1-w)*(sum(ms) - ms[midx]) + w*ms[midx]
    _cache[s] = sc/len(ms)
    return sc, _cache

p_lookup = [
    gen_lookup_scores(0)[1],
    gen_lookup_scores(1)[1]
]
p0_lookup, p1_lookup = tuple(p_lookup)
def alphabeta(player, state, depth, visited, _a=-INF, _b=INF):
    
    # `visited` doesn't contains `state`
    
    s = state; t=s[-1];
    visited = visited.copy(); visited.add(s)
    
    w,p = is_win(s)
    if w:
        return [INF,-INF][p!=player]
    if depth == 0:
        return p_lookup[t][s] * [1,-1][t!=player]
    
    ns = sorted([*(gen_possible(s) - visited)],
               key=lambda x: p_lookup[1^t][x])
    
    if player==t: # max tiem
        val = -INF
        for n in ns:
            val = max(val, alphabeta(player, n, depth-1, visited, _a, _b))
            if val >= _b:
                break
            _a = max(_a, val)
        return val
    
    val = INF
    for n in ns:
        val = min(val, alphabeta(player, n, depth-1, visited, _a, _b))
        if val <= _a:
            break
        _b = min(_b, val)
    return val

def evaluate_possible(state, depth, visited):
    
    # `visited` doesn't contains `state`
    
    visited = visited.copy(); visited.add(state)
    t = state[-1]
    ns = sorted([*(gen_possible(state) - visited)],
               key=lambda x: p_lookup[1^t][x])
    alpha = -INF
    vs = []
    for n in ns:
        v = alphabeta(t, n, depth, visited, alpha)
        vs.append(v)
        alpha = max(v, alpha)
        if alpha == INF:
            return alpha, n
    
    idx = vs.index(max(vs))
    return vs[idx], ns[idx]