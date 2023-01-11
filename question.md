Consider the following system of linear equations in $x$, $y$ and $z$:
$$(E): \begin{cases}\begin{array}{rrrrrrr}x&-&y&-&z&=&1\\4x&-&4y&+&(- a - 7)z&=&b\\(a + 5)x&-&4y&&&=&2\end{array}\end{cases}$$

(a)	If $(E)$ has a unique solution, find the range of values of $a$.

$(E)$ has a unique solution \
⇔ $\Delta\neq0$ \
⇔ $\left|\begin{matrix}1 & -1 & -1\\4 & -4 & - a - 7\\a + 5 & -4 & 0\end{matrix}\right|\neq0$ \
⇔ $a^{2} + 4 a + 3\neq0$ \
⇔ $\left(a + 1\right) \left(a + 3\right)\neq0$ \
⇔ $a\neq-1$ and $a\neq-3$

(b)	Solve $(E)$ for the range of values found in (a).

$$\begin{aligned}
x&=\dfrac{\left|\begin{matrix}1 & -1 & -1\\b & -4 & - a - 7\\2 & -4 & 0\end{matrix}\right|}{\Delta}=\dfrac{- 2 a + 4 b - 22}{\Delta}\\
&=- \frac{2 \left(a - 2 b + 11\right)}{\left(a + 1\right) \left(a + 3\right)}\\
y&=\dfrac{\left|\begin{matrix}1 & 1 & -1\\4 & b & - a - 7\\a + 5 & 2 & 0\end{matrix}\right|}{\Delta}=\dfrac{- a^{2} + a b - 10 a + 5 b - 29}{\Delta}\\
&=- \frac{a^{2} - a b + 10 a - 5 b + 29}{\left(a + 1\right) \left(a + 3\right)}\\
z&=\dfrac{\left|\begin{matrix}1 & -1 & 1\\4 & -4 & b\\a + 5 & -4 & 2\end{matrix}\right|}{\Delta}=\dfrac{- a b + 4 a - b + 4}{\Delta}\\
&=- \frac{b - 4}{a + 3}
\end{aligned}$$


(c) For each of the following cases, find the range of values of b such that $(E)$ is consistent, and solve $(E)$ for such values of $b$ (if they exist). \
(i) $a=-1$\
(ii) $a=-3$ 


(i) When $a=-1$, the augmented matrix of (E) becomes
$$\left(\begin{array}{ccc|c}1 & -1 & -1 & 1\\4 & -4 & -6 & b\\4 & -4 & 0 & 2\end{array}\right)\sim\left(\begin{array}{ccc|c}1 & -1 & -1 & 1\\0 & 0 & -2 & b - 4\\0 & 0 & 0 & 4 b - 20\end{array}\right)$$

$(E)$ is consistent when $b=5$.

Therefore, the solution set is $\left\{\left(\dfrac{2 t + 1}{2},\:t,\:- \dfrac{1}{2}\right):t\in\mathbb{R}\right\}$.

(ii) When $a=-3$, the augmented matrix of (E) becomes
$$\left(\begin{array}{ccc|c}1 & -1 & -1 & 1\\4 & -4 & -4 & b\\2 & -4 & 0 & 2\end{array}\right)\sim\left(\begin{array}{ccc|c}1 & -1 & -1 & 1\\0 & -2 & 2 & 0\\0 & 0 & 0 & b - 4\end{array}\right)$$

$(E)$ is consistent when $b=4$.

Therefore, the solution set is $\left\{\left(2 t + 1,\:t,\:t\right):t\in\mathbb{R}\right\}$.



(d) Find the least value of $2 x^{2} + x z - z^{2}$, where $x, y, z$ are real numbers satisfying

$\begin{cases}\begin{array}{rrrrrrr}x&-&y&-&z&=&1\\4x&-&4y&-&4z&=&4\\2x&-&4y&&&=&2\end{array}\end{cases}$.

The given system is obtained by substituting $a=-3$ and $b=4$ into $(E)$.\
Hence, by putting $x=2 t + 1$, $y=t$ and $z=t$ into the given expression, we have
$$\begin{aligned}
    2 x^{2} + x z - z^{2}&=- t^{2} + t \left(2 t + 1\right) + 2 \left(2 t + 1\right)^{2}
        \\&=9 t^{2} + 9 t + 2
        \\&=9 \left(t + \dfrac{1}{2}\right)^{2} - \dfrac{1}{4}
\end{aligned}$$
Hence, the least value of $2 x^{2} + x z - z^{2}$ is $- \dfrac{1}{4}$.
    

(e) This part was not generated.

This part was not generated.

(f) Solve the following system of equations: 
$\begin{cases}\begin{array}{rrr}x-y-z&=&1\\4x-4y-6z&=&5\\4x-4y&=&2\\2 x z + 5 y^{2} + 2 z^{2}&=&4\end{array}\end{cases}$



The first three equations of the given system is obtained by subtituting $a=-1$ and $b=5$ into $(E)$.
Hence, by putting $x=\dfrac{2 t + 1}{2}$, $y=t$ and $z=- \dfrac{1}{2}$ into the fourth equation, we have\
$5 t^{2} - t=4$,\
or $5 t^{2} - t - 4=0$.\
Solving, we have $t = - \dfrac{4}{5}$ or $1$, and $(x, y, z) = \left(- \dfrac{3}{10},- \dfrac{4}{5},- \dfrac{1}{2}\right)$ or $\left(\dfrac{3}{2},1,- \dfrac{1}{2}\right)$.


(g) Is the following system of linear equations consistent? Explain your answer.
$$\begin{cases}\begin{array}{rrrrrrr}x&-&y&-&z&=&1\\8x&-&8y&-&24z&=&3\\10x&-&4y&&&=&2\\9x&+&9y&+&5z&=&-20\end{array}\end{cases}$$

The first three equations of the given system is obtained by subtituting $a=5$ and $b=\dfrac{3}{2}$ into $(E)$.\
Hence, $(x,y,z)=\left(- \dfrac{13}{24},- \dfrac{89}{48},\dfrac{5}{16}\right)$ by (a).\
Substituting $(x,y,z)$ into the fourth equation, we find that the left matches the right.\
Hence, the system is consistent.\
