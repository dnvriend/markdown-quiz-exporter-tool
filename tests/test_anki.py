"""Tests for Anki CSV exporter.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import csv
from pathlib import Path

import pytest

from markdown_quiz_exporter_tool.anki import (
    AnkiAllInOneExporter,
    export_to_anki_allinone,
    export_to_anki_basic,
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
def five_option_question() -> Question:
    """Create a question with exactly 5 options."""
    return Question(
        text="What is a security group?",
        answers=[
            Answer(text="Option 1", is_correct=False),
            Answer(text="Option 2 (correct)", is_correct=True),
            Answer(text="Option 3", is_correct=False),
            Answer(text="Option 4", is_correct=False),
            Answer(text="Option 5", is_correct=False),
        ],
        reason="Option 2 is correct.",
        question_type="single",
    )


def test_allinone_export_single_choice(tmp_path: Path, single_choice_question: Question) -> None:
    """Test AllInOne format export for single choice question."""
    output_file = tmp_path / "output.csv"
    count = export_to_anki_allinone([single_choice_question], output_file)

    assert count == 1
    assert output_file.exists()

    # Read and parse CSV
    with open(output_file, encoding="utf-8") as f:
        lines = f.readlines()

    # Check headers
    assert lines[0].strip() == "#separator:Semicolon"
    assert lines[1].strip() == "#html:false"
    assert lines[2].strip() == "#notetype:AllInOne (kprim, mc, sc)"
    assert lines[3].strip() == "#tags:quiz generated"

    # Parse data row
    reader = csv.reader([lines[4]], delimiter=";")
    row = next(reader)

    # Check fields
    assert "S3 object" in row[0]  # Question
    assert row[1] == ""  # Title (empty)
    assert row[2] == "2"  # QType (single choice)
    assert row[3] == "1000"  # Q_1
    assert row[4] == "5000"  # Q_2
    assert row[5] == "10000"  # Q_3
    assert row[6] == ""  # Q_4 (empty)
    assert row[7] == ""  # Q_5 (empty)
    assert row[8] == "0 1 0 0 0"  # Answers (second option correct)
    assert row[9] == ""  # Sources (empty)
    assert "5TB" in row[10]  # Extra1 (explanation)
    assert row[11] == "quiz"  # Tags


def test_allinone_export_multiple_choice(
    tmp_path: Path, multiple_choice_question: Question
) -> None:
    """Test AllInOne format export for multiple choice question."""
    output_file = tmp_path / "output.csv"
    count = export_to_anki_allinone([multiple_choice_question], output_file)

    assert count == 1

    # Read and parse CSV
    with open(output_file, encoding="utf-8") as f:
        lines = f.readlines()

    reader = csv.reader([lines[4]], delimiter=";")
    row = next(reader)

    # Check QType is multiple choice
    assert row[2] == "1"

    # Check answers field (first two correct)
    assert row[8] == "1 1 0 0 0"


def test_allinone_five_options(tmp_path: Path, five_option_question: Question) -> None:
    """Test AllInOne format with exactly 5 options."""
    output_file = tmp_path / "output.csv"
    export_to_anki_allinone([five_option_question], output_file)

    with open(output_file, encoding="utf-8") as f:
        lines = f.readlines()

    reader = csv.reader([lines[4]], delimiter=";")
    row = next(reader)

    # All Q_1 through Q_5 should be filled
    assert row[3] == "Option 1"
    assert row[4] == "Option 2 (correct)"
    assert row[5] == "Option 3"
    assert row[6] == "Option 4"
    assert row[7] == "Option 5"

    # Second option correct
    assert row[8] == "0 1 0 0 0"


def test_basic_export_single_answer(tmp_path: Path, single_choice_question: Question) -> None:
    """Test Basic format export for single answer question."""
    output_file = tmp_path / "output.csv"
    count = export_to_anki_basic([single_choice_question], output_file)

    assert count == 1
    assert output_file.exists()

    # Read and parse CSV
    with open(output_file, encoding="utf-8") as f:
        lines = f.readlines()

    # Check headers
    assert lines[0].strip() == "#separator:Semicolon"
    assert lines[1].strip() == "#html:false"
    assert lines[2].strip() == "#notetype:Basic"
    assert lines[3].strip() == "#tags:quiz recall"

    # Parse data row
    reader = csv.reader([lines[4]], delimiter=";")
    row = next(reader)

    # Check fields
    assert "S3 object" in row[0]  # Front
    assert "Answer: 5000" in row[1]  # Back (with answer)
    assert "Explanation:" in row[1]  # Back (with explanation)
    assert "<br>" in row[1]  # Line breaks as <br> tags
    assert row[2] == "recall"  # Tags


def test_basic_export_multiple_answers(tmp_path: Path, multiple_choice_question: Question) -> None:
    """Test Basic format export for multiple answer question."""
    output_file = tmp_path / "output.csv"
    count = export_to_anki_basic([multiple_choice_question], output_file)

    assert count == 1

    # Read and parse CSV
    with open(output_file, encoding="utf-8") as f:
        lines = f.readlines()

    reader = csv.reader([lines[4]], delimiter=";")
    row = next(reader)

    # Check back side has multiple answers
    assert "Answers:" in row[1]
    assert "motivate" in row[1]
    assert "communication" in row[1]
    assert "," in row[1]  # Comma-separated


def test_basic_export_no_reason(tmp_path: Path) -> None:
    """Test Basic format when question has no reason."""
    question = Question(
        text="Test question?",
        answers=[Answer(text="Test answer", is_correct=True)],
        reason="",
        question_type="single",
    )

    output_file = tmp_path / "output.csv"
    export_to_anki_basic([question], output_file)

    with open(output_file, encoding="utf-8") as f:
        lines = f.readlines()

    reader = csv.reader([lines[4]], delimiter=";")
    row = next(reader)

    # Back should only have answer, no explanation
    assert "Answer: Test answer" in row[1]
    assert "Explanation:" not in row[1]


def test_allinone_multiple_questions(
    tmp_path: Path,
    single_choice_question: Question,
    multiple_choice_question: Question,
) -> None:
    """Test AllInOne format with multiple questions."""
    output_file = tmp_path / "output.csv"
    questions = [single_choice_question, multiple_choice_question]

    count = export_to_anki_allinone(questions, output_file)

    assert count == 2

    with open(output_file, encoding="utf-8") as f:
        lines = f.readlines()

    # 4 header lines + 2 question lines
    assert len(lines) == 6


def test_basic_multiple_questions(
    tmp_path: Path,
    single_choice_question: Question,
    multiple_choice_question: Question,
) -> None:
    """Test Basic format with multiple questions."""
    output_file = tmp_path / "output.csv"
    questions = [single_choice_question, multiple_choice_question]

    count = export_to_anki_basic(questions, output_file)

    assert count == 2

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    # Check that we have both questions
    assert "S3 object" in content
    assert "leadership" in content


def test_text_normalization() -> None:
    """Test that multi-line text is normalized to single line."""
    question = Question(
        text="Line 1\nLine 2\n  Line 3  ",
        answers=[
            Answer(text="Answer\nwith\nnewlines", is_correct=True),
        ],
        reason="Reason\nwith\nnewlines",
        question_type="single",
    )

    exporter = AnkiAllInOneExporter([question])
    normalized = exporter._normalize_text(question.text)

    # Should be single line with spaces
    assert "\n" not in normalized
    assert normalized == "Line 1 Line 2 Line 3"


def test_qtype_determination() -> None:
    """Test QType determination logic."""
    # Single choice with radio buttons
    single_radio = Question(
        text="Q?",
        answers=[Answer(text="A", is_correct=True)],
        reason="",
        question_type="single",
    )

    # Multiple choice with checkboxes but only one correct
    single_checkbox = Question(
        text="Q?",
        answers=[
            Answer(text="A", is_correct=True),
            Answer(text="B", is_correct=False),
        ],
        reason="",
        question_type="multiple",
    )

    # Multiple choice with multiple correct
    multiple = Question(
        text="Q?",
        answers=[
            Answer(text="A", is_correct=True),
            Answer(text="B", is_correct=True),
        ],
        reason="",
        question_type="multiple",
    )

    exporter = AnkiAllInOneExporter([])

    assert exporter._get_qtype(single_radio) == "2"
    assert exporter._get_qtype(single_checkbox) == "2"
    assert exporter._get_qtype(multiple) == "1"
