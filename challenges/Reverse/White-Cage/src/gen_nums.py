from typing import Tuple, List, Callable, Union
import pickle, os
import ski

Cfun = Tuple[str, Callable]
Cnum = Tuple[str, int]

NUMS_CACHE = "_cache/nums.pickle"

NS: Tuple[Cnum] = [
    ("[f:[x:%sx%s]]"%("f("*i, ")"*i), i)
        for i in range(0x100)
]
for i in range(0x100):
    globals()["N%d"%i] = NS[i]

FS1: Tuple[Cfun] = (
    ("[n:[f:[x:f(n(f)(x))]]]", lambda n: n+1),
    ("[n:[f:[x:n([g:[y:y(g(f))]])([y:x])([y:y])]]]", lambda n: max(n-1, 0)),
)

FS2: Tuple[Cfun] = (
    ("[a:[b:b([n:[f:[x:f(n(f)(x))]]])(a)]]", lambda a,b: a+b),
    ("[a:[b:b([n:[f:[x:n([g:[y:y(g(f))]])([y:x])([y:y])]]])(a)]]", lambda a,b: max(a-b, 0)),
    ("[a:[b:b([y:[a:[b:b([n:[f:[x:f(n(f)(x))]]])(a)]](y)(a)])([f:[x:x]])]]", lambda a,b: a*b),
    ("[a:[b:[n:[f:[x:f(n(f)(x))]]](b)(a)]]", lambda a,b: a**(b+1)),
)
INC,DEC = FS1
ADD,SUB,MUL,POW = FS2

def str2str_compile(code: str) -> str:
    return str(ski.compile_SKI(ski.code_to_ski(code)))

def score(code: Union[Cfun, Cnum]) -> int:
    return len(str2str_compile(code[0]))

def apply(func: Cfun, *num: Cnum) -> Cnum:
    nf, nc = \
        tuple(x for x,_ in num), \
        tuple(y for _,y in num)
    ff, fc = func
    argstr = "".join("(%s)"%n for n in nf)
    return \
        f"(%s)%s"%(ff, argstr), fc(*nc)

def check(num: Cnum) -> None:

    S = lambda x: lambda y: lambda z: (x(z))(y(z))
    K = lambda x: lambda y: x
    I = lambda x: x

    nf, nc = num
    f = eval(str2str_compile(nf))
    n = f(lambda n: n+1)(0)
    assert n == nc, \
        f"Missmatch! {n}!={nc}"

def toInt(num: Cnum) -> int:
    return num[1]

def search() -> List[Cnum]:

    if os.path.isfile(NUMS_CACHE):
        nums = pickle.load(open(NUMS_CACHE, 'rb'))
    else:
        nums = []
        for i,n in enumerate(NS):
            print(i, end="\r")
            nums.append((n, score(n)))
        pickle.dump(nums, open(NUMS_CACHE, 'wb'))

    def _round(nums, til):

        fp = NUMS_CACHE + ".%d"%r
        if os.path.isfile(fp):
            nums = pickle.load(open(fp, 'rb'))
            return

        for nn in nums[:til]:

            n, _ = nn
            print("1: %d    "%toInt(n), end="\r")
            
            for f in FS1:
                m = apply(f, n)
                mi = toInt(m)
                if mi > 0xff or mi < 0:
                    if type(mi) != int: 
                        print(f"TypeError! {m} ==> {mi}")
                    continue
                if (s := score(m)) < nums[mi][1]:
                    nums[mi] = (m, s)

        for aa in nums[:til]:
            for bb in nums[:til]:

                a, _ = aa
                b, _ = bb
                print("2: %d:%d    "%(toInt(a),toInt(b)), end="\r")

                for f in FS2:
                    m = apply(f, a, b)
                    mi = toInt(m)
                    if mi > 0xff or mi < 0:
                        if type(mi) != int: 
                            print(f"TypeError! {m} ==> {mi}")
                        continue
                    if (s := score(m)) < nums[mi][1]:
                        nums[mi] = (m, s)

        pickle.dump(nums, open(fp, 'wb'))

    r = 0
    for _ in range(32):
        print("Round %d "%r)
        _round(nums, 32)
        r += 1
    for _ in range(10): # Converged! Early stop
        print("Round %d "%r)
        _round(nums, 64)
        r += 1
    for _ in range(13):
        print("Round %d "%r)
        _round(nums, 0x100) # Converged! Early stop
        r += 1
    
            
if __name__ == "__main__":
    search()
