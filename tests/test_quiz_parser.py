"""Tests for quiz markdown parser.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from pathlib import Path

import pytest

from markdown_quiz_exporter_tool.quiz_parser import (
    ParseError,
    QuizParseError,
    parse_quiz_file,
)


@pytest.fixture
def sample_quiz_content() -> str:
    """Sample quiz markdown content."""
    return """What is the max size of an S3 object in GB?

- ( ) 1000
- (X) 5000
- ( ) 10000

# reason
The maximum size for a single S3 object is 5TB or 5000GB.

---

What are characteristics of effective leadership? (Multiple answers)

- [X] Ability to motivate a team
- [X] Clear communication
- [ ] Authoritarian decision making
- [ ] Short-term focus

# reason
Leadership requires motivation and clear communication.
"""


@pytest.fixture
def temp_quiz_file(tmp_path: Path, sample_quiz_content: str) -> Path:
    """Create a temporary quiz file."""
    quiz_file = tmp_path / "test_quiz.md"
    quiz_file.write_text(sample_quiz_content, encoding="utf-8")
    return quiz_file


def test_parse_single_choice_question(temp_quiz_file: Path) -> None:
    """Test parsing a single choice question."""
    questions = parse_quiz_file(temp_quiz_file)

    assert len(questions) == 2

    # Check first question (single choice)
    q1 = questions[0]
    assert q1.question_type == "single"
    assert "S3 object" in q1.text
    assert len(q1.answers) == 3

    # Check correct answer
    correct = [a for a in q1.answers if a.is_correct]
    assert len(correct) == 1
    assert correct[0].text == "5000"


def test_parse_multiple_choice_question(temp_quiz_file: Path) -> None:
    """Test parsing a multiple choice question."""
    questions = parse_quiz_file(temp_quiz_file)

    # Check second question (multiple choice)
    q2 = questions[1]
    assert q2.question_type == "multiple"
    assert "leadership" in q2.text
    assert len(q2.answers) == 4

    # Check correct answers
    correct = [a for a in q2.answers if a.is_correct]
    assert len(correct) == 2
    assert any("motivate" in a.text for a in correct)
    assert any("communication" in a.text for a in correct)


def test_parse_reason_section(temp_quiz_file: Path) -> None:
    """Test parsing the reason section."""
    questions = parse_quiz_file(temp_quiz_file)

    q1 = questions[0]
    assert "5TB" in q1.reason
    assert "5000GB" in q1.reason


def test_missing_correct_answer(tmp_path: Path) -> None:
    """Test error when no correct answer is marked."""
    content = """Question?

- ( ) Answer 1
- ( ) Answer 2

# reason
Some reason.
"""
    quiz_file = tmp_path / "invalid.md"
    quiz_file.write_text(content, encoding="utf-8")

    with pytest.raises(QuizParseError, match="No correct answer"):
        parse_quiz_file(quiz_file)


def test_empty_file(tmp_path: Path) -> None:
    """Test error when file is empty."""
    quiz_file = tmp_path / "empty.md"
    quiz_file.write_text("", encoding="utf-8")

    with pytest.raises(QuizParseError, match="No questions found"):
        parse_quiz_file(quiz_file)


def test_file_not_found() -> None:
    """Test error when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        parse_quiz_file(Path("/nonexistent/file.md"))


def test_mixed_answer_types(tmp_path: Path) -> None:
    """Test error when mixing single and multiple choice formats."""
    content = """Question?

- (X) Answer 1
- [ ] Answer 2

# reason
Mixed types.
"""
    quiz_file = tmp_path / "mixed.md"
    quiz_file.write_text(content, encoding="utf-8")

    with pytest.raises(QuizParseError, match="Mixed answer types"):
        parse_quiz_file(quiz_file)


def test_lowercase_x_marker(tmp_path: Path) -> None:
    """Test that lowercase 'x' is recognized as correct."""
    content = """Question?

- (x) Correct answer
- ( ) Wrong answer

# reason
Testing lowercase.
"""
    quiz_file = tmp_path / "lowercase.md"
    quiz_file.write_text(content, encoding="utf-8")

    questions = parse_quiz_file(quiz_file)
    correct = [a for a in questions[0].answers if a.is_correct]
    assert len(correct) == 1
    assert correct[0].text == "Correct answer"


def test_detailed_error_mixed_types(tmp_path: Path) -> None:
    """Test detailed error reporting for mixed answer types."""
    content = """What is the answer?

- ( ) Wrong 1
- (X) Correct
- [ ] Wrong 2

# reason
This has mixed types.
"""
    quiz_file = tmp_path / "mixed_detailed.md"
    quiz_file.write_text(content, encoding="utf-8")

    with pytest.raises(QuizParseError) as exc_info:
        parse_quiz_file(quiz_file)

    # Check that detailed error info is attached
    assert exc_info.value.parse_error is not None
    err = exc_info.value.parse_error
    assert isinstance(err, ParseError)
    assert err.line_number == 5  # The line with [ ]
    assert err.block_number == 1
    assert "Mixed answer types" in err.error_message
    assert len(err.context_before) > 0


def test_detailed_error_no_correct_answer(tmp_path: Path) -> None:
    """Test detailed error reporting when no correct answer is marked."""
    content = """Which are colors?

- [ ] Red
- [ ] Blue
- [ ] Green

# reason
All wrong!
"""
    quiz_file = tmp_path / "no_correct.md"
    quiz_file.write_text(content, encoding="utf-8")

    with pytest.raises(QuizParseError) as exc_info:
        parse_quiz_file(quiz_file)

    # Check detailed error info
    assert exc_info.value.parse_error is not None
    err = exc_info.value.parse_error
    assert err.line_number == 3  # First answer line
    assert "No correct answer marked" in err.error_message
    assert "(X) or [X]" in err.error_message


def test_detailed_error_no_answers(tmp_path: Path) -> None:
    """Test detailed error reporting when question has no answers."""
    content = """This is a question with no answers?

# reason
No answer options provided.
"""
    quiz_file = tmp_path / "no_answers.md"
    quiz_file.write_text(content, encoding="utf-8")

    with pytest.raises(QuizParseError) as exc_info:
        parse_quiz_file(quiz_file)

    # Check detailed error info
    assert exc_info.value.parse_error is not None
    err = exc_info.value.parse_error
    assert "No answers found" in err.error_message
    assert "- (X)" in err.error_message or "- [X]" in err.error_message


def test_error_context_lines(tmp_path: Path) -> None:
    """Test that error context includes surrounding lines."""
    content = """Line 1

Line 2
Question?
Line 4
- ( ) Answer 1
- (X) Correct answer
- [ ] Mixed type error here
Line 8
Line 9

# reason
Test.
"""
    quiz_file = tmp_path / "context.md"
    quiz_file.write_text(content, encoding="utf-8")

    with pytest.raises(QuizParseError) as exc_info:
        parse_quiz_file(quiz_file)

    err = exc_info.value.parse_error
    assert err is not None

    # Should have context before and after
    assert len(err.context_before) > 0
    assert len(err.context_after) > 0

    # Context should contain actual lines
    assert any("Answer 1" in line or "Correct" in line for line in err.context_before)


def test_question_without_reason(tmp_path: Path) -> None:
    """Test that questions without reason are still valid (reason is optional)."""
    content = """What is the answer?

- (X) Correct
- ( ) Wrong

"""
    quiz_file = tmp_path / "no_reason.md"
    quiz_file.write_text(content, encoding="utf-8")

    # Should parse successfully (reason is optional)
    questions = parse_quiz_file(quiz_file)
    assert len(questions) == 1
    assert questions[0].reason == ""  # Empty reason


def test_error_no_question_text(tmp_path: Path) -> None:
    """Test error when there's no question text."""
    content = """
- (X) Answer 1
- ( ) Answer 2

# reason
Answers without a question.
"""
    quiz_file = tmp_path / "no_question.md"
    quiz_file.write_text(content, encoding="utf-8")

    with pytest.raises(QuizParseError) as exc_info:
        parse_quiz_file(quiz_file)

    # Check detailed error info
    assert exc_info.value.parse_error is not None
    err = exc_info.value.parse_error
    assert "No question text found" in err.error_message
    assert err.block_number == 1
