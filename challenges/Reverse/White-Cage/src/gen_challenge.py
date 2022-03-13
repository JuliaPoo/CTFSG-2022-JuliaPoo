from heapq import nsmallest
from fin_nums import *

MESS2 = 127
MESS = 2022

S = lambda x:lambda y:lambda z:x(z)(y(z))
K = lambda x:lambda y:x
I = lambda x:x
A = lambda n:(n-MESS)%MESS2
B = lambda n:(n+MESS)%MESS2
Z = lambda f:(lambda g:f(g(g)))(lambda g:f(lambda y:g(g)(y)))

mapping = [(-MESS*i)%MESS2 for i in range(MESS2)]

_S = "lambda x:lambda y:lambda z:x(z)(y(z))"
_K = "lambda x:lambda y:x"
_I = "lambda x:x"
_B = f"lambda n:(n+{MESS})%{MESS2}"
_Z = "lambda f:(lambda g:f(g(g)))(lambda g:f(lambda y: g(g)(y)))"
ATOMS = {
    "S": _S, "K": _K, "I": _I, "B": _B, "Z": _Z
}

zcom = "[f:[g:f(g(g))]([g:f([y:g(g)(y)])])]"

int_inc = "[n:[f:[x:f(n(f)(x))]]]"

bool_true = "[x:[y:x]]"
bool_false = "[x:[y:y]]"

arr_int_pair = "[x:[y:[f:f(x)(y)]]]"
arr_int_left = f"[p:p({bool_true})]"
arr_int_right = f"[p:p({bool_false})]"
arr_int_empty = f"{arr_int_pair}({bool_true})({bool_true})"
arr_int_is_empty = arr_int_left
arr_int_push_front = f"[l:[x:{arr_int_pair}({bool_false})({arr_int_pair}(x)(l))]]"
arr_int_first = f"[l:{arr_int_left}({arr_int_right}(l))]"
arr_int_rest = f"[l:{arr_int_right}({arr_int_right}(l))]"

func_to_bool:str = "S(S(I)(K(1)))(K(0))"

arr_int_eq = "Z(lambda f:lambda a:lambda b:(lambda c:lambda d:lambda i:lambda g:c(a)(c(b)(K)(K(I)))(g(d(a))(d(b))(lambda x:f(i(a))(i(b))(x))(K(I))))(S(I)(K(K)))(S(K(S(I)(K(K))))(S(I)(K(K(I)))))(S(K(S(I)(K(K(I)))))(S(I)(K(K(I)))))(S(K(S(S(K(S(K(S(S(S)(K(S(K(S(S)(K(K))))(S(K(K))(S(K(S))(S(K(S(I)))(K)))))))(K(S(K(S(K(S(K(S(S)(K(K))))(S(K(K))(S(S)(K(K(I)))))))))(S(K(S(S)(K(S(K(S(K(S(K(S(I)))(K)))))(S(K(S(I)))(K))))))(K))))))(K))))(K(K(I)))))(S(K(S(S(K(S))(S(K(S(S)(K(S(K(S(S)(K(S(K(K))(S(K(S))(K))))))(S(K(K))(S(K(S(S)))(K)))))))(S(K(S(K(S))))(S(K(S(S)(K(S(K(S(S)(K(S(K(K))(S(K(S))(K))))))(S(K(K))(S(K(S(S)))(S(K(K))(S(K(S(S)(K(K))))(S(K(K))(S))))))))))(S(K(K))(S(K(S))(S(K(K))(S(K(S(K(S(K(S(S)(K(S(S(S))(K)(S)))))(K)))))(S(K(S(S)(K(K))))(S(K(K))(S(K(S))(S(K(S))(S(K(K))(S(K(S(K(I))))(S(K(S))(S(K(K))(S(K(S(S)))(S(K(K))(K)))))))))))))))))))))(S(K(S(K(K))))(S(K(S(S)(K(S(K(S(I)))(S(K(K))(K))))))(S(K(K))(S(K(S(S)))(S(K(K))(K)))))))(K)))"

list_to_func = "Z(lambda y:lambda z:S(K(S(K(S(K(S(S)(K(K))))(S(K(K))(S(K(S))(S(K(S(I)))(K))))(K(I))))))(S(K(S(S)(K(S(K(K))(S(K(S))(S(K(S(I)))(K)))))))(S(K(K))(S(K(S(S(S)(K(K)))))(K))))(lambda x:y(z[1:])(x))(Z(lambda y:lambda m:S(S(K(S))(K))(y(B(m))) if B(m) else I)(z[0])) if z else S(K(S(S)(K(K))))(S(K(K))(S(K(S))(S(K(S(I)))(K))))(K)(K))"

def gen_fstr(b:bytes) -> str:

    from collections import Counter
    b = [mapping.index(c) for c in b]
    rep = {a:b for a,b in Counter(b).items() if b>100}
    gen_label = lambda a: f"fstr_label_{a}"
    ns = "%%%"
    for a in rep.keys():
        ns = f"[{gen_label(a)}:({ns})]({nums[a]})"

    s = arr_int_empty
    for c in b[::-1]:
        s = f"a({s})({gen_label(c) if c in rep else nums[c]})"
    s = f"[a:{s}]({arr_int_push_front})"
    s = ns.replace("%%%", s)
    return str2str_compile(s)

def gen_verify(flag:bytes) -> str:

    fflag = gen_fstr(flag)

    # f"lambda s: {func_to_bool}({arr_int_eq}({list_to_func}(s))({fflag}))"
    # S(K(A))(S(K(S(B)(K(D))))(C))
    ver = f"S(K({func_to_bool}))(S(K(S({arr_int_eq})(K({fflag}))))({list_to_func}))"
    ver = f"(lambda {','.join(ATOMS.keys())}: {ver})({','.join(ATOMS.values())})"

    rename = dict(zip("SKIBZ", "hewro"))
    ver = "".join([rename[c] if c in rename else c for c in ver])

    return ver

def gen_dist(flag:bytes) -> str:

    dist = open("template").read()
    dist = dist.replace("!A!", gen_verify(flag))
    return dist

flag = b"CTFSG{I_respect_Ur_Cunning_BUT_no}"
#fflag = eval(gen_fstr(flag))

print(gen_fstr(flag))

verify = eval(gen_verify(flag))
res = verify(flag)
assert res, res
assert not verify(flag[:-10])

open("build/build.py", "w").write(gen_dist(flag))