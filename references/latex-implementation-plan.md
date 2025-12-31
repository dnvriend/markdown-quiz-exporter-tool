# LaTeX Support Implementation Plan

## Summary

Add KaTeX rendering support to HTML quiz output for inline (`$...$`) and block (`$$...$$`) math formulas in questions, answers, and explanations.

## Approach

**Selected: KaTeX Auto-Render Extension (Option 1 from research)**

Rationale:
- Minimal code changes (add CDN links + one method call)
- Works with existing marked.js pipeline (post-processing)
- Lighter than MathJax (~200KB vs ~500KB)
- Synchronous rendering = no layout shifts

## Implementation Steps

### Step 1: Add KaTeX CDN links to `_build_head()`

Add after the highlight.js stylesheet links in `quiz_html.py`:

```html
<!-- KaTeX for LaTeX math rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/contrib/auto-render.min.js"></script>
```

### Step 2: Add `renderLatex()` method to QuizApp class

Add after the `renderMarkdown()` method in the JavaScript section:

```javascript
// Utility: Render LaTeX math formulas
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

### Step 3: Call `renderLatex()` after DOM updates

Modify the `render()` method to call `renderLatex()` after `attachEventListeners()`:

```javascript
render() {
    const app = document.getElementById('app');

    // ... existing page rendering ...

    // Attach event listeners after rendering
    this.attachEventListeners();

    // Render LaTeX formulas
    this.renderLatex();
}
```

### Step 4: Add KaTeX-specific CSS for dark mode support

Add to `_build_styles()` method:

```css
/* KaTeX dark mode support */
.dark .katex {
    color: #e5e7eb;
}
```

## Files to Modify

| File | Changes |
|------|---------|
| `markdown_quiz_exporter_tool/quiz_html.py` | Add CDN links, renderLatex() method, CSS, render() call |

## Testing

1. Create test quiz with LaTeX content:
   - Inline math in question: `What is $x^2$ when $x = 3$?`
   - Block math in question: `$$\int_0^1 x^2 dx$$`
   - Math in answers: `$f(x) = 2x$`
   - Math in explanation with block formula

2. Verify rendering in both light and dark mode

3. Verify code blocks are not affected (LaTeX should ignore `<pre>` and `<code>` tags)

## Example Test Content

```markdown
# Math Quiz

## Question 1
What is the derivative of $f(x) = x^3$?

- $f'(x) = x^2$
- $f'(x) = 3x^2$ (correct)
- $f'(x) = 3x$

**Reason:** Using the power rule:
$$\frac{d}{dx}x^n = nx^{n-1}$$

Therefore $\frac{d}{dx}x^3 = 3x^{3-1} = 3x^2$.
```

## Supported Delimiters

| Delimiter | Type | Example |
|-----------|------|---------|
| `$...$` | Inline | `$x^2$` renders inline |
| `$$...$$` | Block | `$$\int x dx$$` renders centered |
| `\(...\)` | Inline | `\(x^2\)` alternative syntax |
| `\[...\]` | Block | `\[\int x dx\]` alternative syntax |

## Notes

- The `defer` attribute on KaTeX scripts means they load after HTML parsing
- `renderLatex()` checks if `renderMathInElement` is defined before calling
- Code blocks (`<pre>`, `<code>`) are automatically ignored by KaTeX auto-render
- No changes needed to quiz parser - LaTeX delimiters pass through as-is
