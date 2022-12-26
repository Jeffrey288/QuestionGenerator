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