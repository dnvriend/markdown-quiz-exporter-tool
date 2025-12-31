# markdown-quiz-exporter-tool - Project Specification

## Goal

A CLI tool that exports quiz markdown files to multiple formats: interactive HTML quizzes, Anki flashcards, Flashcard Hero TSV, and Microsoft Word DOCX.

## What is markdown-quiz-exporter-tool?

`markdown-quiz-exporter-tool` is a command-line utility built with modern Python tooling and best practices. It transforms markdown-formatted quiz files into various learning formats for different study tools.

## Technical Requirements

### Runtime

- Python 3.14+
- Installable globally with mise
- Cross-platform (macOS, Linux, Windows)

### Dependencies

- `click` - CLI framework
- `python-docx` - Word DOCX generation

### Development Dependencies

- `ruff` - Linting and formatting
- `mypy` - Type checking
- `pytest` - Testing framework
- `bandit` - Security linting
- `pip-audit` - Dependency vulnerability scanning
- `gitleaks` - Secret detection (requires separate installation)

## CLI Commands

The CLI is structured as a Click group with multiple subcommands for different export formats.

### Main Command

```bash
markdown-quiz-exporter-tool [OPTIONS] COMMAND [ARGS]...
```

### Global Options

- `-v, --verbose` - Enable verbose output (count flag: -v, -vv, -vvv)
  - `-v` (count=1): INFO level logging
  - `-vv` (count=2): DEBUG level logging
  - `-vvv` (count=3+): TRACE level (includes library internals)
- `--help` - Show help message
- `--version` - Show version

### Subcommands

1. **quiz-html** - Generate interactive HTML quiz
   ```bash
   markdown-quiz-exporter-tool quiz-html INPUT_FILE OUTPUT_FILE --title TITLE [OPTIONS]
   ```
   - Required: `--title` - Quiz title for intro page
   - Optional: `-f, --force` - Overwrite existing file
   - Optional: `-v, --verbose` - Verbosity level

2. **flashhero** - Export to Flashcard Hero TSV
   ```bash
   markdown-quiz-exporter-tool flashhero INPUT_FILE OUTPUT_FILE [OPTIONS]
   ```
   - Optional: `-f, --force` - Overwrite existing file
   - Optional: `-v, --verbose` - Verbosity level

3. **anki** - Export to Anki CSV format
   ```bash
   markdown-quiz-exporter-tool anki INPUT_FILE OUTPUT_FILE [OPTIONS]
   ```
   - Optional: `--quiz` - AllInOne quiz format (default)
   - Optional: `--recall` - Basic recall format
   - Optional: `-f, --force` - Overwrite existing file
   - Optional: `-v, --verbose` - Verbosity level

4. **quiz-docx** - Export to Microsoft Word DOCX format
   ```bash
   markdown-quiz-exporter-tool quiz-docx INPUT_FILE OUTPUT_FILE [OPTIONS]
   ```
   - Optional: `-f, --force` - Overwrite existing file
   - Optional: `-v, --verbose` - Verbosity level

5. **completion** - Generate shell completion scripts
   ```bash
   markdown-quiz-exporter-tool completion {bash|zsh|fish}
   ```

## Project Structure

```
markdown-quiz-exporter-tool/
├── markdown_quiz_exporter_tool/     # Main package
│   ├── __init__.py
│   ├── cli.py                       # Click CLI entry point (group with subcommands)
│   ├── completion.py                # Shell completion command
│   ├── logging_config.py            # Multi-level verbosity logging
│   ├── quiz_parser.py               # Parse quiz markdown files
│   ├── quiz_html.py                 # HTML quiz generator
│   ├── flashcard_hero.py            # Flashcard Hero TSV exporter
│   ├── anki.py                      # Anki CSV exporter
│   ├── docx.py                      # Word DOCX exporter
│   └── utils.py                     # Utility functions
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_quiz_parser.py
│   ├── test_quiz_html.py
│   ├── test_flashcard_hero.py
│   ├── test_anki.py
│   ├── test_docx.py
│   └── test_utils.py
├── references/                      # Format specifications
│   ├── markdown-quiz-format.md
│   ├── flashcard-hero-tsv-format.md
│   └── anki-csv-format.md
├── plugins/                         # Claude Code integration
│   └── markdown-quiz-exporter-tool/
│       ├── commands/                # Slash commands
│       ├── skills/                  # Agent skills
│       └── marketplace.json
├── pyproject.toml                   # Project configuration
├── README.md                        # User documentation
├── CLAUDE.md                        # This file - development spec
├── Makefile                         # Development commands
├── LICENSE                          # MIT License
├── .mise.toml                       # mise configuration
├── .gitleaks.toml                   # Gitleaks configuration
└── .gitignore
```

## Code Style

- Type hints for all functions
- Docstrings for all public functions
- Follow PEP 8 via ruff
- 100 character line length
- Strict mypy checking

## Development Workflow

```bash
# Install dependencies
make install

# Run linting
make lint

# Format code
make format

# Type check
make typecheck

# Run tests
make test

# Security scanning
make security-bandit       # Python security linting
make security-pip-audit    # Dependency CVE scanning
make security-gitleaks     # Secret detection
make security              # Run all security checks

# Run all checks (includes security)
make check

# Full pipeline (includes security)
make pipeline
```

## Security

The template includes three lightweight security tools:

1. **bandit** - Python code security linting
   - Detects: SQL injection, hardcoded secrets, unsafe functions
   - Speed: ~2-3 seconds

2. **pip-audit** - Dependency vulnerability scanning
   - Detects: Known CVEs in dependencies
   - Speed: ~2-3 seconds

3. **gitleaks** - Secret and API key detection
   - Detects: AWS keys, GitHub tokens, API keys, private keys
   - Speed: ~1 second
   - Requires: `brew install gitleaks` (macOS)

All security checks run automatically in `make check` and `make pipeline`.

## Multi-Level Verbosity Logging

The template includes a centralized logging system with progressive verbosity levels.

### Implementation Pattern

1. **logging_config.py** - Centralized logging configuration
   - `setup_logging(verbose_count)` - Configure logging based on -v count
   - `get_logger(name)` - Get logger instance for module
   - Maps verbosity to Python logging levels (WARNING/INFO/DEBUG)

2. **CLI Integration** - Add to every CLI command
   ```python
   from markdown_quiz_exporter_tool.logging_config import get_logger, setup_logging

   logger = get_logger(__name__)

   @click.command()
   @click.option("-v", "--verbose", count=True, help="...")
   def command(verbose: int):
       setup_logging(verbose)  # First thing in command
       logger.info("Operation started")
       logger.debug("Detailed info")
   ```

3. **Logging Levels**
   - **0 (no -v)**: WARNING only - production/quiet mode
   - **1 (-v)**: INFO - high-level operations
   - **2 (-vv)**: DEBUG - detailed debugging
   - **3+ (-vvv)**: TRACE - enable library internals

4. **Best Practices**
   - Always log to stderr (keeps stdout clean for piping)
   - Use structured messages with placeholders: `logger.info("Found %d items", count)`
   - Call `setup_logging()` first in every command
   - Use `get_logger(__name__)` at module level
   - For TRACE level, enable third-party library loggers in `logging_config.py`

5. **Customizing Library Logging**
   Edit `logging_config.py` to add project-specific libraries:
   ```python
   if verbose_count >= 3:
       logging.getLogger("requests").setLevel(logging.DEBUG)
       logging.getLogger("urllib3").setLevel(logging.DEBUG)
   ```

## Shell Completion

The template includes shell completion for bash, zsh, and fish following the Click Shell Completion Pattern.

### Implementation

1. **completion.py** - Separate module for completion command
   - Uses Click's `BashComplete`, `ZshComplete`, `FishComplete` classes
   - Generates shell-specific completion scripts
   - Includes installation instructions in help text

2. **CLI Integration** - Added as subcommand
   ```python
   from markdown_quiz_exporter_tool.completion import completion_command

   @click.group(invoke_without_command=True)
   def main(ctx: click.Context):
       # Default behavior when no subcommand
       if ctx.invoked_subcommand is None:
           # Show help by default
           click.echo(ctx.get_help())

   # Add completion subcommand
   main.add_command(completion_command)
   ```

3. **Usage Pattern** - User-friendly command
   ```bash
   # Generate completion script
   markdown-quiz-exporter-tool completion bash
   markdown-quiz-exporter-tool completion zsh
   markdown-quiz-exporter-tool completion fish

   # Install (eval or save to file)
   eval "$(markdown-quiz-exporter-tool completion bash)"
   ```

4. **Supported Shells**
   - **Bash** (≥ 4.4) - Uses bash-completion
   - **Zsh** (any recent) - Uses zsh completion system
   - **Fish** (≥ 3.0) - Uses fish completion system
   - **PowerShell** - Not supported by Click

5. **Installation Methods**
   - **Temporary**: `eval "$(markdown-quiz-exporter-tool completion bash)"`
   - **Permanent**: Add eval to ~/.bashrc or ~/.zshrc
   - **File-based** (recommended): Save to dedicated completion file

### Adding More Commands

The CLI uses `@click.group()` for extensibility. To add new commands:

1. Create new command module in `markdown_quiz_exporter_tool/`
2. Import and add to CLI group:
   ```python
   from markdown_quiz_exporter_tool.new_command import new_command
   main.add_command(new_command)
   ```

3. Completion will automatically work for new commands and their options

## Installation Methods

### Global installation with uv tool

```bash
cd /path/to/markdown-quiz-exporter-tool
uv sync
uv tool install .
```

After installation, `markdown-quiz-exporter-tool` command is available globally.

### Global installation with mise (alternative)

```bash
cd /path/to/markdown-quiz-exporter-tool
mise use -g python@3.14
uv sync
uv tool install .
```

### Local development

```bash
uv sync
uv run markdown-quiz-exporter-tool [args]
```

## Quiz HTML Features

The `quiz-html` command generates a self-contained interactive HTML quiz with the following features:

### User Interface
- **Intro Page**: Configurable quiz title, question count, and shuffle options
- **Question Display**: Clear question text with configurable answer shuffling
- **Progress Tracking**: Visual progress bar and elapsed timer
- **Review Mode**: See all answers with explanations after completion
- **Results Summary**: Score, percentage, and time taken

### Technical Features
- **Self-contained**: Single HTML file with embedded Tailwind CSS and JavaScript
- **Dark/Light Mode**: Automatic system preference detection with manual toggle button
- **Session Storage**: Preserves quiz state across page refreshes
- **Markdown Rendering**: Uses marked.js for rich text explanations
- **Mobile Responsive**: Works on all screen sizes
- **No Dependencies**: Can be opened directly in any modern browser offline

### Question Types
- **Single Choice**: Radio buttons for questions with one correct answer
- **Multiple Choice**: Checkboxes for questions with multiple correct answers

### State Management
The quiz uses a single-page application architecture with JavaScript state management:
- Config page → Question pages → Review page
- Answers are validated immediately on check
- Progress is saved in browser sessionStorage
