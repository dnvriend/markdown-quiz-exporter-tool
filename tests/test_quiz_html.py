"""Tests for quiz HTML generator.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
from pathlib import Path

import pytest

from markdown_quiz_exporter_tool.quiz_html import QuizHTMLGenerator, export_to_quiz_html
from markdown_quiz_exporter_tool.quiz_parser import Answer, Question


@pytest.fixture
def single_choice_question() -> Question:
    """Create a single choice question."""
    return Question(
        text="S3: What is the max size of an S3 object in GB?",
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


def test_quiz_html_generation_basic(tmp_path: Path, single_choice_question: Question) -> None:
    """Test basic HTML generation."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test Quiz")

    file_size = generator.generate(output)

    assert output.exists()
    assert file_size > 0

    content = output.read_text(encoding="utf-8")

    # Verify HTML structure
    assert "<!DOCTYPE html>" in content
    assert '<html lang="nl">' in content
    assert "<title>Test Quiz</title>" in content
    assert "</html>" in content


def test_tailwind_cdn_included(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that Tailwind CSS CDN is included."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test")

    generator.generate(output)
    content = output.read_text()

    assert "cdn.tailwindcss.com" in content


def test_quiz_data_embedded(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that quiz data is embedded as JSON."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test Quiz")

    generator.generate(output)
    content = output.read_text()

    # Check for quiz data
    assert "const QUIZ_DATA = " in content
    assert "What is the max size" in content  # Question text without category
    assert "5000" in content


def test_quiz_app_javascript_included(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that QuizApp JavaScript is included."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test")

    generator.generate(output)
    content = output.read_text()

    # Check for quiz application code
    assert "class QuizApp" in content
    assert "constructor(quizData)" in content
    assert "initializeState()" in content
    assert "render()" in content


def test_dark_mode_support(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that dark mode support is included."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test")

    generator.generate(output)
    content = output.read_text()

    # Check for dark mode classes
    assert "dark:bg-gray-900" in content
    assert "dark:bg-gray-800" in content
    assert "darkMode: 'class'" in content  # Tailwind dark mode config
    assert "detectDarkMode()" in content  # System preference detection


def test_category_extraction(tmp_path: Path) -> None:
    """Test category extraction from question text."""
    question = Question(
        text="STAKEHOLDERS: Bij welke stakeholders ligt het belang?",
        answers=[Answer(text="Test", is_correct=True)],
        reason="Test reason",
        question_type="single",
    )

    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([question], "Test")

    generator.generate(output)
    content = output.read_text()

    # Category should be extracted and clean question text used
    assert "STAKEHOLDERS" in content
    assert "Bij welke stakeholders ligt het belang?" in content


def test_multiple_questions(
    tmp_path: Path,
    single_choice_question: Question,
    multiple_choice_question: Question,
) -> None:
    """Test generation with multiple questions."""
    output = tmp_path / "test.html"
    questions = [single_choice_question, multiple_choice_question]

    file_size = export_to_quiz_html(questions, output, "Multi Question Quiz")

    assert output.exists()
    assert file_size > 0

    content = output.read_text()

    # Check both questions are in the data
    assert "S3 object" in content
    assert "leadership" in content


def test_html_escaping(tmp_path: Path) -> None:
    """Test that HTML is properly escaped."""
    question = Question(
        text="What does <script>alert('xss')</script> do?",
        answers=[
            Answer(text="It's <dangerous>", is_correct=True),
        ],
        reason="This & that",
        question_type="single",
    )

    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([question], "Test & Quiz")

    generator.generate(output)
    content = output.read_text()

    # Title should be escaped
    assert "<title>Test &amp; Quiz</title>" in content


def test_question_to_dict_structure(single_choice_question: Question) -> None:
    """Test question dictionary structure."""
    generator = QuizHTMLGenerator([single_choice_question], "Test")
    result = generator._question_to_dict(single_choice_question)

    assert "category" in result
    assert "text" in result
    assert "type" in result
    assert "answers" in result
    assert "reason" in result

    assert result["type"] == "single"
    assert len(result["answers"]) == 3  # type: ignore
    assert result["answers"][1]["correct"] is True  # type: ignore


def test_quiz_data_json_format(single_choice_question: Question) -> None:
    """Test that quiz data is valid JSON."""
    generator = QuizHTMLGenerator([single_choice_question], "Test")

    # Test the JSON directly
    json_str = generator._build_quiz_data()
    data = json.loads(json_str)

    assert data["title"] == "Test"
    assert len(data["questions"]) == 1
    assert data["questions"][0]["type"] == "single"


def test_responsive_classes(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that responsive classes are included."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test")

    generator.generate(output)
    content = output.read_text()

    # Check for responsive breakpoints
    assert "md:grid-cols-2" in content or "sm:" in content or "lg:" in content


def test_session_storage_code(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that session storage code is included."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test")

    generator.generate(output)
    content = output.read_text()

    assert "sessionStorage" in content
    assert "saveState()" in content
    assert "loadState()" in content


def test_navigation_functions(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that navigation functions are included."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test")

    generator.generate(output)
    content = output.read_text()

    assert "goToIntro()" in content
    assert "goToQuestion(" in content
    assert "goToStatistics()" in content
    assert "goToReview(" in content
    assert "nextQuestion()" in content
    assert "previousQuestion()" in content


def test_shuffle_functions(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that shuffle functionality is included."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test")

    generator.generate(output)
    content = output.read_text()

    assert "shuffleArray(" in content
    assert "applyShuffling()" in content
    assert "shuffleQuestions" in content
    assert "shuffleAnswers" in content


def test_file_size_reasonable(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that generated file size is reasonable."""
    output = tmp_path / "test.html"
    questions = [single_choice_question] * 10  # 10 questions

    file_size = export_to_quiz_html(questions, output, "Test")

    # Should be less than 100KB for 10 questions
    assert file_size < 100 * 1024

    # Should be more than 20KB (has embedded JS)
    assert file_size > 20 * 1024


def test_markdown_rendering_support(tmp_path: Path, single_choice_question: Question) -> None:
    """Test that markdown rendering is included."""
    output = tmp_path / "test.html"
    generator = QuizHTMLGenerator([single_choice_question], "Test")

    generator.generate(output)
    content = output.read_text()

    # Check for marked.js CDN
    assert "marked" in content
    assert "jsdelivr.net/npm/marked" in content

    # Check for renderMarkdown function
    assert "renderMarkdown(text)" in content
    assert "marked.parse" in content
