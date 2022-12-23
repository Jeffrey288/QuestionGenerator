
It is given that $\overrightarrow{OA}=-3\mathbf{i}+2\mathbf{j}-5\mathbf{k}$,  $\overrightarrow{OB}=5\mathbf{i}-11\mathbf{k}$,  $\overrightarrow{OC}=-12\mathbf{i}+\mathbf{j}+5\mathbf{k}$ and $\overrightarrow{OD}=-9\mathbf{k}$. $A$, $B$ and $C$ lie on the same plane $\Pi$, and the projection of $D$ on $\Pi$ is $E$.
1. Evaluate $\overrightarrow{AB}\times\overrightarrow{BC}$.
2. Find $\overrightarrow{AE}\cdot(\overrightarrow{AB}\times\overrightarrow{BC})$.
3. Find the distance between $D$ and $\Pi$.
4. Find the angle between $AE$ and $\Pi$.
5. $D$ is reflected about the plane $\Pi$ to $F$. Find $\overrightarrow{OF}$.

Solutions
1. $-26\mathbf{i}-26\mathbf{j}-26\mathbf{k}$
$$\begin{aligned}
\overrightarrow{AB}\times\overrightarrow{BC} &= (8\mathbf{i}-2\mathbf{j}-6\mathbf{k})\times(-17\mathbf{i}+\mathbf{j}+16\mathbf{k}) \\
&=
\begin{vmatrix}
\mathbf{i} & \mathbf{j} & \mathbf{k} \\ 
8 & -2 & -6 \\ 
-17 & 1 & 16
\end{vmatrix} \\
&= 
\begin{vmatrix}  -2& 1\\  -6& 16\end{vmatrix}\mathbf{i}
- \begin{vmatrix}  8& -17\\  -6& 16 \end{vmatrix}\mathbf{j}
+ \begin{vmatrix}  8& -17\\  -2& 1 \end{vmatrix}\mathbf{k} \\
&= -26\mathbf{i}-26\mathbf{j}-26\mathbf{k} \\
\end{aligned}$$ 

2. $4\mathbf{i}-\mathbf{j}-3\mathbf{k}$

$\overrightarrow{ED}$ is the projection of $\overrightarrow{AE}$ on $\overrightarrow{AB}\times\overrightarrow{BC}$, so
$$\begin{aligned}
\overrightarrow{ED} &= \dfrac{\overrightarrow{AE}\cdot\left(\overrightarrow{AB}\times\overrightarrow{BC}\right)}{\left|\overrightarrow{AB}\times\overrightarrow{BC}\right|^2}\left(\overrightarrow{AB}\times\overrightarrow{BC}\right) \\
&= \dfrac{(4)(-26)+(-1)(-26)+(-3)(-26)}{(-26)^2+(-26)^2+(-26)^2}(-26\mathbf{i}-26\mathbf{j}-26\mathbf{k}) \\
&= -\mathbf{i}-\mathbf{j}-\mathbf{k}
\end{aligned}$$ 
Hence,
$$\begin{aligned}
\overrightarrow{AE} &= \overrightarrow{AD} - \overrightarrow{ED} \\
    &= (3\mathbf{i}-2\mathbf{j}-4\mathbf{k}) - (-\mathbf{i}-\mathbf{j}-\mathbf{k}) \\
        &= 4\mathbf{i}-\mathbf{j}-3\mathbf{k}
\end{aligned}$$ 

3. $\sqrt{3}$

The distance $=\left|\overrightarrow{ED}\right|=\sqrt{(-1)^2+(-1)^2+(-1)^2}=\sqrt{3}$.

4. $18.8^\circ$

The angle between $\overrightarrow{AE}$ on $\overrightarrow{AB}\times\overrightarrow{BC}$, which we denote as $\theta$, is given by
$$\begin{aligned}
\cos{\theta} &= \dfrac{\overrightarrow{AE}\cdot\left(\overrightarrow{AB}\times\overrightarrow{BC}\right)}{\left|\overrightarrow{AE}\right|\left|\overrightarrow{AB}\times\overrightarrow{BC}\right|} \\
&= \dfrac{(4)(-26)+(-1)(-26)+(-3)(-26)}{\sqrt{(-26)^2+(-26)^2+(-26)^2}\sqrt{4^2+(-1)^2+(-3)^2}}(-26\mathbf{i}-26\mathbf{j}-26\mathbf{k}) \\
&\approx 0.321634\\
    \theta&= 71.238245^\circ
\end{aligned}$$ 

Since $\theta<90^\circ$, the angle between $\overrightarrow{AE}$ and $\Pi$ $=90^\circ-\theta=90^\circ-71.238245^\circ=18.8^\circ$.

5. $2\mathbf{i}+2\mathbf{j}-7\mathbf{k}$

$$\begin{aligned}
\overrightarrow{EF} &= -\overrightarrow{ED} \\
    &= \mathbf{i}+\mathbf{j}+\mathbf{k} \\
\overrightarrow{OF} &= \overrightarrow{OA} + \overrightarrow{AE} + \overrightarrow{EF} \\
    &= (-3\mathbf{i}+2\mathbf{j}-5\mathbf{k}) + (4\mathbf{i}-\mathbf{j}-3\mathbf{k}) + (\mathbf{i}+\mathbf{j}+\mathbf{k}) \\
        &= 2\mathbf{i}+2\mathbf{j}-7\mathbf{k}
\end{aligned}$$ 

