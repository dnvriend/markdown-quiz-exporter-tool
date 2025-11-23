---
description: Validate quiz markdown file format
argument-hint: input.md
---

Validate quiz markdown file format and show statistics.

## Usage

```bash
markdown-quiz-exporter-tool validate INPUT.md [OPTIONS]
```

## Arguments

- `INPUT.md`: Quiz markdown file to validate (required)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Basic validation
markdown-quiz-exporter-tool validate quiz.md

# With verbose output for debugging
markdown-quiz-exporter-tool validate quiz.md -vv
```

## Output

### On Success

Shows statistics about the quiz:
- Total question count
- Single choice vs multiple choice breakdown
- Answer statistics (total, average per question, correct count)
- Explanation coverage

### On Error

Shows detailed error information:
- Exact line number where error occurred
- Problematic line content
- Context lines (2 before, 2 after)
- Clear error message with fix suggestions
- Question block number

## Common Errors

**Mixed answer types:**
```
Error at line 5: Cannot mix ( ) and [ ] formats in same question
```
Fix: Use consistent format - either `( )` for single choice OR `[ ]` for multiple choice

**No correct answer:**
```
Error at line 3: No correct answer marked. Use (X) or [X]
```
Fix: Mark at least one answer with `(X)` or `[X]`

**No answers found:**
```
Error at line 2: No answers found. Expected format: '- (X) text'
```
Fix: Add answer options in format `- (X) answer` or `- [X] answer`

**No question text:**
```
Error at line 1: No question text found
```
Fix: Add question text before answer options
