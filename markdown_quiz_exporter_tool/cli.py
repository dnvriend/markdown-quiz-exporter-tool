"""CLI entry point for markdown-quiz-exporter-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from pathlib import Path

import click

from markdown_quiz_exporter_tool.anki import export_to_anki_allinone, export_to_anki_basic
from markdown_quiz_exporter_tool.completion import completion_command
from markdown_quiz_exporter_tool.flashcard_hero import export_to_flashcard_hero
from markdown_quiz_exporter_tool.logging_config import get_logger, setup_logging
from markdown_quiz_exporter_tool.quiz_html import export_to_quiz_html
from markdown_quiz_exporter_tool.quiz_parser import QuizParseError, parse_quiz_file

logger = get_logger(__name__)


@click.group(invoke_without_command=True)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.version_option(version="0.1.0")
@click.pass_context
def main(ctx: click.Context, verbose: int) -> None:
    """A CLI tool that exports the quiz-markdown-format to tools like Anki, Flashcard Hero"""
    # Setup logging based on verbosity count
    setup_logging(verbose)

    # If no subcommand is provided, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@click.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Overwrite output file if it exists",
)
def flashhero(input_file: Path, output_file: Path, verbose: int, force: bool) -> None:
    """Export quiz markdown to Flashcard Hero TSV format.

    Reads a quiz markdown file and exports it to TSV format that can be
    imported into Flashcard Hero flashcard application.

    \b
    Arguments:
        INPUT_FILE   Path to the quiz markdown file (*.md)
        OUTPUT_FILE  Path where TSV file will be written (*.tsv)

    \b
    Examples:

        \b
        # Basic export
        markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv

        \b
        # Overwrite existing file
        markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv --force

        \b
        # With verbose output for debugging
        markdown-quiz-exporter-tool flashhero quiz.md flashcards.tsv -vv

    \b
    Output Format:
        TSV file with two columns separated by tabs:
        Question<TAB>Answer

        For questions with multiple correct answers:
        Question<TAB>Answer1; Answer2; Answer3
    """
    setup_logging(verbose)

    logger.info("Starting Flashcard Hero export")
    logger.debug("Input file: %s", input_file)
    logger.debug("Output file: %s", output_file)

    # Check if output file exists
    if output_file.exists() and not force:
        click.echo(
            f"Error: Output file '{output_file}' already exists. Use --force to overwrite.",
            err=True,
        )
        raise click.Abort()

    # Validate input file extension
    if input_file.suffix.lower() != ".md":
        click.echo(
            f"Warning: Input file '{input_file}' does not have .md extension. Continuing anyway...",
            err=True,
        )

    # Parse the quiz file
    try:
        logger.info("Parsing quiz file: %s", input_file)
        questions = parse_quiz_file(input_file)
        logger.info("Parsed %d questions", len(questions))
    except FileNotFoundError:
        click.echo(f"Error: Quiz file not found: {input_file}", err=True)
        raise click.Abort()
    except QuizParseError as e:
        click.echo(f"Error parsing quiz file: {e}", err=True)
        logger.debug("Parse error details", exc_info=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error parsing quiz file: {e}", err=True)
        logger.debug("Unexpected error details", exc_info=True)
        raise click.Abort()

    # Export to Flashcard Hero format
    try:
        logger.info("Exporting to Flashcard Hero format")
        count = export_to_flashcard_hero(questions, output_file)
        logger.info("Exported %d flashcards", count)

        click.echo(f"✓ Successfully exported {count} flashcards to {output_file}")
    except OSError as e:
        click.echo(f"Error writing to output file: {e}", err=True)
        logger.debug("IO error details", exc_info=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error during export: {e}", err=True)
        logger.debug("Unexpected error details", exc_info=True)
        raise click.Abort()


@click.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Overwrite output file if it exists",
)
@click.option(
    "--quiz",
    "format_type",
    flag_value="quiz",
    default=True,
    help="Export as AllInOne quiz format (default)",
)
@click.option(
    "--recall",
    "format_type",
    flag_value="recall",
    help="Export as Basic recall format",
)
def anki(input_file: Path, output_file: Path, verbose: int, force: bool, format_type: str) -> None:
    """Export quiz markdown to Anki CSV format.

    Reads a quiz markdown file and exports it to CSV format that can be
    imported into Anki flashcard application. Supports two note types:

    \b
    - AllInOne (--quiz): Quiz format with multiple choice questions
    - Basic (--recall): Simple question/answer recall format

    \b
    Arguments:
        INPUT_FILE   Path to the quiz markdown file (*.md)
        OUTPUT_FILE  Path where CSV file will be written (*.csv)

    \b
    Examples:

        \b
        # Export as quiz format (default)
        markdown-quiz-exporter-tool anki quiz.md quiz-cards.csv

        \b
        # Export as recall format
        markdown-quiz-exporter-tool anki quiz.md recall-cards.csv --recall

        \b
        # Overwrite existing file
        markdown-quiz-exporter-tool anki quiz.md cards.csv --force

        \b
        # With verbose output for debugging
        markdown-quiz-exporter-tool anki quiz.md cards.csv -vv

    \b
    Output Format:
        AllInOne (--quiz):
          Question;Title;QType;Q_1;Q_2;Q_3;Q_4;Q_5;Answers;Sources;Extra1;Tags

        Basic (--recall):
          Front;Back;Tags
    """
    setup_logging(verbose)

    logger.info("Starting Anki export")
    logger.debug("Input file: %s", input_file)
    logger.debug("Output file: %s", output_file)
    logger.debug("Format type: %s", format_type)

    # Check if output file exists
    if output_file.exists() and not force:
        click.echo(
            f"Error: Output file '{output_file}' already exists. Use --force to overwrite.",
            err=True,
        )
        raise click.Abort()

    # Validate input file extension
    if input_file.suffix.lower() != ".md":
        click.echo(
            f"Warning: Input file '{input_file}' does not have .md extension. Continuing anyway...",
            err=True,
        )

    # Parse the quiz file
    try:
        logger.info("Parsing quiz file: %s", input_file)
        questions = parse_quiz_file(input_file)
        logger.info("Parsed %d questions", len(questions))
    except FileNotFoundError:
        click.echo(f"Error: Quiz file not found: {input_file}", err=True)
        raise click.Abort()
    except QuizParseError as e:
        click.echo(f"Error parsing quiz file: {e}", err=True)
        logger.debug("Parse error details", exc_info=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error parsing quiz file: {e}", err=True)
        logger.debug("Unexpected error details", exc_info=True)
        raise click.Abort()

    # Check for questions with more than 5 options (AllInOne limitation)
    if format_type == "quiz":
        over_limit = [q for q in questions if len(q.answers) > 5]
        if over_limit:
            click.echo(
                f"Warning: {len(over_limit)} question(s) have more than 5 answer options. "
                "Only the first 5 will be included in AllInOne format.",
                err=True,
            )
            logger.warning("%d questions exceed 5-option limit for AllInOne", len(over_limit))

    # Export to Anki format
    try:
        logger.info("Exporting to Anki %s format", format_type)

        if format_type == "recall":
            count = export_to_anki_basic(questions, output_file)
            format_name = "Basic (recall)"
        else:
            count = export_to_anki_allinone(questions, output_file)
            format_name = "AllInOne (quiz)"

        logger.info("Exported %d flashcards", count)

        click.echo(
            f"✓ Successfully exported {count} flashcards to {output_file} ({format_name} format)"
        )
    except OSError as e:
        click.echo(f"Error writing to output file: {e}", err=True)
        logger.debug("IO error details", exc_info=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error during export: {e}", err=True)
        logger.debug("Unexpected error details", exc_info=True)
        raise click.Abort()


@click.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "--title",
    required=True,
    help="Quiz title displayed on intro page",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Overwrite output file if exists",
)
def quiz_html(
    input_file: Path,
    output_file: Path,
    title: str,
    verbose: int,
    force: bool,
) -> None:
    """Generate interactive HTML quiz from markdown.

    Creates a single-page application with embedded quiz data,
    CSS (Tailwind), and JavaScript. The generated HTML file is
    self-contained and requires no external dependencies.

    \b
    Features:
    - Dark/light mode with system preference detection
    - Configurable question/answer shuffling
    - Progress tracking and timer
    - Statistics and review mode
    - Mobile-responsive design
    - Session storage for progress persistence

    \b
    Arguments:
        INPUT_FILE   Path to quiz markdown file (*.md)
        OUTPUT_FILE  Path where HTML file will be written (*.html)

    \b
    Examples:

        \b
        # Generate quiz HTML
        markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "My Quiz"

        \b
        # Overwrite existing file
        markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "Quiz" --force

        \b
        # With verbose output
        markdown-quiz-exporter-tool quiz-html quiz.md quiz.html --title "Quiz" -vv
    """
    setup_logging(verbose)

    logger.info("Starting HTML quiz generation")
    logger.debug("Input: %s, Output: %s, Title: %s", input_file, output_file, title)

    # Check output file
    if output_file.exists() and not force:
        click.echo(
            f"Error: Output file '{output_file}' already exists. Use --force to overwrite.",
            err=True,
        )
        raise click.Abort()

    # Validate input file extension
    if input_file.suffix.lower() != ".md":
        click.echo(
            f"Warning: Input file '{input_file}' does not have .md extension. Continuing anyway...",
            err=True,
        )

    # Parse quiz file
    try:
        logger.info("Parsing quiz file: %s", input_file)
        questions = parse_quiz_file(input_file)
        logger.info("Parsed %d questions", len(questions))
    except FileNotFoundError:
        click.echo(f"Error: Quiz file not found: {input_file}", err=True)
        raise click.Abort()
    except QuizParseError as e:
        click.echo(f"Error parsing quiz file: {e}", err=True)
        logger.debug("Parse error details", exc_info=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error parsing quiz file: {e}", err=True)
        logger.debug("Unexpected error details", exc_info=True)
        raise click.Abort()

    # Generate HTML quiz
    try:
        logger.info("Generating HTML quiz")
        file_size = export_to_quiz_html(questions, output_file, title)
        logger.info("Generated HTML quiz: %s (%d bytes)", output_file, file_size)

        file_size_kb = file_size / 1024
        click.echo(f"✓ Successfully generated {output_file} ({file_size_kb:.1f} KB)")
        click.echo(f"  Questions: {len(questions)}")
        click.echo(f"  Open {output_file} in a web browser to start the quiz")
    except OSError as e:
        click.echo(f"Error writing to output file: {e}", err=True)
        logger.debug("IO error details", exc_info=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error during HTML generation: {e}", err=True)
        logger.debug("Unexpected error details", exc_info=True)
        raise click.Abort()


# Add subcommands
main.add_command(completion_command)
main.add_command(flashhero)
main.add_command(anki)
main.add_command(quiz_html)


if __name__ == "__main__":
    main()
