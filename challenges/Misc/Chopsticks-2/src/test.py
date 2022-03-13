from strat import *

s = init_state
v = set()
while True:

    v.add(s)
    sc,s = evaluate_possible(s, 11, v)
    print(s,sc/INF)
    w,p = is_win(s)
    if w:break

    v.add(s)
    sc,s = evaluate_possible(s, 10, v)
    print(s,sc/INF)
    w,p = is_win(s)
    if w:break

print(f"Player {p} won!")
