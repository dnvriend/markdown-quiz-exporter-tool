<div align="center">
  <img src=".github/assets/logo-small.png" alt="markdown-quiz-exporter-tool logo" width="200"/>

  # markdown-quiz-exporter-tool
</div>

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![AI Generated](https://img.shields.io/badge/AI-Generated-blueviolet.svg)](https://www.anthropic.com/claude)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)

A CLI tool that exports the quiz-markdown-format to tools like Anki, Flashcard Hero

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Multi-Level Verbosity Logging](#multi-level-verbosity-logging)
- [Shell Completion](#shell-completion)
- [Development](#development)
- [Testing](#testing)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## About

`markdown-quiz-exporter-tool` is a Python CLI tool built with modern tooling and best practices.

## Features

- 📤 **Export Formats**:
  - Interactive HTML quiz with dark/light mode
  - Flashcard Hero TSV format
  - Anki AllInOne (quiz) format
  - Anki Basic (recall) format
- 🎨 **HTML Quiz Features**:
  - Self-contained single HTML file
  - Dark/light mode with auto-detect
  - Question/answer shuffling
  - Progress tracking and timer
  - Session storage persistence
  - Mobile-responsive design
  - Markdown rendering in explanations
- ✅ Type-safe with mypy strict mode
- ✅ Linted with ruff
- ✅ Tested with pytest
- 📊 Multi-level verbosity logging (-v/-vv/-vvv)
- 🐚 Shell completion for bash, zsh, and fish
- 🔒 Security scanning with bandit, pip-audit, and gitleaks
- ✅ Modern Python tooling (uv, mise, click)

## Installation

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install from source

```bash
# Clone the repository
git clone https://github.com/dnvriend/markdown-quiz-exporter-tool.git
cd markdown-quiz-exporter-tool

# Install globally with uv
uv tool install .
```

### Install with mise (recommended for development)

```bash
cd markdown-quiz-exporter-tool
mise trust
mise install
uv sync
uv tool install .
```

### Verify installation

```bash
markdown-quiz-exporter-tool --version
```

## Usage

The tool provides three main export commands:

### 1. Interactive HTML Quiz

Generate a self-contained interactive HTML quiz that can be opened in any web browser:

```bash
# Basic export
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "My Quiz"

# Overwrite existing file
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "AWS Quiz" --force

# With verbose output
markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "Quiz" -vv
```

**Features:**
- **Self-contained**: Single HTML file with embedded CSS and JavaScript
- **Dark/Light Mode**: Automatic theme detection with manual toggle
- **Shuffling**: Configurable question and answer randomization
- **Progress Tracking**: Visual progress bar and timer
- **Session Persistence**: Saves progress in browser storage
- **Mobile Responsive**: Works on all screen sizes
- **Markdown Support**: Renders markdown in explanations
- **Multiple Question Types**: Supports both single and multiple choice

**Opening the Quiz:**
Simply open the generated HTML file in any modern web browser. No server or internet connection required after generation.

### 2. Flashcard Hero Export

Export quiz markdown files to Flashcard Hero TSV format:

```bash
# Basic export
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv

# Overwrite existing file
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv --force

# With verbose output
markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv -vv
```

### 3. Anki Export

Export quiz markdown files to Anki CSV format with two note types:

#### AllInOne Format (Quiz) - Default

Quiz-style learning with multiple choice questions:

```bash
# Export as quiz format (default)
markdown-quiz-exporter-tool anki quiz.md quiz-cards.csv

# Or explicitly specify quiz format
markdown-quiz-exporter-tool anki quiz.md quiz-cards.csv --quiz
```

#### Basic Format (Recall)

Simple question/answer recall cards:

```bash
# Export as recall format
markdown-quiz-exporter-tool anki quiz.md recall-cards.csv --recall
```

### Quiz Markdown Format

Quiz files are markdown files with this structure:

```markdown
Question text here?

- (X) Correct answer
- ( ) Wrong answer 1
- ( ) Wrong answer 2

# reason
Explanation of why the answer is correct.

---

Next question here?
...
```

**Note Types:**
- Single choice: Use `( )` and `(X)` for radio button questions
- Multiple choice: Use `[ ]` and `[X]` for checkbox questions

For complete format specification, see `references/markdown-quiz-format.md`.

### General Options

```bash
# Show help
markdown-quiz-exporter-tool --help
markdown-quiz-exporter-tool quiz-html --help
markdown-quiz-exporter-tool flashhero --help
markdown-quiz-exporter-tool anki --help

# Run with verbose output
markdown-quiz-exporter-tool quiz-html quiz.md out.html --title "Quiz" -v    # INFO level
markdown-quiz-exporter-tool flashhero quiz.md out.tsv -vv                  # DEBUG level
markdown-quiz-exporter-tool anki quiz.md out.csv -vvv                      # TRACE level
```

## Multi-Level Verbosity Logging

The CLI supports progressive verbosity levels for debugging and troubleshooting. All logs output to stderr, keeping stdout clean for data piping.

### Logging Levels

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals | Deep debugging |

### Examples

```bash
# Quiet mode - only errors and warnings
markdown-quiz-exporter-tool

# INFO - see operations and progress
markdown-quiz-exporter-tool -v
# Output:
# [INFO] markdown-quiz-exporter-tool started
# [INFO] markdown-quiz-exporter-tool completed

# DEBUG - see detailed information
markdown-quiz-exporter-tool -vv
# Output:
# [INFO] markdown-quiz-exporter-tool started
# [DEBUG] Running with verbose level: 2
# [INFO] markdown-quiz-exporter-tool completed

# TRACE - see library internals (configure in logging_config.py)
markdown-quiz-exporter-tool -vvv
```

### Customizing Library Logging

To enable DEBUG logging for third-party libraries at TRACE level (-vvv), edit `markdown_quiz_exporter/logging_config.py`:

```python
# Configure dependent library loggers at TRACE level (-vvv)
if verbose_count >= 3:
    logging.getLogger("requests").setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)
    # Add your project-specific library loggers here
```

## Shell Completion

The CLI provides native shell completion for bash, zsh, and fish shells.

### Supported Shells

| Shell | Version Requirement | Status |
|-------|-------------------|--------|
| **Bash** | ≥ 4.4 | ✅ Supported |
| **Zsh** | Any recent version | ✅ Supported |
| **Fish** | ≥ 3.0 | ✅ Supported |
| **PowerShell** | Any version | ❌ Not Supported |

### Installation

#### Quick Setup (Temporary)

```bash
# Bash - active for current session only
eval "$(markdown-quiz-exporter-tool completion bash)"

# Zsh - active for current session only
eval "$(markdown-quiz-exporter-tool completion zsh)"

# Fish - active for current session only
markdown-quiz-exporter-tool completion fish | source
```

#### Permanent Setup (Recommended)

```bash
# Bash - add to ~/.bashrc
echo 'eval "$(markdown-quiz-exporter-tool completion bash)"' >> ~/.bashrc
source ~/.bashrc

# Zsh - add to ~/.zshrc
echo 'eval "$(markdown-quiz-exporter-tool completion zsh)"' >> ~/.zshrc
source ~/.zshrc

# Fish - save to completions directory
mkdir -p ~/.config/fish/completions
markdown-quiz-exporter-tool completion fish > ~/.config/fish/completions/markdown-quiz-exporter-tool.fish
```

#### File-based Installation (Better Performance)

For better shell startup performance, generate completion scripts to files:

```bash
# Bash
markdown-quiz-exporter-tool completion bash > ~/.markdown-quiz-exporter-tool-complete.bash
echo 'source ~/.markdown-quiz-exporter-tool-complete.bash' >> ~/.bashrc

# Zsh
markdown-quiz-exporter-tool completion zsh > ~/.markdown-quiz-exporter-tool-complete.zsh
echo 'source ~/.markdown-quiz-exporter-tool-complete.zsh' >> ~/.zshrc

# Fish (automatic loading from completions directory)
mkdir -p ~/.config/fish/completions
markdown-quiz-exporter-tool completion fish > ~/.config/fish/completions/markdown-quiz-exporter-tool.fish
```

### Usage

Once installed, completion works automatically:

```bash
# Tab completion for commands
markdown-quiz-exporter-tool <TAB>
# Shows: completion

# Tab completion for options
markdown-quiz-exporter-tool --<TAB>
# Shows: --verbose --version --help

# Tab completion for shell types
markdown-quiz-exporter-tool completion <TAB>
# Shows: bash zsh fish
```

### Getting Help

```bash
# View completion installation instructions
markdown-quiz-exporter-tool completion --help
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dnvriend/markdown-quiz-exporter-tool.git
cd markdown-quiz-exporter-tool

# Install dependencies
make install

# Show available commands
make help
```

### Available Make Commands

```bash
make install                 # Install dependencies
make format                  # Format code with ruff
make lint                    # Run linting with ruff
make typecheck               # Run type checking with mypy
make test                    # Run tests with pytest
make security-bandit         # Python security linter
make security-pip-audit      # Dependency vulnerability scanner
make security-gitleaks       # Secret/API key detection
make security                # Run all security checks
make check                   # Run all checks (lint, typecheck, test, security)
make pipeline                # Run full pipeline (format, lint, typecheck, test, security, build, install-global)
make build                   # Build package
make run ARGS="..."          # Run markdown-quiz-exporter-tool locally
make clean                   # Remove build artifacts
```

### Project Structure

```
markdown-quiz-exporter-tool/
├── markdown_quiz_exporter/         # Main package
│   ├── __init__.py
│   ├── cli.py                      # CLI entry point
│   ├── quiz_parser.py              # Quiz markdown parser
│   ├── flashcard_hero.py           # Flashcard Hero TSV exporter
│   ├── anki.py                     # Anki CSV exporter
│   ├── completion.py               # Shell completion
│   ├── logging_config.py           # Multi-level logging
│   └── utils.py                    # Utility functions
├── tests/                          # Test suite
│   ├── test_quiz_parser.py
│   ├── test_flashcard_hero.py
│   ├── test_anki.py
│   └── test_utils.py
├── references/                     # Format specifications
│   ├── markdown-quiz-format.md
│   ├── flashcard-hero-tsv-format.md
│   └── anki-csv-format.md
├── pyproject.toml                  # Project configuration
├── Makefile                        # Development commands
├── README.md                       # This file
├── LICENSE                         # MIT License
└── CLAUDE.md                       # Development documentation
```

## Testing

Run the test suite:

```bash
# Run all tests
make test

# Run tests with verbose output
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_utils.py

# Run with coverage
uv run pytest tests/ --cov=markdown_quiz_exporter
```

## Security

The project includes lightweight security tools providing 80%+ coverage with fast scan times:

### Security Tools

| Tool | Purpose | Speed | Coverage |
|------|---------|-------|----------|
| **bandit** | Python code security linting | ⚡⚡ Fast | SQL injection, hardcoded secrets, unsafe functions |
| **pip-audit** | Dependency vulnerability scanning | ⚡⚡ Fast | Known CVEs in dependencies |
| **gitleaks** | Secret and API key detection | ⚡⚡⚡ Very Fast | Secrets in code and git history |

### Running Security Scans

```bash
# Run all security checks (~5-8 seconds)
make security

# Or run individually
make security-bandit       # Python security linting
make security-pip-audit    # Dependency CVE scanning
make security-gitleaks     # Secret detection
```

### Prerequisites

gitleaks must be installed separately:

```bash
# macOS
brew install gitleaks

# Linux
# See: https://github.com/gitleaks/gitleaks#installation
```

Security checks run automatically in `make check` and `make pipeline`.

### What's Protected

- ✅ AWS credentials (AKIA*, ASIA*, etc.)
- ✅ GitHub tokens (ghp_*, gho_*, etc.)
- ✅ API keys and secrets
- ✅ Private keys
- ✅ Slack tokens
- ✅ 100+ other secret types

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the full pipeline (`make pipeline`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for public functions
- Format code with `ruff`
- Pass all linting and type checks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Dennis Vriend**

- GitHub: [@dnvriend](https://github.com/dnvriend)

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI framework
- Developed with [uv](https://github.com/astral-sh/uv) for fast Python tooling

---

**Generated with AI**

This project was generated using [Claude Code](https://www.anthropic.com/claude/code), an AI-powered development tool by [Anthropic](https://www.anthropic.com/). Claude Code assisted in creating the project structure, implementation, tests, documentation, and development tooling.

Made with ❤️ using Python 3.14
