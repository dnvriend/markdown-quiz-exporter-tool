# LaTeX Math Formula Support - Research and Options

## Research Date
2025-12-31

## Current HTML Quiz Implementation

The quiz HTML generator currently uses:
- **marked.js** (v11.1.1) - Markdown to HTML conversion
- **highlight.js** (v11.9.0) - Code syntax highlighting
- **Tailwind CSS** (via CDN) - Styling
- All content (questions, answers, explanations) passes through `renderMarkdown()` which uses marked.js

All libraries are loaded via CDN, and the output is a self-contained HTML file that can be opened offline.

## LaTeX Syntax to Support

### Inline Math (within text)
| Delimiter | Style | Example |
|-----------|-------|---------|
| `$ ... $` | TeX-style | `The value $x = 5$ is correct` |
| `\( ... \)` | LaTeX-style | `The value \(x = 5\) is correct` |

### Block/Display Math (centered on own line)
| Delimiter | Style | Example |
|-----------|-------|---------|
| `$$ ... $$` | TeX-style | `$$\int_0^1 x^2 dx$$` |
| `\[ ... \]` | LaTeX-style | `\[ \int_0^1 x^2 dx \]` |

## Comparison: KaTeX vs MathJax

### KaTeX
**Pros:**
- **Faster rendering** - Synchronous, no page reflows
- **Smaller bundle size** - ~200KB vs MathJax's ~500KB+
- **Better performance** for large numbers of equations
- **Simpler API** for browser usage

**Cons:**
- Fewer LaTeX features supported (but covers most common use cases)
- Some advanced environments not available

**Latest Version:** 0.16.22 (via jsDelivr CDN)

### MathJax
**Pros:**
- **Broader LaTeX feature support** - More environments and commands
- **Better accessibility** support
- More extensible

**Cons:**
- Larger bundle size
- Slower initial rendering
- More complex configuration

**Latest Version:** 3.x (via jsDelivr CDN)

## Recommended Option: KaTeX

For a quiz HTML generator, **KaTeX is recommended** because:
1. Faster rendering - important for smooth quiz experience
2. Smaller footprint - HTML files stay reasonably sized
3. Self-contained offline use - KaTeX fonts can be embedded
4. Covers 99% of typical math notation needs

## Integration Approaches

### Option 1: KaTeX Auto-Render Extension (Recommended)

**How it works:** After marked.js renders markdown, KaTeX scans the resulting HTML for LaTeX delimiters and renders them.

**CDN Links (KaTeX v0.16.22):**
```html
<!-- CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css">

<!-- Core library -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.js"></script>

<!-- Auto-render extension -->
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/contrib/auto-render.min.js"></script>
```

**Implementation:**
```javascript
// Call after page content is rendered
renderMathInElement(element, {
    delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false},
        {left: '\\(', right: '\\)', display: false},
        {left: '\\[', right: '\\]', display: true}
    ],
    throwOnError: false,
    ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option']
});
```

**Pros:**
- Simplest implementation - no marked.js extension needed
- Works with existing `renderMarkdown()` function
- Auto-render ignores code blocks by default
- Delimiters configurable

**Cons:**
- Two-pass rendering (markdown → HTML, then LaTeX render)
- Potential delimiter conflicts with markdown syntax

### Option 2: marked-katex-extension

**How it works:** A marked.js extension that processes LaTeX before markdown rendering.

**CDN Link:**
```html
<script src="https://cdn.jsdelivr.net/npm/marked-katex-extension@5.1.6/lib/index.umd.js"></script>
```

**Implementation:**
```javascript
import { marked } from 'marked';
import { markedKatex } from 'marked-katex-extension';

marked.use(markedKatex({
    throwOnError: false,
    displayMode: false,
    output: 'html'
}));
```

**Pros:**
- Single-pass rendering
- Better control over rendering order
- No delimiter conflicts

**Cons:**
- Requires marked.js v5+ (currently using v11.1.1, so compatible)
- More complex integration
- Another dependency to manage

### Option 3: MathJax with Post-Processing

**How it works:** Similar to KaTeX auto-render, but using MathJax.

**CDN Links:**
```html
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

**Pros:**
- Broader LaTeX support
- Good for advanced math notation

**Cons:**
- Larger file size
- Slower rendering
- May be overkill for quiz use case

## Recommended Implementation

**Use Option 1: KaTeX Auto-Render Extension**

This provides the best balance of simplicity, performance, and functionality for the quiz HTML generator.

### Integration Steps

1. **Add KaTeX CDN links** to `_build_head()` method in `quiz_html.py`
2. **Add a new method** `_render_latex(element)` in the JavaScript section
3. **Call `_render_latex()`** after each content render in `render()`

### Code Changes Required

In `_build_head()` method, add:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/contrib/auto-render.min.js"></script>
```

In JavaScript section, add to `render()` method or as a new method:
```javascript
renderLatex() {
    if (typeof renderMathInElement !== 'undefined') {
        const app = document.getElementById('app');
        renderMathInElement(app, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
            ],
            throwOnError: false,
            ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option']
        });
    }
}
```

Call `this.renderLatex()` at the end of the `render()` method, after `this.attachEventListeners()`.

### Example Quiz Content with LaTeX

```markdown
# Math Quiz

## Question 1
What is the derivative of $f(x) = x^2$?

- $f'(x) = x$
- $f'(x) = 2x$ (correct)
- $f'(x) = x^2$

**Reason:** Using the power rule, $\frac{d}{dx}x^n = nx^{n-1}$, so:
$$
\frac{d}{dx}x^2 = 2x^{2-1} = 2x
$$

## Question 2
Evaluate the integral:
$$
\int_0^1 x^2 \, dx
$$

- $0$
- $\frac{1}{2}$ (correct)
- $1$

**Reason:** Using integration:
\[
\int_0^1 x^2 \, dx = \left[\frac{x^3}{3}\right]_0^1 = \frac{1}{3} - 0 = \frac{1}{3}
\]
```

## Offline Considerations

For fully offline HTML files:

1. **KaTeX fonts** need to be embedded or the HTML requires internet connection
2. **Alternative:** Bundle KaTeX fonts as base64 data URIs in the CSS
3. **Current approach:** The quiz HTML already requires CDN for marked.js, highlight.js, and Tailwind CSS

If true offline capability is required:
- Download and embed KaTeX CSS with fonts as data URIs (~300KB additional)
- This would make HTML files larger but truly offline-capable

## Sources

- [KaTeX Official Documentation](https://katex.org/)
- [KaTeX Auto-render Extension](https://katex.org/docs/autorender.html)
- [KaTeX Browser Usage](https://katex.org/docs/browser.html)
- [marked-katex-extension on npm](https://www.npmjs.com/package/marked-katex-extension)
- [marked-katex-extension on GitHub](https://github.com/UziTech/marked-katex-extension)
- [MathJax Official Documentation](https://www.mathjax.org/)
- [MathJax Delimiters Documentation](https://docs.mathjax.org/en/latest/input/tex/delimiters.html)
- [KaTeX vs MathJax Comparison (2025)](https://biggo.com/news/202511040733_KaTeX_MathJax_Web_Rendering_Comparison)
- [Marked.js with KaTeX Tutorial](https://blog.woooo.tech/posts/marked_with_katex/)
- [Marked.js Advanced Usage](https://marked.js.org/using_advanced)
