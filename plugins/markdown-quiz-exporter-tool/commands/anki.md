---
description: Export quiz to Anki CSV format
argument-hint: input.md output.csv
---

Export quiz markdown to Anki CSV format (AllInOne or Basic).

## Usage

```bash
markdown-quiz-exporter-tool anki INPUT.md OUTPUT.csv [OPTIONS]
```

## Arguments

- `INPUT.md`: Quiz markdown file (required)
- `OUTPUT.csv`: Output CSV file (required)
- `--quiz`: AllInOne quiz format (default)
- `--recall`: Basic recall format
- `--force` / `-f`: Overwrite existing file
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Export as quiz (default)
markdown-quiz-exporter-tool anki quiz.md cards.csv

# Export as recall
markdown-quiz-exporter-tool anki quiz.md cards.csv --recall

# Overwrite existing
markdown-quiz-exporter-tool anki quiz.md cards.csv --force
```

## Output

CSV with AllInOne (quiz) or Basic (recall) format.
