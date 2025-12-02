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


@dataclass
class ParseError:
    """Detailed information about a parsing error."""

    line_number: int
    line_content: str
    error_message: str
    block_number: int
    context_before: list[str]
    context_after: list[str]


class QuizParseError(Exception):
    """Exception raised when quiz parsing fails."""

    def __init__(self, message: str, parse_error: ParseError | None = None) -> None:
        """Initialize with error message and optional detailed error info.

        Args:
            message: Error message
            parse_error: Detailed parsing error information
        """
        super().__init__(message)
        self.parse_error = parse_error


class QuizParser:
    """Parser for quiz markdown files."""

    # Regex patterns - allow empty or non-empty text after marker
    SINGLE_CHOICE_PATTERN = re.compile(r"^-\s+\(([Xx ])\)\s*(.*)$")
    MULTIPLE_CHOICE_PATTERN = re.compile(r"^-\s+\[([Xx ])\]\s*(.*)$")
    QUESTION_SEPARATOR = "---"
    REASON_MARKER = "# reason"

    def __init__(self, file_path: Path) -> None:
        """Initialize the parser with a quiz markdown file.

        Args:
            file_path: Path to the quiz markdown file
        """
        self.file_path = file_path
        self.questions: list[Question] = []
        self.all_lines: list[str] = []  # Store all lines for error reporting
        self.line_offset: int = 0  # Track current line offset in file

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
        self.all_lines = content.split("\n")

        # Split into question blocks
        blocks = content.split(self.QUESTION_SEPARATOR)

        current_line = 0
        for i, block in enumerate(blocks):
            # Track line offset for this block
            self.line_offset = current_line

            # Count lines in this block including separator
            block_line_count = block.count("\n") + 1
            if i < len(blocks) - 1:  # Add separator line except for last block
                block_line_count += 1

            block = block.strip()
            if not block:
                current_line += block_line_count
                continue

            try:
                question = self._parse_question_block(block, i + 1)
                self.questions.append(question)
            except QuizParseError:
                raise
            except Exception as e:
                # Create generic error without line info
                raise QuizParseError(f"Error parsing question block {i + 1}: {e}") from e

            current_line += block_line_count

        if not self.questions:
            raise QuizParseError("No questions found in the quiz file")

        return self.questions

    def _parse_question_block(self, block: str, block_number: int) -> Question:
        """Parse a single question block.

        Args:
            block: The text block containing one question
            block_number: The question block number (1-indexed)

        Returns:
            Question object

        Raises:
            QuizParseError: If the block format is invalid
        """
        lines = [line for line in block.split("\n")]

        # Extract question text (everything before the first answer option)
        # Preserve newlines for markdown rendering
        question_text_lines = []
        answer_start_idx = 0

        for i, line in enumerate(lines):
            if self._is_answer_line(line):
                answer_start_idx = i
                break
            question_text_lines.append(line)

        # Join with newlines to preserve markdown structure (codeblocks, etc.)
        question_text = "\n".join(question_text_lines).strip()

        if not question_text:
            self._raise_parse_error(
                0, lines[0] if lines else "", "No question text found", block_number, lines
            )

        # Extract answers with multi-line support
        answers = []
        question_type = None
        reason_start_idx = len(lines)

        i = answer_start_idx
        while i < len(lines):
            line = lines[i]

            # Check for reason marker (case-insensitive, stripped)
            if line.strip().lower() == self.REASON_MARKER.lower():
                reason_start_idx = i
                break

            # Try to match answer marker
            match = self.SINGLE_CHOICE_PATTERN.match(line)
            answer_type = "single"
            if not match:
                match = self.MULTIPLE_CHOICE_PATTERN.match(line)
                answer_type = "multiple"

            if match:
                # Validate question type consistency
                if question_type is None:
                    question_type = answer_type
                elif question_type != answer_type:
                    self._raise_parse_error(
                        i,
                        line,
                        "Mixed answer types: Cannot mix ( ) and [ ] formats in same question",
                        block_number,
                        lines,
                    )

                is_correct = match.group(1).upper() == "X"
                first_line_text = match.group(2)

                # Collect multi-line answer content
                answer_lines = [first_line_text] if first_line_text else []
                i += 1

                # Collect subsequent lines until next answer marker, reason, or end
                while i < len(lines):
                    next_line = lines[i]
                    # Stop if we hit another answer marker or reason
                    if self._is_answer_line(next_line):
                        break
                    if next_line.strip().lower() == self.REASON_MARKER.lower():
                        break
                    answer_lines.append(next_line)
                    i += 1

                # Join answer lines preserving structure for markdown
                answer_text = "\n".join(answer_lines).strip()
                answers.append(Answer(text=answer_text, is_correct=is_correct))
            else:
                # Skip empty lines between answers
                i += 1

        if not answers:
            # Find first line after question
            line_idx = answer_start_idx if answer_start_idx < len(lines) else 0
            self._raise_parse_error(
                line_idx,
                lines[line_idx] if line_idx < len(lines) else "",
                "No answers found. Expected format: '- (X) text' or '- [X] text'",
                block_number,
                lines,
            )

        if not any(a.is_correct for a in answers):
            # Find first answer line
            for i in range(answer_start_idx, len(lines)):
                if self._is_answer_line(lines[i]):
                    self._raise_parse_error(
                        i,
                        lines[i],
                        "No correct answer marked. Use (X) or [X] to mark correct answers",
                        block_number,
                        lines,
                    )
                    break

        # Extract reason section - preserve newlines for markdown
        reason_lines = []
        for i in range(reason_start_idx + 1, len(lines)):
            reason_lines.append(lines[i])

        reason = "\n".join(reason_lines).strip()

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

    def _raise_parse_error(
        self,
        line_idx_in_block: int,
        line_content: str,
        error_message: str,
        block_number: int,
        block_lines: list[str],
    ) -> None:
        """Raise a QuizParseError with detailed line information.

        Args:
            line_idx_in_block: Line index within the block (0-indexed)
            line_content: Content of the problematic line
            error_message: Description of the error
            block_number: Question block number (1-indexed)
            block_lines: All lines in the current block

        Raises:
            QuizParseError: Always raised with detailed error info
        """
        # Calculate absolute line number in file
        absolute_line = self.line_offset + line_idx_in_block + 1  # +1 for 1-indexed

        # Get context lines (2 before, 2 after)
        context_before = []
        context_after = []

        for i in range(max(0, line_idx_in_block - 2), line_idx_in_block):
            if i < len(block_lines):
                context_before.append(block_lines[i])

        for i in range(line_idx_in_block + 1, min(len(block_lines), line_idx_in_block + 3)):
            context_after.append(block_lines[i])

        parse_error = ParseError(
            line_number=absolute_line,
            line_content=line_content,
            error_message=error_message,
            block_number=block_number,
            context_before=context_before,
            context_after=context_after,
        )

        raise QuizParseError(f"Error at line {absolute_line}: {error_message}", parse_error)


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
