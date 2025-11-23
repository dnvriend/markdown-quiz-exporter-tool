"""Quiz markdown parser for extracting questions and answers from quiz files.

This module parses quiz markdown files following the format specification.
It extracts questions, answer options, correct answers, and reasoning sections.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Answer:
    """Represents an answer option for a quiz question."""

    text: str
    is_correct: bool


@dataclass
class Question:
    """Represents a quiz question with answers and reasoning."""

    text: str
    answers: list[Answer]
    reason: str
    question_type: str  # "single" or "multiple"


class QuizParseError(Exception):
    """Exception raised when quiz parsing fails."""

    pass


class QuizParser:
    """Parser for quiz markdown files."""

    # Regex patterns
    SINGLE_CHOICE_PATTERN = re.compile(r"^-\s+\(([Xx ])\)\s+(.+)$")
    MULTIPLE_CHOICE_PATTERN = re.compile(r"^-\s+\[([Xx ])\]\s+(.+)$")
    QUESTION_SEPARATOR = "---"
    REASON_MARKER = "# reason"

    def __init__(self, file_path: Path) -> None:
        """Initialize the parser with a quiz markdown file.

        Args:
            file_path: Path to the quiz markdown file
        """
        self.file_path = file_path
        self.questions: list[Question] = []

    def parse(self) -> list[Question]:
        """Parse the quiz markdown file and extract questions.

        Returns:
            List of Question objects

        Raises:
            QuizParseError: If parsing fails
            FileNotFoundError: If the file doesn't exist
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Quiz file not found: {self.file_path}")

        content = self.file_path.read_text(encoding="utf-8")

        # Split into question blocks
        blocks = content.split(self.QUESTION_SEPARATOR)

        for i, block in enumerate(blocks):
            block = block.strip()
            if not block:
                continue

            try:
                question = self._parse_question_block(block)
                self.questions.append(question)
            except Exception as e:
                raise QuizParseError(f"Error parsing question block {i + 1}: {e}") from e

        if not self.questions:
            raise QuizParseError("No questions found in the quiz file")

        return self.questions

    def _parse_question_block(self, block: str) -> Question:
        """Parse a single question block.

        Args:
            block: The text block containing one question

        Returns:
            Question object

        Raises:
            QuizParseError: If the block format is invalid
        """
        lines = [line for line in block.split("\n")]

        # Extract question text (everything before the first answer option)
        question_text_lines = []
        answer_start_idx = 0

        for i, line in enumerate(lines):
            if self._is_answer_line(line):
                answer_start_idx = i
                break
            if line.strip():
                question_text_lines.append(line.strip())

        if not question_text_lines:
            raise QuizParseError("No question text found")

        question_text = " ".join(question_text_lines)

        # Extract answers
        answers = []
        question_type = None
        reason_start_idx = len(lines)

        for i in range(answer_start_idx, len(lines)):
            line = lines[i].strip()

            if line == self.REASON_MARKER:
                reason_start_idx = i
                break

            if not line:
                continue

            # Try single choice pattern
            match = self.SINGLE_CHOICE_PATTERN.match(line)
            if match:
                if question_type is None:
                    question_type = "single"
                elif question_type != "single":
                    raise QuizParseError("Mixed answer types (single and multiple choice)")

                is_correct = match.group(1).upper() == "X"
                answer_text = match.group(2).strip()
                answers.append(Answer(text=answer_text, is_correct=is_correct))
                continue

            # Try multiple choice pattern
            match = self.MULTIPLE_CHOICE_PATTERN.match(line)
            if match:
                if question_type is None:
                    question_type = "multiple"
                elif question_type != "multiple":
                    raise QuizParseError("Mixed answer types (single and multiple choice)")

                is_correct = match.group(1).upper() == "X"
                answer_text = match.group(2).strip()
                answers.append(Answer(text=answer_text, is_correct=is_correct))
                continue

        if not answers:
            raise QuizParseError("No answers found")

        if not any(a.is_correct for a in answers):
            raise QuizParseError("No correct answer marked")

        # Extract reason section
        reason_lines = []
        for i in range(reason_start_idx + 1, len(lines)):
            line = lines[i].strip()
            if line:
                reason_lines.append(line)

        reason = " ".join(reason_lines) if reason_lines else ""

        return Question(
            text=question_text,
            answers=answers,
            reason=reason,
            question_type=question_type or "single",
        )

    def _is_answer_line(self, line: str) -> bool:
        """Check if a line is an answer option.

        Args:
            line: The line to check

        Returns:
            True if the line matches answer format
        """
        return bool(
            self.SINGLE_CHOICE_PATTERN.match(line) or self.MULTIPLE_CHOICE_PATTERN.match(line)
        )


def parse_quiz_file(file_path: Path) -> list[Question]:
    """Parse a quiz markdown file.

    Args:
        file_path: Path to the quiz markdown file

    Returns:
        List of Question objects

    Raises:
        QuizParseError: If parsing fails
        FileNotFoundError: If the file doesn't exist
    """
    parser = QuizParser(file_path)
    return parser.parse()
