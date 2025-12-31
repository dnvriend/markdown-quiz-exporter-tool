# Known Bugs

## BUG-001: Percent sign (`%`) not rendering in LaTeX formulas

**Status:** Open
**Severity:** Low
**Affected:** quiz-html export

### Description

The percent sign (`%`) does not render in LaTeX formulas. When using `\%` in markdown (the standard LaTeX escape for percent), the backslash is lost and KaTeX treats `%` as a comment character, hiding everything after it.

### Example

**Input (markdown):**
```markdown
What is $50\%$ of $200$?
```

**Expected output:**
> What is 50% of 200?

**Actual output:**
> What is 50 of 200?

### Investigation Notes

1. In LaTeX, `%` is a comment character - everything after it on the same line is ignored
2. The standard escape is `\%` which should render as a literal percent sign
3. The markdown file correctly contains `$50\%$`
4. The JSON in HTML shows `$50\\%$` (correct double-escaping for JSON)
5. KaTeX should receive `$50\%$` after JSON parsing
6. However, the `%` and everything after it disappears in the rendered output

### Attempted Solutions (Failed)

| Attempt | Syntax | Result |
|---------|--------|--------|
| Standard escape | `$50\%$` | `%` treated as comment, content lost |
| Text wrapper | `$\text{%}$` | Same issue |
| Space after escape | `$50\% $` | Same issue |

### Possible Causes

1. **Markdown parser interference** - The markdown parser (marked.js) might be consuming or modifying the backslash before KaTeX processes it
2. **JSON double-parsing** - The backslash might need additional escaping (`\\%` in markdown?)
3. **KaTeX auto-render limitation** - The auto-render extension might handle `%` differently than direct KaTeX API calls
4. **Character encoding** - The `%` might need URL encoding in certain contexts

### Workaround

Avoid using `%` in LaTeX formulas. Alternative notations:
- Use `$\times 100$` instead of `$\times 100\%$`
- Write percentage in text: "50 percent" or "(in %)"
- Use decimal notation: `$0.50$` instead of `$50\%$`

### Research Tasks

- [ ] Test with direct KaTeX API call instead of auto-render
- [ ] Check if marked.js is modifying the backslash
- [ ] Try `\\%` in the markdown source (double backslash)
- [ ] Test with marked-katex-extension instead of auto-render
- [ ] Check KaTeX GitHub issues for similar problems
