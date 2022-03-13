from fin_nums import *

S = lambda x: lambda y: lambda z: x(z)(y(z))
K = lambda x: lambda y: x
I = lambda x: x
A = lambda n: n+1
B = lambda n: n-1
Z = lambda f: (lambda g: f(g(g)))(lambda g: f(lambda y: g(g)(y)))

ZCOM = lambda f: (lambda g: f(g(g)))(lambda g: f(lambda y: g(g)(y)))

INT_IS_ZERO = lambda n: n(lambda y:BOOL_FALSE)(BOOL_TRUE)
INT_INC = lambda n: lambda f: lambda x: f(n(f)(x))
INT_DEC = lambda n:(lambda f: lambda x: n(lambda g: lambda y: y(g(f)))(lambda y:x)(lambda y:y))
INT_SUB = lambda a: lambda b: b(INT_DEC)(a)
INT_LE = lambda a: lambda b: INT_IS_ZERO(INT_SUB(a)(b))
INT_GE = lambda a: lambda b: INT_IS_ZERO(INT_SUB(b)(a))
INT_EQ = lambda a: lambda b: INT_LE(a)(b)(INT_GE(a)(b))(BOOL_FALSE)

BOOL_TRUE = lambda x: lambda y: x
BOOL_FALSE = lambda x: lambda y: y

ARR_INT_PAIR = lambda x: lambda y: lambda f: f(x)(y)
ARR_INT_LEFT = lambda p: p(BOOL_TRUE)
ARR_INT_RIGHT = lambda p: p(BOOL_FALSE)
ARR_INT_EMPTY = ARR_INT_PAIR(BOOL_TRUE)(BOOL_TRUE)
ARR_INT_IS_EMPTY = ARR_INT_LEFT
ARR_INT_PUSH_FRONT = lambda l: lambda x: ARR_INT_PAIR(BOOL_FALSE)(ARR_INT_PAIR(x)(l))
ARR_INT_FIRST = lambda l: ARR_INT_LEFT(ARR_INT_RIGHT(l))
ARR_INT_REST = lambda l: ARR_INT_RIGHT(ARR_INT_RIGHT(l))
ARR_INT_EQ = ZCOM(lambda f: lambda a: lambda b: ARR_INT_IS_EMPTY(a)(ARR_INT_IS_EMPTY(b)(BOOL_TRUE)(BOOL_FALSE))(INT_EQ(ARR_INT_FIRST(a))(ARR_INT_FIRST(b))(lambda x: f(ARR_INT_REST(a))(ARR_INT_REST(b))(x))(BOOL_FALSE)))
# arr_int_eq = ZCOM(lambda f: lambda a: lambda b: (lambda c: lambda d: lambda e: c(a)(c(b)(BOOL_TRUE)(BOOL_FALSE))(INT_EQ(d(a))(d(b))(lambda x: f(e(a))(e(b))(x))(BOOL_FALSE)))(ARR_INT_IS_EMPTY)(ARR_INT_FIRST)(ARR_INT_REST))


FUNC_TO_INT = lambda n: n(lambda n:n+1)(0)
FUNC_TO_BOOL = lambda b: b(True)(False)
FUNC_TO_LIST = ZCOM(lambda f: lambda l: [] if FUNC_TO_BOOL(ARR_INT_IS_EMPTY(l)) else [FUNC_TO_INT(ARR_INT_FIRST(l))]+f(ARR_INT_REST(l)))

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

func_to_int:str = "[n:n(A)(0)]"
func_to_bool:str = "[b:b(1)(0)]"

arr_int_eq = Z(lambda f: lambda a: lambda b: (lambda c: lambda d: lambda e: lambda g: c(a)(c(b)(K)(K(I)))(g(d(a))(d(b))(lambda x: f(e(a))(e(b))(x))(K(I))))(S(I)(K(K)))(S(K(S(I)(K(K))))(S(I)(K(K(I)))))(S(K(S(I)(K(K(I)))))(S(I)(K(K(I)))))(S(K(S(S(K(S(K(S(S(S)(K(S(K(S(S)(K(K))))(S(K(K))(S(K(S))(S(K(S(I)))(K)))))))(K(S(K(S(K(S(K(S(S)(K(K))))(S(K(K))(S(S)(K(K(I)))))))))(S(K(S(S)(K(S(K(S(K(S(K(S(I)))(K)))))(S(K(S(I)))(K))))))(K))))))(K))))(K(K(I)))))(S(K(S(S(K(S))(S(K(S(S)(K(S(K(S(S)(K(S(K(K))(S(K(S))(K))))))(S(K(K))(S(K(S(S)))(K)))))))(S(K(S(K(S))))(S(K(S(S)(K(S(K(S(S)(K(S(K(K))(S(K(S))(K))))))(S(K(K))(S(K(S(S)))(S(K(K))(S(K(S(S)(K(K))))(S(K(K))(S))))))))))(S(K(K))(S(K(S))(S(K(K))(S(K(S(K(S(K(S(S)(K(S(S(S))(K)(S)))))(K)))))(S(K(S(S)(K(K))))(S(K(K))(S(K(S))(S(K(S))(S(K(K))(S(K(S(K(I))))(S(K(S))(S(K(K))(S(K(S(S)))(S(K(K))(K)))))))))))))))))))))(S(K(S(K(K))))(S(K(S(S)(K(S(K(S(I)))(S(K(K))(K))))))(S(K(K))(S(K(S(S)))(S(K(K))(K)))))))(K)))

int_to_func:Callable = Z(lambda f: lambda n: S(S(K(S))(K))(f(B(n))) if B(n) else I)
list_to_func:Callable = Z(lambda f: lambda l: S(K(S(K(S(K(S(S)(K(K))))(S(K(K))(S(K(S))(S(K(S(I)))(K))))(K(I))))))(S(K(S(S)(K(S(K(K))(S(K(S))(S(K(S(I)))(K)))))))(S(K(K))(S(K(S(S(S)(K(K)))))(K))))(lambda x:f(l[1:])(x))(int_to_func(l[0])) if l else S(K(S(S)(K(K))))(S(K(K))(S(K(S))(S(K(S(I)))(K))))(K)(K))

def gen_fstr(b:bytes) -> str:
    s = arr_int_empty
    for c in b[::-1]:
        s = f"a({s})({nums[c]})"
    s = f"[a:{s}]({arr_int_push_front})"
    return s

print(str2str_compile("[x:f(x)]"))

l1 = list_to_func([1,2,3,4])
l2 = list_to_func([1,2,3,5])
print(FUNC_TO_BOOL(arr_int_eq(l1)(l2)))

l1 = list_to_func([1,2,3])
l2 = list_to_func([1,2,3,5])
print(FUNC_TO_BOOL(arr_int_eq(l1)(l2)))

l1 = list_to_func([1,2,3,5])
l2 = list_to_func([1,2,3,5])
print(FUNC_TO_BOOL(arr_int_eq(l1)(l2)))

print(FUNC_TO_LIST(list_to_func([1,2,3,4])))

#test = gen_fstr(b"CTFSG{oh my god why is this so cancer}")
#test = str2str_compile(test)
#print(test)
#print(bytes(FUNC_TO_LIST(eval(test))))