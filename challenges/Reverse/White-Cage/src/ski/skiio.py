#############################
# SKI Compiler as optimized #
# as I could get it.        #
# Will be packaged with an  #
# intepreter and a proper   # 
# interface once I get      #
# around to writing it      #
# Written by: JuliaPoo      #
#############################

from dataclasses import dataclass
from typing import NoReturn, Tuple, Literal, Union, List
from enum import Enum, unique
import re
import string
import random; random.seed(1)

ATOMS = {
    'S': '[x:[y:[z:x(z)(y(z))]]]',
    'K': '[x:[y:x]]',
    'I': '[x:x]',
    'i': 'i',
    'o': 'o'
}

VALID_NAME_REGEX = r"[a-zA-Z0-9_]+"

def gen_new_name(avoid:list=[]) -> str:
    names = string.ascii_lowercase + string.ascii_uppercase
    for n in names:
        if n in avoid: continue
        return n
    raise Exception("Ran out of variable names")

@unique
class NodeType(Enum):
    DECL = 0
    CALL = 1

@dataclass
class SKInode:

    node_type: Literal[NodeType.DECL, NodeType.CALL]
    childs: Tuple[Union[
        'SKInode', str
        ]] # Always length 2

    @staticmethod
    def _to_str(node: 'SKInode', minimise:bool=False) -> str:

        if type(node) is str:
            return node

        ntype = node.node_type
        if ntype == NodeType.DECL:
            argname, defi = node.childs
            return "[%s:%s]"%(argname, SKInode._to_str(defi, minimise))

        elif ntype == NodeType.CALL:
            A,B = node.childs
            A = SKInode._to_str(A, minimise)
            if minimise:
                return str(A) + (B if type(B) is str else \
                    "(%s)"%SKInode._to_str(B, minimise))
            return str(A) + "(%s)"%SKInode._to_str(B, minimise)

        else:
            raise Exception("Unexpected NodeType!")

    def __str__(self) -> str:
        return self._to_str(self)

    @staticmethod
    def _eq(node1: Union['SKInode',str], node2: Union['SKInode',str], 
            ctx1:dict, ctx2:dict) -> bool:
        
        if type(node1) is not type(node2):
            return False

        # Both nodes are leafs
        if type(node1) is str:

            free1, free2 = node1 in ctx1, node2 in ctx2
            if free1 != free2:
                return False

            # Both leafs are free
            if free1 and free2:
                # Check if leafs reference same variable
                return ctx1[node1] == ctx2[node2]

            # Both leafs are not free
            return node1 == node2

        # Both nodes are SKInodes
        if node1.node_type != node2.node_type:
            return False

        # Both nodes are declarations
        if node1.node_type == NodeType.DECL:

            arg1,defi1 = node1.childs
            arg2,defi2 = node2.childs

            # Add free variables to context
            ctx1,ctx2 = ctx1.copy(), ctx2.copy()
            ctx1[arg1] = max(ctx1.values())+1
            ctx2[arg2] = max(ctx2.values())+1

            return SKInode._eq(defi1, defi2, ctx1, ctx2)

        # Both nodes are calls
        if node1.node_type == NodeType.CALL:

            # Check if all children are equal
            for c1,c2 in zip(node1.childs, node2.childs):
                if not SKInode._eq(c1, c2, ctx1, ctx2):
                    return False

            return True

        raise Exception("Unexpected NodeType!")

    def __eq__(self, other: 'SKInode'):
        return self._eq(self, other, {0:0}, {0:0})

    def __repr__(self):
        return str(self)

SKInode_T = Union[SKInode, str]

class Rule:

    def __init__(self, lhs:str, rhs:str):
        self.rule_str = (lhs, rhs)
        self.lhs, self.rhs = code_to_ski(lhs), code_to_ski(rhs)

    def __str__(self):
        return "%s => %s"%(self.lhs, self.rhs)

    def __repr__(self):
        return str(self)

    @staticmethod
    def _check(lhs:SKInode_T, expr:SKInode_T, mapping:dict, \
        _lctx:dict, _ectx:dict) \
        -> Tuple[bool, dict]:
        
        # TODO: Make this only for NodeType.CALL

        if type(lhs) == str:
            if lhs in _lctx:
                if expr not in _ectx:
                    return False, {}
                return _lctx[lhs] == _ectx[expr], mapping
            if lhs in ATOMS:
                return lhs == expr, mapping
            if lhs in mapping:
                return mapping[lhs] == expr, mapping
            mapping[lhs] = expr
            return True, mapping
                
        if type(expr) == str:
            return False, {}

        lhs_t = lhs.node_type
        exp_t = expr.node_type
        if lhs_t != exp_t:
            return False, {}

        l1,l2 = lhs .childs
        e1,e2 = expr.childs

        if lhs_t == NodeType.DECL:
           (_lctx := _lctx.copy())[l1] = max(_lctx.values())+1
           (_ectx := _ectx.copy())[e1] = max(_ectx.values())+1
           return Rule._check(l2, e2, mapping, _lctx, _ectx)

        elif lhs_t == NodeType.CALL:
            succ, mapping = Rule._check(l1, e1, mapping, _lctx, _ectx)
            if not succ: return False, {}
            succ, mapping = Rule._check(l2, e2, mapping, _lctx, _ectx)
            if not succ: return False, {}
            return True, mapping

        raise Exception("Unexpected NodeType!")

    @staticmethod
    def _transform(rhs:SKInode_T, mapping:dict, \
        _rctx:set=set()) \
        -> SKInode_T:

        if type(rhs) == str:
            if rhs in _rctx or rhs in ATOMS:
                return rhs
            if rhs not in mapping:
                raise Exception("Mapping invalid! Doesn't have key %s"%rhs)
            return mapping[rhs]

        r1,r2 = rhs.childs
        if rhs.node_type == NodeType.DECL:
            (_rctx := _rctx.copy()).add(r1)
            childs = r1, Rule._transform(r2, mapping, _rctx)
        elif rhs.node_type == NodeType.CALL:
            childs = Rule._transform(r1, mapping, _rctx), \
                Rule._transform(r2, mapping, _rctx)
        else:
            raise Exception("Unexpected NodeType!")

        return SKInode(rhs.node_type, childs)

    def check(self, expr:SKInode_T) -> Tuple[bool, dict]:
        succ, mapping = self._check(self.lhs, expr, \
            {}, {0:0}, {0:0})
        if not succ: mapping = {}
        frees = get_all_free(self.rhs)
        for name in list(mapping.keys()):
            if name not in frees:
                mapping.pop(name)
        return succ, mapping

    def transform(self, mapping:dict) -> SKInode_T:
        return self._transform(self.rhs, mapping)

    def apply(self, expr:SKInode_T) -> Tuple[bool, SKInode_T]:
        success, mapping = self.check(expr)
        if not success:
            return success, expr
        return True, self.transform(mapping)

    def verify(self) -> bool:
        # If returns False, not guaranteed to be false
        B = beta_eta_reduce
        return B(self.rhs) == B(self.lhs)


def _is_valid_name(name:str) -> bool:
    return bool(re.match("^%s$"%VALID_NAME_REGEX, name))

def _tokenize(code:str) -> List[str]:
        
    tokens = []
    idx = 0
    while True:

        if idx==len(code): break
        c = code[idx]

        if c in '[]():': 
            tokens.append(c)
        elif match := re.match("^"+VALID_NAME_REGEX, code[idx:]):
            if not match:
                code_snippet = code[idx:min(len(code)-1, idx+10)]
                raise Exception("Invalid name `%s...`!"%(code_snippet))
            obj_str = match.group()
            tokens.append(obj_str)
            idx += len(obj_str)
            continue

        idx += 1
        
    return tokens

def _get_end_bracket(tokens:List[str], idx:int) -> bool:
    
    start = tokens[idx]
    end = {'(':')', '[':']'}[start]
    depth = 0
    while True:
        if idx == len(tokens): break
        t = tokens[idx]
        depth += t == start
        depth -= t == end
        if depth == 0: return idx
        idx += 1
    raise Exception("Unbalanced brackets `%s`"%start)

def _to_node(tokens:List[str]) -> SKInode_T:
    
    t = tokens[0]
    if len(tokens) == 1:
        if not _is_valid_name(t):
            raise Exception("Invalid name %s"%t)
        return t

    if t == '(':
        idx = _get_end_bracket(tokens, 0)
        node = _to_node(tokens[1:idx])

    elif t == '[':
        if len(tokens) < 5:
            raise Exception("Incomplete declaration!")
        t1,t2 = tokens[1], tokens[2]
        if not _is_valid_name(t1):
            raise Exception("Invalid argname %s"%t1)
        if t2 != ':':
            raise Exception("Expected `:`, not %s"%t2)

        idx = _get_end_bracket(tokens, 0)
        node = SKInode(NodeType.DECL, (
            t1, _to_node(tokens[3:idx])
        ))

    else:
        if not _is_valid_name(t):
            raise Exception("Invalid name %s"%t)
        t1 = tokens[1]
        if t1 != '(':
            raise Exception("Expected `(`, not %s"%t1)

        idx = _get_end_bracket(tokens, 1)
        node = SKInode(NodeType.CALL, (
            t, _to_node(tokens[2:idx])
        ))

    while idx != len(tokens)-1:
        tmp = idx
        t = tokens[tmp+1]
        if t != '(':
            raise Exception("Expected `(`, not %s"%t)

        idx = _get_end_bracket(tokens, tmp+1)
        node = SKInode(NodeType.CALL, (
            node, _to_node(tokens[tmp+2: idx])
        ))
        
    return node

def code_to_ski(code:str) -> SKInode_T:
    tokens = _tokenize(code)
    return _to_node(tokens)

def is_free(expr:SKInode_T, varname:str) -> bool:
    
    if type(expr) == str:
        return expr==varname
    
    t = expr.node_type
    c1,c2 = expr.childs
    if t == NodeType.DECL:
        if c1 == varname:
            return False
        return is_free(c2, varname)
    if t == NodeType.CALL:
        ret  = is_free(c1, varname)
        ret |= is_free(c2, varname)
        return ret
    raise Exception("Unexpected NodeType!")

def get_all_free(expr:SKInode_T, _ctx:set=set()) -> set:
    
    if type(expr) == str:
        if expr in _ctx:
            return set()
        return set(expr)

    t = expr.node_type
    c1,c2 = expr.childs
    if t == NodeType.DECL:
        (_ctx := _ctx.copy()).add(c1)
        return get_all_free(c2, _ctx)
    if t == NodeType.CALL:
        ret1 = get_all_free(c1, _ctx)
        ret2 = get_all_free(c2, _ctx)
        return ret1 | ret2
    raise Exception("Unexpected NodeType!")

def _sub(expr:SKInode_T, varname:str, repl:SKInode_T, \
    _repl_free:list, _ctx:set=set()) \
    -> SKInode_T:

    if type(expr) == str:
        if expr==varname:
            return repl
        return expr

    t = expr.node_type
    c1,c2 = expr.childs

    if t == NodeType.DECL:
        (_ctx := _ctx.copy()).add(c1)
        if c1 == varname:
            return expr
        if c1 in _repl_free:
            new_c1 = gen_new_name(avoid = _repl_free + list(_ctx))
            (_ctx := _ctx.copy()).add(new_c1)
            c2 = sub(c2, c1, new_c1, _ctx)
            c1 = new_c1
        c2 = _sub(c2, varname, repl, _repl_free, _ctx)
        return SKInode(t, (c1,c2))

    if t == NodeType.CALL:
        c1 = _sub(c1, varname, repl, _repl_free, _ctx)
        c2 = _sub(c2, varname, repl, _repl_free, _ctx)
        return SKInode(t, (c1,c2))

    raise Exception("Unexpected NodeType!")

def sub(expr:SKInode_T, varname:str, repl:SKInode_T, ctx:set=set()) \
    -> SKInode_T:

    repl_free = list(get_all_free(repl))
    return _sub(expr, varname, repl, repl_free, ctx)

def beta_eta_reduce(expr:SKInode_T, max_depth:int=500, raise_error=True, \
    _ctx:set=set(), _depth:int=0) -> SKInode_T:

    if _depth == max_depth:
        if raise_error:
            raise Exception("`beta_eta_reduce` Max depth `%d` reached"%max_depth)
        return expr
    _depth += 1

    if type(expr) == str:
        if expr in ATOMS and expr not in _ctx:
            return code_to_ski(ATOMS[expr])
        return expr

    # Shortforms
    B = lambda e,_c,_d: beta_eta_reduce(e, max_depth, raise_error, _c, _d)
    N, C, D = SKInode, NodeType.CALL, NodeType.DECL

    t = expr.node_type
    c1,c2 = expr.childs

    if t == C:

        c2 = B(c2, _ctx, _depth)
        if type(c1) == N and \
            c1.node_type == D:
            n,fn = c1.childs
            (_ctx := _ctx.copy()).add(n)
            return B(sub(fn, n, c2, _ctx), _ctx, _depth)

        if type(c1) == str:
            if c1 in 'SKI' and c1 not in _ctx:
                c1 = code_to_ski(ATOMS[c1])
                return B(N(t, (c1,c2)), _ctx, _depth)
            return N(t, (c1,c2))

        c1 = B(c1, _ctx, _depth)
        if (type(c1) == N and \
            c1.node_type == D):
            return B(N(t, (c1,c2)), _ctx, _depth)

        return N(t,(c1,c2))

    if t == D:

        if type(c2) != str and \
            c2.node_type == C:
            d1,d2 = c2.childs
            if d2 == c1 and not is_free(d1, c1):
                return B(d1, _ctx, _depth)

        (_ctx := _ctx.copy()).add(c1)
        c2 = B(c2, _ctx, _depth)
        return N(t, (c1, c2))

    raise Exception("Unexpected NodeType!")

def _optimise_node(expr:SKInode_T, rules:List[Rule]) -> SKInode_T:

    if type(expr) == str:
        return expr

    for r in rules:
        succ,mapping = r.check(expr)
        if not succ:
            continue
        return r.transform(mapping)

    return expr

def _optimise(expr:SKInode_T, rules:List[Rule], _cache={}) -> SKInode_T:

    expr = _optimise_node(expr, rules)
    h = hash(str(expr))
    if h in _cache:
        return _cache[h]
    
    if type(expr) == str:
        return expr

    t = expr.node_type
    c1,c2 = expr.childs
    if t == NodeType.CALL:
        c1,c2 = _optimise(c1,rules), _optimise(c2,rules)
    else:
        raise Exception("Declarations aren't supported in `optimise`")
    
    new_expr = SKInode(t, (c1,c2))
    _cache[h] = new_expr

    return new_expr

def _compile_SKI(expr:SKInode_T, rules:List[Rule], _cache = {}) -> SKInode_T:

    h = hash(str(expr))
    if h in _cache: return _cache[h]

    def store_cache(ret):
        _cache[h] = ret
        return ret

    # T[x] => x
    if type(expr) == str:
        return expr

    # Shortforms
    O = lambda e: _optimise(e, rules)
    T = lambda e: O(_compile_SKI(e, rules))
    C, D, N = NodeType.CALL, NodeType.DECL, SKInode

    t = expr.node_type
    c1,c2 = expr.childs

    # T[AB] => T[A] T[B]
    if t == C:
        return store_cache(O(N(C, (T(c1), T(c2)))))

    # T[[x:A]] => K T[A]  (x isn't free in A)
    if not is_free(c2, c1):
        return store_cache(O(N(C, ('K', T(c2)))))
    
    # T[x:x] => I
    if type(c2) == str and c2 == c1:
        return 'I'

    # T[x:[y:A]] => T[[x:T[y:A]]] (x is free in A)
    if c2.node_type == D:
        _,d2 = c2.childs
        if is_free(d2, c1):
            return store_cache(T(N(D, (c1, T(c2)))))
    
    # T[x:AB] => S T[[x:A]] T[[x:B]] (x is free in AB)
    d1,d2 = c2.childs
    ta = T(N(D, (c1, d1)))
    tb = T(N(D, (c1, d2)))
    return store_cache(O(N(C, (N(C, ('S', ta)), tb))))

def compile_SKI(expr:SKInode_T, optimisation:bool=True) -> SKInode_T:
    opt_rules = [
            Rule("M(L)(N(L))", "S(M)(N)(L)"),
            Rule("S(K(S(K(A))))(S(K(S(K(B))))(C))", "S(K(S(K(S(K(A))(B)))))(C)"),
            Rule("S(K(S(K(A))))(S(K(B)))", "S(K(S(K(A))(B)))"),
            Rule("S(K(A))(K(B))", "K(A(B))"),
            Rule("S(K(A))(I)", "A"),
            Rule("S(S(K(A))(B))(K(C))", "S(K(S(A)(K(C))))(B)"),
            Rule("S(S(I(A)))(I)", "S(S(S)(K))(A)"),
        ] if optimisation else []
    expr = _compile_SKI(expr, opt_rules)
    return expr
