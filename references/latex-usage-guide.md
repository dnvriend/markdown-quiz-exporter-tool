# LaTeX Math Support in Quiz HTML

The HTML quiz generator supports LaTeX math formulas using KaTeX for rendering.

## Syntax

### Inline Math

Use single dollar signs for inline formulas within text:

```markdown
The quadratic formula is $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ for solving equations.
```

Alternative syntax with backslash parentheses:

```markdown
The area is \(A = \pi r^2\) square units.
```

### Block/Display Math

Use double dollar signs for centered, standalone formulas:

```markdown
$$
\int_0^1 x^2 \, dx = \frac{1}{3}
$$
```

Alternative syntax with backslash brackets:

```markdown
\[
E = mc^2
\]
```

## Where LaTeX Works

LaTeX rendering works in all content areas:

| Location | Example |
|----------|---------|
| Question text | `What is $\frac{d}{dx}x^2$?` |
| Answer options | `- $2x$ (correct)` |
| Explanations | `**Reason:** Using $\frac{d}{dx}x^n = nx^{n-1}$...` |

## Common Formulas

### Fractions

```latex
$\frac{a}{b}$           # Simple fraction
$\dfrac{a}{b}$          # Display-style fraction (larger)
```

### Exponents and Subscripts

```latex
$x^2$                   # Superscript
$x_i$                   # Subscript
$x_i^2$                 # Both
$e^{i\pi}$              # Grouped exponent
```

### Greek Letters

```latex
$\alpha, \beta, \gamma, \delta$
$\pi, \sigma, \mu, \lambda$
$\Sigma, \Pi, \Omega$   # Capital letters
```

### Roots

```latex
$\sqrt{x}$              # Square root
$\sqrt[3]{x}$           # Cube root
$\sqrt[n]{x}$           # nth root
```

### Sums and Products

```latex
$\sum_{i=1}^{n} x_i$    # Summation
$\prod_{i=1}^{n} x_i$   # Product
```

### Integrals

```latex
$\int x \, dx$          # Indefinite integral
$\int_a^b f(x) \, dx$   # Definite integral
$\iint$, $\iiint$       # Multiple integrals
```

### Limits

```latex
$\lim_{x \to \infty} f(x)$
$\lim_{n \to 0}$
```

### Trigonometry

```latex
$\sin, \cos, \tan$
$\arcsin, \arccos, \arctan$
$\sin^2(x) + \cos^2(x) = 1$
```

### Matrices

```latex
$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$
```

### Aligned Equations

```latex
$$
\begin{aligned}
f(x) &= x^2 + 2x + 1 \\
     &= (x + 1)^2
\end{aligned}
$$
```

## Code Blocks Are Safe

LaTeX delimiters inside code blocks are ignored:

```markdown
Here is code: `$variable = 5`

And a code block:
```python
price = 100
tax = price * 0.21  # $21
```
```

The `$` signs in code are not rendered as math.

## Tips

1. **Spacing in integrals**: Use `\,` for thin space before `dx`: `$\int x \, dx$`
2. **Text in formulas**: Use `\text{}`: `$P(\text{rain}) = 0.3$`
3. **Multiplication**: Use `\times` or `\cdot`: `$3 \times 4$` or `$3 \cdot 4$`
4. **Approximately equal**: Use `\approx`: `$\pi \approx 3.14$`
5. **Not equal**: Use `\neq`: `$x \neq 0$`
6. **Percent sign**: Avoid `%` in formulas - KaTeX has issues with it. Write `$\times 100$` instead of `$\times 100\%$`, or describe percentage in text

## Limitations

- Some advanced LaTeX packages are not supported
- Very complex equations may render slowly
- Equation numbering is not supported
- Cross-references to equations are not supported

## References

- [KaTeX Supported Functions](https://katex.org/docs/supported.html)
- [KaTeX Support Table](https://katex.org/docs/support_table.html)
