import z3

# Init parameters
ct = open('../dist/flag.enc','rb').read()
blksize = 4
n = 100000
iv = b'\0'*4
allowed = b"qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM "

# Get cipher text blocks
cblks = [ct[i*blksize:(i+1)*blksize] for i in range(len(ct) // blksize)]
# Don't consider collisions from blocks with too high frequency
# as that would probably be from same-input collisions.

# Init symbolic flag
flag_len = len(ct)//n
flag_sym = [z3.BitVec("f%02d"%i, 8) for i in range(flag_len)]

# Get all collisions
# This cannot distinguish identical cipher text blocks due to
# hash collisions or input collisions (input = xor(prev_plaintext_blk, curr_ciphertext_blk))
# We only want input collisions as that leaks plaintext info.
collisions = {}
for idx,blk in enumerate(cblks):
    if blk not in collisions: 
        collisions[blk] = []
    # Remove all collisions that results from reason 3.
    if cblks[idx-1] in [cblks[i-1] for i in collisions[blk]]:
        continue
    collisions[blk].append(idx)
collisions = [idxlist for _, idxlist in collisions.items() if len(idxlist)!=1]

# Flatten collisions into pairs
collisions = [(L[i], L[j]) for L in collisions for i in range(len(L)) for j in range(i+1,len(L))]

print("Found %d potential collisions"%len(collisions))

def init_solver():

    '''
    Init z3 solver and 
    constraint flag to be composed of `allowed` characters
    '''

    s = z3.Solver()
    for c_sym in flag_sym:
        s.add(z3.Or([c_sym == c for c in allowed]))
    return s

def build_constraints(collisions):

    '''
    Returns constraints on `flag_sym` assuming collisions
    are caused by input collisions and not hash collisions
    '''

    constraints = []
    for idxlist in collisions:
        tmp = ()
        prev_blks = [cblks[idx-1] if idx != 0 else iv for idx in idxlist]
        ci,cj = prev_blks[0], prev_blks[1]
        ii,ij = idxlist[0], idxlist[1]
        cxor = [x^y for x,y in zip(ci,cj)]
        for k in range(blksize):
            pi = flag_sym[(ii*blksize + k)%flag_len]
            pj = flag_sym[(ij*blksize + k)%flag_len]
            tmp += (pi^pj == cxor[k],)
        constraints.append(tmp)
    return constraints

def print_sols(solver, n=3):

    '''
    Given a solver, print n solutions for `flag_sym` (default 3)
    '''

    while solver.check()!=z3.unsat and n>0:
        m = solver.model()
        print("Possible flag: CTF{%s}"%
            bytes([m[c].as_long() for c in flag_sym]).decode('utf-8'))
        solver.add(z3.Not(z3.And([m[c]==c for c in flag_sym])))
        n -= 1
    if solver.check()!=z3.unsat:
        print("...")

def recurse(solver, constraints):

    '''
    Recursively tries all maximal subsets of `constraints` that yield a satisfiable model (>0 solutions)
    A maximal subset A of `constraints` means it is impossible to increase the size of subset A
    by adding more constraints from `constraints` such that A still yields a satisfiable model.

    This allows finding a sufficient subset of `constraints` caused by input collisions and not
    hash collisions, recovering the flag.

    Prints solutions reached by these maximal subsets
    Returns True if solver is satisfiable
    '''
    
    # Stores the minimum number of constraints left ever reached.
    global depth_left
    # Stores constraints tried
    global tried
    # Init default globals
    if 'depth_left' not in globals():
        depth_left = len(constraints)
    if 'tried' not in globals():
        tried = []

    # Check if has tried
    s = set(constraints)
    for c in tried:
        if c.issubset(s):
            return True
    # Update tried
    tried.append(s)

    # Stop recursing if solver is already unsatisfiable
    if solver.check()==z3.unsat:
        return True

    # Stop recursing if no constraints are left.
    if len(constraints)==0:
        print_sols(solver)
        return True
    
    print("Constraints left: %d"%len(constraints), end="  \r")

    valid = False
    # Try to append one more constraint from those left
    for c in constraints:
        # Duplicate current solver
        new_solver = solver.translate(z3.main_ctx())
        new_solver.add(c)
        valid != recurse(new_solver, [con for con in constraints if con!=c])

    # None of the new models are satisfiable
    # set of constraints in `solver` is maximal
    if not valid:
        # depth reached before, ignore
        if len(constraints) >= depth_left:
            return True
        # Depth not reached before, print solutions
        depth_left = len(constraints)
        print("New depth reached, %d constraints left"%depth_left)
        print_sols(solver)

    return True


solver = init_solver()
constraints = build_constraints(collisions)
recurse(solver, constraints)
print("Done")