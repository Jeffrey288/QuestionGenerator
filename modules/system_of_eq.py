from sympy import *
import random
from time import time
init_printing(use_unicode=True)
time = int(time())
random.seed(time)
print(time)

# random.seed(1673374020)

def swap(M, a, b): temp = M[a, :]; M[a, :] = M[b, :]; M[b, :] = temp


a = symbols('a')
b = symbols('b')
x, y, z, s, t = symbols('x y z s t')
roots = random.sample(range(-5, 6), k=2)
M = diag(*([a - root for root in roots] + [random.choice([1, -1])]))
M[2, :2] = [random.sample(range(-5, 6), k=2)]
M[1, 0] = random.randint(-1, 1) + random.choices([3, M[0, 0], a**2], weights=[0.45, 0.45, 0.1])[0]
M[0, :] = M[0, :] - M[2, :]
M[1, :] = M[1, :] + M[2, :]
for _ in range(10):
    p = random.random() 
    if (p < 0.2): swap(M, 1, 2)
    elif (p < 0.4): swap(M, 1, 0)
    elif (p < 0.6): swap(M, 2, 0)
    elif (p < 0.8): M = M.T
    elif (p < 0.86): r = int(5 * (p - 0.8)); M[r, :] = M[r, :] + M[(r + random.randint(1, 2)) % 3, :]
if sum([M[i % 3, i // 3] == 0 for i in range(9)]) > 2: pass
rhs = [[random.randint(-5, 5)] for _ in range(2)] + [[b]]
random.shuffle(rhs)
rhs = Matrix(rhs)

# question generation completed

pprint(rhs)
pprint(M)
pprint(factor(M.det()))
print(roots)

# solutions to (a):
print("══════════════════════ Part (a) ══════════════════════")
print(roots)
# solution to (b): M * X = rhs -> X = Minv * rhs
print("══════════════════════ Part (b) ══════════════════════") # https://en.wikipedia.org/wiki/Box-drawing_character
pprint(simplify(M ** (-1) * rhs))

print("══════════════════════ Part (c) ══════════════════════")
sol_properties = [[] for _ in roots]
sol = [[] for _ in roots]
from enum import Enum
class Root(Enum):
    ALL = 1
    NONE = 2
    UNIQUE = 3 # unique value of b
    ONE = 4 # solution uses only t
    TWO = 5 # solution uses s and t

for i, root in enumerate(roots):

    print("───────── Root:", root, "────────")
    """
    The substituted matrix m can have the following cases:
    - it is of rank 2
    - it is of rank 1 (actually most likely won't happen)
    - it is of rank 0: [[0, 0, 0]] case, which is likely to be prevented by question generation
    """
    m = M.subs(a, root)
    pprint(m)
    rank = m.rank()
    print("rank =", rank)
    
    h = m.col_insert(3, rhs)
    # "row reduction"
    if not (h[0, 0] == 0 and h[1, 0] == 0 and h[2, 0]): # if first row all 0, then we don't need to row reduce
        if (h[0, 0] == 0): 
            if h[1, 0] == 0: swap(h, 0, 2) # we made sure that h[2, 0] is not 0
            else: swap(h, 0, 1)
        if h[1, 0] != 0: h[1, :] = - h[1, 0] * h[0, :] + h[0, 0] * h[1, :]
        if h[2, 0] != 0: h[2, :] = - h[2, 0] * h[0, :] + h[0, 0] * h[2, :]
    if not (h[1, 1] == 0 and h[2, 1] == 0): 
        if h[1, 1] == 0: swap(h, 1, 2)
        if h[2, 1] != 0: h[2, :] = - h[1, 1] * h[2, :] + h[2, 1] * h[1, :]
    elif not (h[1, 2] == 0 and h[2, 2] == 0):
        if h[1, 2] == 0: swap(h, 1, 2)
        if h[2, 2] != 0: h[2, :] = - h[1, 2] * h[2, :] + h[2, 2] * h[1, :]
    pprint(h)
    
    print(h[2, 3])
    b0 = h[2, 3].coeff(b, n=0)
    b1 = h[2, 3].coeff(b, n=1)
    if b0 == 0 and b1 == 0: bval = "all"; sol_properties[i].append(Root.ALL) # i.e. for all values of b
    elif b0 != 0 and b1 == 0: bval = "none"; sol_properties[i].append(Root.NONE) # i.e. independent of b, and always no solution
    else: bval = -b0 / b1; sol_properties[i].append(Root.UNIQUE)
    print(b0, b1, bval)

    if bval == "none": X = None; Y = None; Z = None
    else:
        if bval == "all": H = h
        else: H = h.subs(b, bval)
        
        if H[1, 1] == 0 and H[1, 2] == 0: Y = s; Z = t
        elif H[1, 1] == 0: Y = t; Z = H[1, 3] / H[1, 2]
        elif H[1, 2] == 0: Z = t; Y = H[1, 3] / H[1, 1]
        else: Z = t; Y = (H[1, 3] - H[1, 2] * Z) / H[1, 1]

        X = (H[0, 3] - H[0, 1] * Y - H[0, 2] * Z) / H[0, 0] # we made sure H[0, 0] is never zero

        if H[1, 1] == 0 and H[1, 2] == 0:
            print("X =", X, ", Y =", Y, ", Z =", Z, ", s, t are real numbers")
            sol_properties[i].append(Root.TWO)
        else:
            print("X =", X, ", Y =", Y, ", Z =", Z, ", t is real number")
            sol_properties[i].append(Root.ONE)
    
    sol[i] = [bval, (X, Y, Z)]



if sol_properties[0][0] == Root.ALL and sol_properties[0][1] == Root.ONE:
    e_idx = 0
elif sol_properties[1][0] == Root.ALL and sol_properties[1][1] == Root.ONE:
    e_idx = 1
else:
    e_idx = None

if sol_properties[0][0] != Root.NONE and sol_properties[0][1] == Root.ONE and e_idx != 0:
    d_idx = 0
    if e_idx != 1 and sol_properties[1][0] != Root.NONE and sol_properties[1][1] == Root.ONE: f_idx = 1
    else: f_idx = None
elif sol_properties[1][0] != Root.NONE and sol_properties[1][1] == Root.ONE and e_idx != 1:
    d_idx = 1
    f_idx = None
else:
    d_idx = None
    f_idx = None

print("══════════════════════ Part (d) ══════════════════════")
# Suppose (x,y,z) satisfies (E) with a=1 and b=5. Find the least value of x^2+y^2+z^2. 
if d_idx is not None:
    if sol_properties[d_idx][0] == Root.ALL: d_b = random.randint(-10, 10)
    else: d_b = sol[d_idx][0]
    d_sys = M.subs(a, roots[d_idx]).col_insert(3, rhs).subs(b, d_b)
    d_sols = [X.subs(b, d_b) for X in sol[d_idx][1]]

    def generate():
        while True:
            d_expr = sum([a * b for a, b in zip(random.sample([x**2, y**2, z**2, x*y, y*z, x*z], k=3), [int(random.gauss(mu=0, sigma=8)) for _ in range(3)])])
            d_sub_expr = expand(d_expr.subs(x, d_sols[0]).subs(y, d_sols[1]).subs(z, d_sols[2]))
            if (d_sub_expr.coeff(t, n=2) != 0): break
        d_opt = d_sub_expr.coeff(t, n=0) - (d_sub_expr.coeff(t, n=1) ** 2 / 4 / d_sub_expr.coeff(t, n=2))
        return [d_opt, d_expr, d_sub_expr]
    d_opt, d_expr, d_sub_expr = min([generate() for _ in range(6)], key=lambda x: (fraction(x[0])[1]) ** 4 + 1e-3 * x[0] ** 2)

    pprint(d_sys)
    pprint(d_expr)
    pprint(expand(d_sub_expr))
    print(d_sub_expr.coeff(t, n=2))
    print(d_opt)

else:
    print("part (d) is not generated")

print("══════════════════════ Part (e) ══════════════════════")
# (e)	Suppose (x,y,z) satisfies (E) with a=1 and x^2+y^2+z^2=b+3. Find the range of values of b. [ALL, ONE]
if e_idx is not None:
    e_sys = M.subs(a, roots[e_idx]).col_insert(3, rhs)
    e_sols = sol[e_idx][1]
    pprint(e_sys)

    def generate():
        e_expr_lhs = sum([a * b for a, b in zip(random.sample([x**2, y**2, z**2, x*y, y*z, x*z], k=3), [int(random.gauss(mu=0, sigma=8)) for _ in range(3)])])
        e_expr_rhs = b + int(random.gauss(mu=0, sigma=10))
        e_expr = e_expr_lhs - e_expr_rhs
        e_sub_expr = expand(e_expr.subs(x, e_sols[0]).subs(y, e_sols[1]).subs(z, e_sols[2]))
        e_disc = expand(e_sub_expr.coeff(t, n=1) ** 2 - 4 * e_sub_expr.coeff(t, n=0) * e_sub_expr.coeff(t, n=2))
        return [e_expr_lhs, e_expr_rhs, e_expr, e_sub_expr, e_disc]
    e_expr_lhs, e_expr_rhs, e_expr, e_sub_expr, e_disc = min([generate() for _ in range(24)], key=lambda x: abs((fraction(x[4].coeff(b, n=0))[0])) - 1e10 * (x[4].coeff(b, n=2) == 0))
    
    A, B, C = e_disc.coeff(b, n=2), e_disc.coeff(b, n=1), e_disc.coeff(b, n=0)
    print(A, B, C)
    if A == 0:
        if B == 0:
            if C >= 0: print(r"The required range is $\mathbb{R}$")
            else: print(r"No real values of b.")
        else:
            if B > 0: print(rf"The required range is b >= {-C/B}") 
            else: print(rf"The required range is b <= {-C/B}")       
    else:
        if B**2-4*A*C < 0: print(rf"No real values of b.")
        elif B > 0: print(rf"b < {(-B-sqrt(B**2-4*A*C))/(2*A)} or b >= {(-B+sqrt(B**2-4*A*C))/(2*A)}")
        else: print(rf"b < {(-B-sqrt(B**2-4*A*C))/(2*A)} or b >= {(-B+sqrt(B**2-4*A*C))/(2*A)}")

    print(e_expr)
    print(e_sub_expr)
    print(e_disc)
    
print("══════════════════════ Part (f) ══════════════════════")
# (f) 	(F) is (E) with a=1 and x+y-z=1. Is (F) consistent? [UNIQUE, ONE/ALL, ONE]
if f_idx is not None:
    if sol_properties[f_idx][0] == Root.ALL: f_b = random.randint(-10, 10)
    else: f_b = sol[f_idx][0]
    f_sys = M.subs(a, roots[f_idx]).col_insert(3, rhs).subs(b, f_b)
    f_sols = [X.subs(b, f_b) for X in sol[f_idx][1]]
    f_basis = min([[X.subs(t, t_rand) for X in sol[f_idx][1]] for t_rand in [int(random.gauss(mu=0, sigma=15)) for _ in range(10)]], key=lambda x: fraction(sum(x))[1]) # generate quadratic equation above this
    def generate():
        f_expr_lhs = sum([a * b for a, b in zip(random.sample([x**2, y**2, z**2, x*y, y*z, x*z], k=3), [random.choice([1, -1]) * random.randint(1, 6) for _ in range(3)])])
        f_expr_rhs = f_expr_lhs.subs(x, f_basis[0]).subs(y, f_basis[1]).subs(z, f_basis[2])
        return [f_expr_lhs, f_expr_rhs]
    f_expr_lhs, f_expr_rhs = min([generate() for _ in range(10)], key=lambda x: (fraction(x[1])[0]) ** 4 + 1e-3 * x[1] ** 2)
    # denom = fraction(f_expr_rhs)[1]
    # f_expr_lhs = f_expr_lhs * denom
    # f_expr_rhs = f_expr_rhs * denom
    f_expr = f_expr_lhs - f_expr_rhs
    f_sub_expr = expand(f_expr.subs(x, f_sols[0]).subs(y, f_sols[1]).subs(z, f_sols[2]))
    print(f_sub_expr)
    A, B, C = f_sub_expr.coeff(t, n=2), f_sub_expr.coeff(t, n=1), f_sub_expr.coeff(t, n=0)

    if A == 0:
        print(rf"t = {-C/B}, and (x, y, z) = {[X.subs(t, -C/B) for X in sol[f_idx][1]]}")
    elif B**2-4*A*C == 0:
        print(rf"t = {-B/2/A}, and (x, y, z) = {[X.subs(t, -B/2/A) for X in sol[f_idx][1]]}")
    else:
        t1 = (-B-sqrt(B**2-4*A*C))/(2*A)
        t2 = (-B+sqrt(B**2-4*A*C))/(2*A)
        print(rf"t = {t1} or {t2}, and (x, y, z) = {[X.subs(t, t1) for X in sol[f_idx][1]]} or {[X.subs(t, t2) for X in sol[f_idx][1]]}")
    print(A, B, C)

    print(f_expr_lhs)
    print(f_expr_rhs)
    print(f_basis)

    print(f_sols)

else:
    print("part (f) is not generated")