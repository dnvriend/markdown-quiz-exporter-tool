---
description: Generate interactive HTML quiz from markdown
argument-hint: input.md output.html
---

Generate self-contained interactive HTML quiz page.

## Usage

```bash
markdown-quiz-exporter-tool quiz-html INPUT.md OUTPUT.html --title "TITLE" [OPTIONS]
```

## Arguments

- `INPUT.md`: Quiz markdown file (required)
- `OUTPUT.html`: Output HTML file (required)
- `--title "TITLE"`: Quiz title (required)
- `--force` / `-f`: Overwrite existing file
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Generate quiz HTML
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "My Quiz"

# Overwrite existing
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "Quiz" --force

# With verbose output
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "Quiz" -vv
```

## Output

Self-contained HTML with embedded quiz, CSS, and JavaScript.
