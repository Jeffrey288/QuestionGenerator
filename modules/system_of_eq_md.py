from sympy import *
import random
from enum import Enum
class Root(Enum):
    ALL = 1
    NONE = 2
    UNIQUE = 3 # unique value of b
    ONE = 4 # solution uses only t
    TWO = 5 # solution uses s and t

# random.seed(1673437677)
# print(random.getstate())
# from time import time
# init_printing(use_unicode=True)
# time = int(time())
# random.seed(time)
# print(time)


f = open("question.md", "w", encoding="utf8")
def process(text): return text.replace("<<", "{").replace(">>", "}")

def swap(M, a, b): temp = M[a, :]; M[a, :] = M[b, :]; M[b, :] = temp



def row(M):
    first = False
    arglist = ["" for _ in range(5)] + ["=", latex(M[0, 3])]
    if (M[0, 0] == 0): pass
    else:
        first = True
        X = Poly(M[0, 0], a)
        if (abs(M[0, 0]) == 1):
            arglist[0] = "x" if M[0, 0] > 0 else "-x"
        elif (len(X.terms()) == 1):
            arglist[0] = f"{latex(M[0, 0])}x"
        else:
            arglist[0] = f"({latex(M[0, 0])})x"
    print(M[0, 1])
    Y = Poly(M[0, 1], a)
    if (M[0, 1] == 0): pass
    elif (abs(M[0, 1]) == 1):
        arglist[1:3] = ["-", "y"] if (M[0, 1] < 0) else ["+" if first else "", "y"]
    elif (len(Y.terms()) == 1):
        arglist[1:3] = ["-", latex(-M[0, 1])+"y"] if (Y.terms()[0][1] < 0) else ["+", latex(M[0, 1])+"y"]
    else:
        arglist[1:3] = ["+" if first else "", f"({latex(M[0, 1])})y"]
    if (M[0, 1] != 0): first = True
    Z = Poly(M[0, 2], a)
    if (M[0, 2] == 0): pass
    elif (abs(M[0, 2]) == 1):
        arglist[3:5] = ["-", "z"] if (M[0, 2] < 0) else ["+" if first else "", "z"]
    elif (len(Z.terms()) == 1):
        arglist[3:5] = ["-", latex(-M[0, 2])+"z"] if (Z.terms()[0][1] < 0) else ["+", latex(M[0, 2])+"z"]
    else:
        arglist[3:5] = ["+" if first else "", f"({latex(M[0, 2])})z"]
    return "&".join(arglist)

def print_matrix(M):
    return "\\\\ ".join([row(M[r, :]) for r in range(shape(M)[0])])

def print_sys(M):
    temp = print_matrix(M)
    return rf"\begin<<cases>>\begin<<array>><<rrrrrrr>>{temp}\end<<array>>\end<<cases>>"


def print_det(M):
    return rf"\left|{latex(M)[6:-7]}\right|"

def print_aug(M):
    return rf"\left(\begin<<array>><<ccc|c>>{latex(M)[6+14:-7-12]}\end<<array>>\right)"

def row_reduce(h0):
    # "row reduction"
    h = h0[:, :]
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
    return h

a = symbols('a')
b = symbols('b')
x, y, z, s, t = symbols('x y z s t')

while True:
    # generate lhs
    while True:
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
        if sum([M[i % 3, i // 3] == 0 for i in range(9)]) >= 2: continue
        for i in range(3):
            if (M[i, 0].is_real and M[i, 0] < 0): M[i, :] = - M[i, :]
        break

    # generate rhs
    while True:
        rhs = [[random.randint(-5, 5)] for _ in range(2)] + [[b]]
        random.shuffle(rhs)
        b_idx = rhs.index([b])
        rhs = Matrix(rhs)

        h0s = []
        hs = []
        properties = []
        for root in roots: # requires the problem to contain some kind of root
            m = M.subs(a, root)
            h0 = m.col_insert(3, rhs)
            h0s.append(h0)
            h = row_reduce(h0)
            hs.append(h)
            b0 = h[2, 3].coeff(b, n=0)
            b1 = h[2, 3].coeff(b, n=1)
            if b0 == 0 and b1 == 0: properties.append(Root.ALL) # i.e. for all values of b
            elif b0 != 0 and b1 == 0: properties.append(Root.NONE) # i.e. independent of b, and always no solution
            else: properties.append(Root.UNIQUE)
        if (Root.ALL in properties or Root.NONE in properties): continue # remove this later
        break
    break


# question generation completed

pprint(rhs)
pprint(M)
pprint(factor(M.det()))
print(roots)

q_question = process(rf"""Consider the following system of linear equations in $x$, $y$ and $z$:
$$(E): {print_sys(M.col_insert(3, rhs))}$$""")
f.write(q_question)

# solutions to (a):
print("══════════════════════ Part (a) ══════════════════════")
print(roots)

q_a = process("If $(E)$ has a unique solution, find the range of values of $a$.")
f.write("\n\n(a)\t" + q_a)
a_a = process(
rf"""$(E)$ has a unique solution     
⇔ $\Delta\neq0$     
⇔ ${print_det(M)}\neq0$     
⇔ ${latex(M.det())}\neq0$     
⇔ ${latex(factor(M.det()))}\neq0$     
⇔ $a\neq{roots[0]}$ and $a\neq{roots[1]}$""")
f.write("\n\n" + a_a)
# solution to (b): M * X = rhs -> X = Minv * rhs
print("══════════════════════ Part (b) ══════════════════════") # https://en.wikipedia.org/wiki/Box-drawing_character
unique_sol = simplify(M ** (-1) * rhs)
u_sol = list(unique_sol)
pprint(unique_sol)

Dx = M.copy(); Dx[:, 0] = rhs
Dy = M.copy(); Dy[:, 1] = rhs
Dz = M.copy(); Dz[:, 2] = rhs
q_b = process("Solve $(E)$ for the range of values found in (a).")
f.write("\n\n(b)\t" + q_b)
a_b = process(
rf"""$$\begin<<aligned>>
x&=\dfrac<<{print_det(Dx)}>><<\Delta>>=\dfrac<<{latex(Dx.det())}>><<\Delta>>\\
&={latex(factor(unique_sol[0]))}\\
y&=\dfrac<<{print_det(Dy)}>><<\Delta>>=\dfrac<<{latex(Dy.det())}>><<\Delta>>\\
&={latex(factor(unique_sol[1]))}\\
z&=\dfrac<<{print_det(Dz)}>><<\Delta>>=\dfrac<<{latex(Dz.det())}>><<\Delta>>\\
&={latex(factor(unique_sol[2]))}
\end<<aligned>>$$
"""
)
f.write("\n\n" + a_b)

print("══════════════════════ Part (c) ══════════════════════")
sol_properties = [[] for _ in roots]
sol = [[] for _ in roots]

q_c = rf"""For each of the following cases, find the range of values of b such that $(E)$ is consistent, and solve $(E)$ for such values of $b$ (if they exist).  \
(i) $a={roots[0]}$ \
(ii) $a={roots[1]}$ 
"""
a_c = ""

f.write("\n\n(c) " + q_c)

for i, root in enumerate(roots):

    text = rf"({'i'*(i+1)}) When $a={root}$, the augmented matrix of (E) becomes" + "\n"

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
    
    h0 = h0s[i]
    text +=  "$$" + print_aug(h0)
    h = hs[i]
    text += rf"\sim" + print_aug(h) + "$$\n\n"

    print(h[2, 3])
    b0 = h[2, 3].coeff(b, n=0)
    b1 = h[2, 3].coeff(b, n=1)
    if b0 == 0 and b1 == 0: 
        bval = "all"; sol_properties[i].append(Root.ALL) # i.e. for all values of b
        text += rf"$(E)$ is consistent for all real values of $b$." + "\n\n"
    elif b0 != 0 and b1 == 0: 
        bval = "none"; sol_properties[i].append(Root.NONE) # i.e. independent of b, and always no solution
        text += rf"$(E)$ is inconsistent for all real values of $b$." + "\n\n"
    else: 
        bval = -b0 / b1; sol_properties[i].append(Root.UNIQUE)
        text += rf"$(E)$ is consistent when $b={latex(bval)}$.".replace("frac", "dfrac") + "\n\n"
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
    
        text += rf"Therefore, the solution set is $\left\<<\left({latex(together(X))},\:{latex(together(Y))},\:{latex(together(Z))}\right):".replace("frac", "dfrac") + \
            rf"{'s,t' if (H[1, 1] == 0 and H[1, 2] == 0) else 't'}\in\mathbb<<R>>\right\>>$." + "\n\n"
    sol[i] = [bval, (X, Y, Z)]

    a_c += process(text)

f.write("\n\n" + a_c)

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

d_idx, f_idx = [d_idx, f_idx][::random.choice([1,-1])]

print("══════════════════════ Part (d) ══════════════════════")
# Suppose (x,y,z) satisfies (E) with a=1 and b=5. Find the least value of x^2+y^2+z^2. 
if d_idx is not None:
    if sol_properties[d_idx][0] == Root.ALL: d_b = random.randint(-10, 10)
    else: d_b = sol[d_idx][0]
    d_sys = M.subs(a, roots[d_idx]).col_insert(3, rhs).subs(b, d_b)
    d_sys[b_idx, :] = d_sys[b_idx, :] * fraction(d_b)[1]
    for i in range(3):
        if (d_sys[i, 0].is_real and d_sys[i, 0] < 0): d_sys[i, :] = - d_sys[i, :]
    d_sols = [X.subs(b, d_b) for X in sol[d_idx][1]]
    print(sol[d_idx][1])
    print(d_sols)

    def generate():
        while True:
            d_expr = sum([a * b for a, b in zip(random.sample([x**2, y**2, z**2, x*y, y*z, x*z], k=3), [int(random.gauss(mu=5, sigma=10)) for _ in range(3)])])
            d_sub_expr_1 = d_expr.subs(x, d_sols[0]).subs(y, d_sols[1]).subs(z, d_sols[2])
            d_sub_expr = expand(d_sub_expr_1)
            if (d_sub_expr.coeff(t, n=2) != 0): break
        d_opt = d_sub_expr.coeff(t, n=0) - (d_sub_expr.coeff(t, n=1) ** 2 / 4 / d_sub_expr.coeff(t, n=2))
        return [d_opt, d_expr, d_sub_expr, d_sub_expr_1]
    d_opt, d_expr, d_sub_expr, d_sub_expr_1 = min([generate() for _ in range(6)], key=lambda x: (print(x), (fraction(x[0])[1]) ** 4 + 1e-3 * x[0] ** 2)[-1])
    A, B, C = d_sub_expr.coeff(t, n=2), d_sub_expr.coeff(t, n=1), d_sub_expr.coeff(t, n=0)
    q_d = process(rf"Find the {'greatest' if (d_sub_expr.coeff(t, n=2) < 0) else 'least'} value of ${latex(d_expr)}$, where $x, y, z$ are real numbers satisfying" + "\n\n$"
     + print_sys(d_sys).replace("frac", "dfrac") + "$.")
    double_slash = r"\\"
    a_d = process(rf"""The given system is obtained by substituting $a={roots[d_idx]}$ and $b={latex(d_b)}$ into $(E)$. \
Hence, by putting $x={latex(together(d_sols[0]))}$, $y={latex(together(d_sols[1]))}$ and $z={latex(together(d_sols[2]))}$ into the given expression, we have
$$\begin<<aligned>>
    {latex(d_expr)}&={latex(d_sub_expr_1)}
        {double_slash + r'&='+latex(Poly(A*t**2+B*t+C,t).as_expr()) if (A*t**2+B*t+C != d_sub_expr_1) else ""}
        {double_slash + r'&='+latex(A*(t+B/(2*A))**2+(C-B**2/(4*A))) if (A*(t+B/(2*A))**2+(C-B**2/(4*A)) != d_sub_expr_1) else ""}
\end<<aligned>>$$
Hence, the {'greatest' if (d_sub_expr.coeff(t, n=2) < 0) else 'least'} value of ${latex(d_expr)}$ is ${latex(d_opt)}$.
    """).replace("frac", "dfrac")
    pprint(d_sys)
    pprint(d_expr)
    pprint(expand(d_sub_expr))
    print(d_sub_expr.coeff(t, n=2))
    print(d_opt)

else:
    q_d = "This part was not generated."
    a_d = "This part was not generated."

f.write("\n\n(d) " + q_d + "\n\n" + a_d)


print("══════════════════════ Part (e) ══════════════════════")
# (e)	Suppose (x,y,z) satisfies (E) with a=1 and x^2+y^2+z^2=b+3. Find the range of values of b. [ALL, ONE]
if e_idx is not None:
    e_sys = M.subs(a, roots[e_idx]).col_insert(3, rhs)
    for i in range(3):
        if (e_sys[i, 0].is_real and e_sys[i, 0] < 0): e_sys[i, :] = - e_sys[i, :]
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
            if C >= 0: result = (r"Solving, the required range is $\mathbb{R}$")
            else: result = (r"Solving, we find that there are no real values of $b$ that satisfy.")
        else:
            if B > 0: result = (rf"Solving, we find that the required range is $b \geq {latex(-C/B)}$") 
            else: result = (rf"Solving, we find that the required range is $b \leq {latex(-C/B)}$")       
    else:
        if B**2-4*A*C < 0: result = (rf"No real values of b.")
        elif B > 0: result = (rf"Solving, we find that the required range is $b \leq {latex((-B-sqrt(B**2-4*A*C))/(2*A))}$ or $b \geq {latex((-B+sqrt(B**2-4*A*C))/(2*A))}$.")
        else: result = (rf"Solving, we find that the required range is $b \leq {latex((-B-sqrt(B**2-4*A*C))/(2*A))}$ or $b \geq {latex((-B+sqrt(B**2-4*A*C))/(2*A))}$.")

    print(e_expr)
    print(e_sub_expr)
    print(e_disc)

    q_e = process(rf"Suppose that a real solution of ${print_sys(e_sys)}$ satisfies ${latex(e_expr_lhs)}={latex(e_expr_rhs)}$, where $b\in\mathbb<<R>>$. Find the range of values of $b$.")
    a_e = process(rf"""The given system is obtained by substituting $a={roots[e_idx]}$ into $(E)$. \
Hence, by putting $x={latex(together(e_sols[0]))}$, $y={latex(together(e_sols[1]))}$ and $z={latex(together(e_sols[2]))}$ into the given equation, we have \
${latex(e_expr_lhs.subs(x, e_sols[0]).subs(y, e_sols[1]).subs(z, e_sols[2]))}={latex(e_expr_rhs)}$, \
or ${latex(collect(e_sub_expr, t))}=0$. \
Since the above equation has real solutions, we have \
$\Delta={latex(UnevaluatedExpr(e_sub_expr.coeff(t, n=1)) ** 2 - 4 * UnevaluatedExpr(e_sub_expr.coeff(t, n=0)) * UnevaluatedExpr(e_sub_expr.coeff(t, n=2)))}>0$ \
or ${latex(e_disc)}\geq0$ \
{result}
""".replace("frac", "dfrac"))
 
else:
    q_e = "This part was not generated."
    a_e = "This part was not generated."

f.write("\n\n(e) " + q_e + "\n\n" + a_e)   
print("══════════════════════ Part (f) ══════════════════════")
# (f) 	(F) is (E) with a=1 and x+y-z=1. Is (F) consistent? [UNIQUE, ONE/ALL, ONE]
if f_idx is not None:
    if sol_properties[f_idx][0] == Root.ALL: f_b = random.randint(-10, 10)
    else: f_b = sol[f_idx][0]
    f_sys = M.subs(a, roots[f_idx]).col_insert(3, rhs).subs(b, f_b)
    f_sys[b_idx, :] = f_sys[b_idx, :] * fraction(f_b)[1]
    for i in range(3):
        if (f_sys[i, 0].is_real and f_sys[i, 0] < 0): f_sys[i, :] = - f_sys[i, :]
    f_sols = [X.subs(b, f_b) for X in sol[f_idx][1]]
    f_basis = min([[X.subs(t, t_rand) for X in sol[f_idx][1]] for t_rand in [int(random.gauss(mu=0, sigma=15)) for _ in range(10)]], key=lambda x: fraction(sum(x))[1]) # generate quadratic equation above this
    def generate():
        f_expr_lhs = sum([a * b for a, b in zip(random.sample([x**2, y**2, z**2, x*y, y*z, x*z], k=3), [random.choice([1, -1]) * random.randint(1, 6) for _ in range(3)])])
        f_expr_rhs = f_expr_lhs.subs(x, f_basis[0]).subs(y, f_basis[1]).subs(z, f_basis[2])
        return [f_expr_lhs, f_expr_rhs]
    f_expr_lhs, f_expr_rhs = min([generate() for _ in range(10)], key=lambda x: [k := (fraction(x[1])[0]) ** 4 + 1e-3 * x[1] ** 2, print(k), k][-1])
    # denom = fraction(f_expr_rhs)[1]
    # f_expr_lhs = f_expr_lhs * denom
    # f_expr_rhs = f_expr_rhs * denom
    f_expr = f_expr_lhs - f_expr_rhs
    f_sub_expr = expand(f_expr.subs(x, f_sols[0]).subs(y, f_sols[1]).subs(z, f_sols[2]))
    print(f_sub_expr)
    A, B, C = f_sub_expr.coeff(t, n=2), f_sub_expr.coeff(t, n=1), f_sub_expr.coeff(t, n=0)

    if A == 0:
        result = (rf"$t = {latex(-C/B)}$, and $(x, y, z) = \left({r','.join([latex(X.subs(t, -C/B)) for X in sol[f_idx][1]])}\right)$.")
    elif B**2-4*A*C == 0:
        result = (rf"$t = {latex(-B/2/A)}$, and $(x, y, z) = \left({r','.join([latex(X.subs(t, -B/2/A)) for X in sol[f_idx][1]])}\right)$.")
    else:
        t1 = (-B-sqrt(B**2-4*A*C))/(2*A)
        t2 = (-B+sqrt(B**2-4*A*C))/(2*A)
        result = (rf"$t = {latex(t1)}$ or ${latex(t2)}$, and $(x, y, z) = \left({r','.join([latex(X.subs(t, t1)) for X in sol[f_idx][1]])}\right)$ or $\left({r','.join([latex(X.subs(t, t2)) for X in sol[f_idx][1]])}\right)$.")
    print(A, B, C)

    print(f_expr_lhs)
    print(f_expr_rhs)
    print(f_basis)

    print(f_sols)

    backslash = "\\"

    
    q_f = process(rf"""Solve the following system of equations: 
$\begin<<cases>>\begin<<array>><<rrr>>{(backslash*2).join([(lambda x:"".join(x[:5])+rf"&"+"&".join(x[5:]))(row(f_sys[r, :]).split("&")) for r in range(shape(f_sys)[0])])}\\{latex(f_expr_lhs)}&=&{latex(f_expr_rhs)}\end<<array>>\end<<cases>>$
""".replace("frac", "dfrac"))
    a_f = process(rf"""
The first three equations of the given system is obtained by subtituting $a={roots[f_idx]}$ and $b={latex(f_b)}$ into $(E)$.
Hence, by putting $x={latex(together(f_sols[0]))}$, $y={latex(together(f_sols[1]))}$ and $z={latex(together(f_sols[2]))}$ into the fourth equation, we have \
${latex(f_expr_lhs.subs(x, f_sols[0]).subs(y, f_sols[1]).subs(z, f_sols[2]))}={latex(f_expr_rhs)}$, \
or ${latex(collect(f_sub_expr, t))}=0$. \
Solving, we have {result}
""".replace("frac", "dfrac"))

else:
    q_f = "This part was not generated."
    a_f = "This part was not generated."

f.write("\n\n(f) " + q_f + "\n\n" + a_f)  

print("══════════════════════ Part (g) ══════════════════════")
while ((g_a := random.randint(-5, 5)) in roots): pass
g_b = Rational(random.randint(-9, 9), random.randint(1, 5))
g_sys = M.subs(a, g_a).col_insert(3, rhs).subs(b, g_b)
g_sys[b_idx, :] = g_sys[b_idx, :] * g_b.q 
print(unique_sol.T, g_a, g_b)
g_sol = list(unique_sol.subs(a, g_a).subs(b, g_b))
print(b_idx)
pprint(g_sys)
print(g_sol)
g_coeffs =  min([[random.randint(-9, 9) for _ in range(3)] for _ in range(14)], 
    key=lambda x: (temp := fraction(sum([a*b for a,b in zip(g_sol,x)])), abs(temp[0])*1e-3+temp[1])[-1])
g_rhs = sum([a*b for a,b in zip(g_sol,g_coeffs)])
if abs(g_rhs) > 24 or fraction(g_rhs)[1] != 1:
    g_equal = False
    g_rhs = random.randint(-24, 24)
else:
    g_equal = True
print(g_coeffs, g_rhs, g_equal)

q_g = process(rf"Is the following system of linear equations consistent? Explain your answer." + "\n" + rf"$${print_sys(g_sys.row_insert(3, Matrix([g_coeffs + [g_rhs]])))}$$")
a_g = process(rf"""The first three equations of the given system is obtained by subtituting $a={g_a}$ and $b={latex(g_b)}$ into $(E)$. \
Hence, $(x,y,z)=\left({",".join([latex(sol) for sol in g_sol])}\right)$ by (a). \
Substituting $(x,y,z)$ into the fourth equation, we find that the left {"matches" if g_equal else "does not match"} the right. \
Hence, the system is {"consistent" if g_equal else "inconsistent"}.
""".replace("frac", "dfrac"))

f.write("\n\n(g) " + q_g + "\n\n" + a_g)  