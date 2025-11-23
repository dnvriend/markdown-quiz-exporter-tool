---
description: Export quiz to Flashcard Hero TSV format
argument-hint: input.md output.tsv
---

Export quiz markdown to Flashcard Hero TSV format.

## Usage

```bash
markdown-quiz-exporter-tool flashhero INPUT.md OUTPUT.tsv [OPTIONS]
```

## Arguments

- `INPUT.md`: Quiz markdown file (required)
- `OUTPUT.tsv`: Output TSV file (required)
- `--force` / `-f`: Overwrite existing file
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Basic export
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv

# Overwrite existing
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv --force

# With verbose output
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv -vv
```

## Output

TSV file with: Question<TAB>Answer format.
