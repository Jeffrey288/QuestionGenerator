import numpy as np
import random

def vector_proj():
    def is_int(x): return (abs(x - int(x)) < 1e-6)
    
    def printVec(v):
        res = ""
        first = "i"
        for x, c in zip(v, ["i", "j", "k"]):
            if x == 0: 
                if c == first: first = chr(ord(first) + 1)
            elif x == -1: res += rf"-\mathbf<<{c}>>"
            elif x == 1 and c == first: res += rf"\mathbf<<{c}>>"
            elif x == 1: res += rf"+\mathbf<<{c}>>"
            elif c == first: res += rf"{int(x)}\mathbf<<{c}>>"
            else: res += rf"{int(x):+}\mathbf<<{c}>>"
        return res

    def printSquareRoot(x):
        if is_int(x): return str(int(x))
        else: return rf"\sqrt<<{int(round(x**2))}>>"

    def printSquare(x):
        if (x < 0): return "(" + str(int(x)) + ")^2"
        else: return str(int(x)) + "^2"

    while True:
        A = np.random.randint(24, size=(3)) - 12
        B = np.random.randint(24, size=(3)) - 12
        C = np.random.randint(24, size=(3)) - 12
        if (A[0] == B[0] or B[0] == C[0] or A[0] == C[0]): continue
        if (A[1] == B[1] or B[1] == C[1] or A[1] == C[1]): continue
        if (A[2] == B[2] or B[2] == C[2] or A[2] == C[2]): continue
        temp = np.cross(B-A, C-B)
        # if (abs(temp[0]) + abs(temp[1]) + abs(temp[2]) > 80): continue
        n = np.cross(A-B, A-C)
        gcd = np.gcd.reduce(n)
        if (gcd == 0): continue
        n = n / gcd
        if (np.linalg.norm(n) > 13): continue
        D = (A + B)/2 # can change to other two points
        if (not is_int(D[0])): continue
        if (not is_int(D[1])): continue
        if (not is_int(D[2])): continue
        E = D + n * random.choice([1, -1])
        AE = E - A
        DE = np.dot(AE, n) / (np.linalg.norm(n) ** 2) * n
        cos_angle = np.dot(AE, n) / np.linalg.norm(n) / np.linalg.norm(AE)
        angle = 180 / 3.1415926 * np.arccos(cos_angle)
        plane_angle = abs(90 - angle)
        if (plane_angle < 10 or plane_angle > 85): continue
        distance = np.linalg.norm(DE)
        F = D - n
        AB = B-A
        BC = C-B
        cross = np.cross(AB, BC)
        temp = rf"Since $\theta>90^\circ$, the angle between $\vec<<AE>>$ and $\Pi$ $=\theta-90^\circ={angle:.6f}^\circ-90^\circ={plane_angle:.1f}^\circ$" if angle>90 else \
                rf"Since $\theta<90^\circ$, the angle between $\vec<<AE>>$ and $\Pi$ $=90^\circ-\theta=90^\circ-{angle:.6f}^\circ={plane_angle:.1f}^\circ$" 
    
        res = {
            "num_questions": 5,
            "question": rf"""
It is given that $\vec<<OA>>={printVec(A)}$,  $\vec<<OB>>={printVec(B)}$,  $\vec<<OC>>={printVec(C)}$ and $\vec<<OD>>={printVec(E)}$. $A$, $B$ and $C$ lie on the same plane $\Pi$, and the projection of $D$ on $\Pi$ is $E$.
""",
"q1":rf"Evaluate $\vec<<AB>>\times\vec<<BC>>$.",
"q2":rf"Find $\vec<<AE>>$.",
"q3":rf"Find the distance between $D$ and $\Pi$.",
"q4":rf"Find the angle between $AE$ and $\Pi$.",
"q5":rf"$D$ is reflected about the plane $\Pi$ to $F$. Find $\vec<<OF>>$.",
            "a1": rf"""
**Answer**: ${printVec(np.cross(B-A, C-B))}$

$$\begin<<aligned>>
\vec<<AB>>\times\vec<<BC>> &= ({printVec(B-A)})\times({printVec(C-B)}) \\
&=
\begin<<vmatrix>>
\mathbf<<i>> & \mathbf<<j>> & \mathbf<<k>> \\ 
{int(AB[0])} & {int(AB[1])} & {int(AB[2])} \\ 
{int(BC[0])} & {int(BC[1])} & {int(BC[2])}
\end<<vmatrix>> \\
&= 
\begin<<vmatrix>>  {int(AB[1])}& {int(BC[1])}\\  {int(AB[2])}& {int(BC[2])}\end<<vmatrix>>\mathbf<<i>>
- \begin<<vmatrix>>  {int(AB[0])}& {int(BC[0])}\\  {int(AB[2])}& {int(BC[2])} \end<<vmatrix>>\mathbf<<j>>
+ \begin<<vmatrix>>  {int(AB[0])}& {int(BC[0])}\\  {int(AB[1])}& {int(BC[1])} \end<<vmatrix>>\mathbf<<k>> \\
&= {printVec(np.cross(B-A, C-B))} \\
\end<<aligned>>$$ 
""",
            "a2": rf"""
**Answer**: ${printVec(D-A)}$

$\vec<<ED>>$ is the projection of $\vec<<AE>>$ on $\vec<<AB>>\times\vec<<BC>>$, so
$$\begin<<aligned>>
\vec<<ED>> &= \dfrac<<\vec<<AE>>\cdot\left(\vec<<AB>>\times\vec<<BC>>\right)>><<\left|\vec<<AB>>\times\vec<<BC>>\right|^2>>\left(\vec<<AB>>\times\vec<<BC>>\right) \\
&= \dfrac<<({int((D-A)[0])})({cross[0]})+({int((D-A)[1])})({cross[1]})+({int((D-A)[2])})({cross[2]})>><<{printSquare(cross[0])}+{printSquare(cross[1])}+{printSquare(cross[2])}>>({printVec(cross)}) \\
&= {printVec(E-D)}
\end<<aligned>>$$ 
Hence,
$$\begin<<aligned>>
\vec<<AE>> &= \vec<<AD>> - \vec<<ED>> \\
    &= ({printVec(E-A)}) - ({printVec(E-D)}) \\
        &= {printVec(D-A)}
\end<<aligned>>$$ 
""",
            "a3": rf"""
**Answer**: ${printSquareRoot(distance)}$

The distance $=\left|\vec<<ED>>\right|=\sqrt<<{printSquare((E-D)[0])}+{printSquare((E-D)[1])}+{printSquare((E-D)[2])}>>={printSquareRoot(distance)}$.
""",
            "a4": rf"""
**Answer**: ${plane_angle:.1f}^\circ$

The angle between $\vec<<AE>>$ on $\vec<<AB>>\times\vec<<BC>>$, which we denote as $\theta$, is given by
$$\begin<<aligned>>
\cos<<\theta>> &= \dfrac<<\vec<<AE>>\cdot\left(\vec<<AB>>\times\vec<<BC>>\right)>><<\left|\vec<<AE>>\right|\left|\vec<<AB>>\times\vec<<BC>>\right|>> \\
&= \dfrac<<({int((D-A)[0])})({cross[0]})+({int((D-A)[1])})({cross[1]})+({int((D-A)[2])})({cross[2]})>><<\sqrt<<{printSquare(cross[0])}+{printSquare(cross[1])}+{printSquare(cross[2])}>>\sqrt<<{printSquare((D-A)[0])}+{printSquare((D-A)[1])}+{printSquare((D-A)[2])}>>>>({printVec(cross)}) \\
&\approx {cos_angle:.6f}\\
    \theta&= {angle:.6f}^\circ
\end<<aligned>>$$ 

{temp}.
""",
            "a5": rf"""
**Answer**: ${printVec(F)}$

$$\begin<<aligned>>
\vec<<EF>> &= -\vec<<ED>> \\
    &= {printVec(D-E)} \\
\vec<<OF>> &= \vec<<OA>> + \vec<<AE>> + \vec<<EF>> \\
    &= ({printVec(A)}) + ({printVec(D-A)}) + ({printVec(D-E)}) \\
        &= {printVec(F)}
\end<<aligned>>$$ 
"""
        }

        for k in res.keys():
            if (k != "num_questions"):
                res[k] = res[k].replace("<<", "{").replace(">>", "}").replace(r"\vec", r"\overrightarrow")
        
        return res


if __name__ == "__main__":
    # from markdown import markdown
    # temp = vector_proj()
    # for k in temp.keys():
    #     if (k != "num_questions"):
    #         temp[k] = markdown(temp[k])
    # print(temp)

    import regex as re
    def temp(match_obj):
        print(match_obj, "\n-------\n")
        print(match_obj.group(2), "\n-------\n")
        return rf"\({match_obj.group(2)}\)"
    print(re.sub(r"(\$\$)([^\$]+)(\$\$)", temp, r"""<p><strong>Answer</strong>: $2\mathbf{i}+2\mathbf{j}+2\mathbf{k}$</p>
<p>$\overrightarrow{ED}$ is the projection of $\overrightarrow{AE}$ on $\overrightarrow{AB}\times\overrightarrow{BC}$, so
$$\begin{aligned}
\overrightarrow{ED} &amp;= \dfrac{\overrightarrow{AE}\cdot\left(\overrightarrow{AB}\times\overrightarrow{BC}\right)}{\left|\overrightarrow{AB}\times\overrightarrow{BC}\right|^2}\left(\overrightarrow{AB}\times\overrightarrow{BC}\right) \
&amp;= \dfrac{(2)(24)+(2)(16)+(2)(-40)}{24^2+16^2+(-40)^2}(24\mathbf{i}+16\mathbf{j}-40\mathbf{k}) \
&amp;= -3\mathbf{i}-2\mathbf{j}+5\mathbf{k}
\end{aligned}$$
Hence,
$$\begin{aligned}
\overrightarrow{AE} &amp;= \overrightarrow{AD} - \overrightarrow{ED} \
    &amp;= (-\mathbf{i}+7\mathbf{k}) - (-3\mathbf{i}-2\mathbf{j}+5\mathbf{k}) \
        &amp;= 2\mathbf{i}+2\mathbf{j}+2\mathbf{k}
\end{aligned}$$ </p>
"""))

    

