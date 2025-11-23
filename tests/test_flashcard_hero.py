"""Tests for Flashcard Hero TSV exporter.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from pathlib import Path

import pytest

from markdown_quiz_exporter_tool.flashcard_hero import (
    FlashcardHeroExporter,
    export_to_flashcard_hero,
)
from markdown_quiz_exporter_tool.quiz_parser import Answer, Question


@pytest.fixture
def single_choice_question() -> Question:
    """Create a single choice question."""
    return Question(
        text="What is the max size of an S3 object in GB?",
        answers=[
            Answer(text="1000", is_correct=False),
            Answer(text="5000", is_correct=True),
            Answer(text="10000", is_correct=False),
        ],
        reason="The maximum size is 5TB or 5000GB.",
        question_type="single",
    )


@pytest.fixture
def multiple_choice_question() -> Question:
    """Create a multiple choice question."""
    return Question(
        text="What are characteristics of effective leadership?",
        answers=[
            Answer(text="Ability to motivate", is_correct=True),
            Answer(text="Clear communication", is_correct=True),
            Answer(text="Authoritarian approach", is_correct=False),
        ],
        reason="Leadership requires motivation and communication.",
        question_type="multiple",
    )


@pytest.fixture
def markdown_formatted_question() -> Question:
    """Create a question with markdown formatting."""
    return Question(
        text="What is **management** according to the *definition*?",
        answers=[
            Answer(text="The `optimal` cooperation of **people**", is_correct=True),
        ],
        reason="Management is defined with these **key terms**.",
        question_type="single",
    )


def test_export_single_choice(tmp_path: Path, single_choice_question: Question) -> None:
    """Test exporting a single choice question."""
    output_file = tmp_path / "output.tsv"
    count = export_to_flashcard_hero([single_choice_question], output_file)

    assert count == 1
    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    assert len(lines) == 1
    front, back = lines[0].split("\t")

    assert "S3 object" in front
    assert back == "5000"


def test_export_multiple_choice(tmp_path: Path, multiple_choice_question: Question) -> None:
    """Test exporting a multiple choice question."""
    output_file = tmp_path / "output.tsv"
    count = export_to_flashcard_hero([multiple_choice_question], output_file)

    assert count == 1

    content = output_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    front, back = lines[0].split("\t")

    assert "leadership" in front
    # Multiple answers separated by semicolon
    assert "motivate" in back
    assert "communication" in back
    assert ";" in back


def test_export_multiple_questions(
    tmp_path: Path,
    single_choice_question: Question,
    multiple_choice_question: Question,
) -> None:
    """Test exporting multiple questions."""
    output_file = tmp_path / "output.tsv"
    questions = [single_choice_question, multiple_choice_question]

    count = export_to_flashcard_hero(questions, output_file)

    assert count == 2

    content = output_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    assert len(lines) == 2


def test_strip_markdown_formatting(tmp_path: Path, markdown_formatted_question: Question) -> None:
    """Test that markdown formatting is stripped."""
    output_file = tmp_path / "output.tsv"
    export_to_flashcard_hero([markdown_formatted_question], output_file)

    content = output_file.read_text(encoding="utf-8")
    front, back = content.strip().split("\t")

    # Bold should be stripped
    assert "**" not in front
    assert "management" in front

    # Italic should be stripped
    assert "*" not in front
    assert "definition" in front

    # Code backticks should be stripped
    assert "`" not in back
    assert "optimal" in back


def test_no_tabs_in_output(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that tabs in content are replaced."""
    # Create question with tab in text
    question = Question(
        text="Question\twith\ttabs",
        answers=[Answer(text="Answer\twith\ttabs", is_correct=True)],
        reason="",
        question_type="single",
    )

    output_file = tmp_path / "output.tsv"
    export_to_flashcard_hero([question], output_file)

    content = output_file.read_text(encoding="utf-8")

    # Should have exactly one tab (the separator)
    assert content.count("\t") == 1

    front, back = content.strip().split("\t")
    assert "\t" not in front.replace("\t", "")  # No additional tabs
    assert "\t" not in back.replace("\t", "")


def test_utf8_encoding(tmp_path: Path) -> None:
    """Test UTF-8 encoding for special characters."""
    question = Question(
        text="Wat is de definitie van 'management'?",
        answers=[
            Answer(
                text="Optimaal samenwerken van mensen en middelen",
                is_correct=True,
            )
        ],
        reason="",
        question_type="single",
    )

    output_file = tmp_path / "output.tsv"
    export_to_flashcard_hero([question], output_file)

    # Read with UTF-8 encoding
    content = output_file.read_text(encoding="utf-8")
    assert "definitie" in content
    assert "samenwerken" in content


def test_exporter_class_directly() -> None:
    """Test using the exporter class directly."""
    question = Question(
        text="Test question?",
        answers=[Answer(text="Test answer", is_correct=True)],
        reason="Test reason",
        question_type="single",
    )

    exporter = FlashcardHeroExporter([question])
    assert len(exporter.questions) == 1

    # Test formatting methods
    formatted_q = exporter._format_question(question.text)
    assert formatted_q == "Test question?"

    formatted_a = exporter._format_answer(question)
    assert formatted_a == "Test answer"


def test_strip_markdown_links(tmp_path: Path) -> None:
    """Test that markdown links are stripped correctly."""
    question = Question(
        text="See [documentation](https://example.com) for details",
        answers=[Answer(text="Answer with [link](https://example.com)", is_correct=True)],
        reason="",
        question_type="single",
    )

    output_file = tmp_path / "output.tsv"
    export_to_flashcard_hero([question], output_file)

    content = output_file.read_text(encoding="utf-8")
    front, back = content.strip().split("\t")

    # Links should be converted to text only
    assert "[" not in front
    assert "]" not in front
    assert "documentation" in front

    assert "[" not in back
    assert "link" in back
