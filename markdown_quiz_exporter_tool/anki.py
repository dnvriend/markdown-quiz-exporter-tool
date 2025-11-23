"""Anki CSV exporter for quiz questions.

This module exports parsed quiz questions to Anki CSV format.
Supports two note types:
- AllInOne: Quiz format with multiple choice questions
- Basic: Simple recall format with question/answer

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import csv
from pathlib import Path

from markdown_quiz_exporter_tool.quiz_parser import Question


class AnkiExporter:
    """Base class for Anki CSV exporters."""

    def __init__(self, questions: list[Question]) -> None:
        """Initialize the exporter with parsed questions.

        Args:
            questions: List of Question objects to export
        """
        self.questions = questions

    def export(self, output_path: Path) -> int:
        """Export questions to Anki CSV format.

        Args:
            output_path: Path where the CSV file will be written

        Returns:
            Number of flashcards exported

        Raises:
            IOError: If writing to file fails
        """
        raise NotImplementedError("Subclasses must implement export()")


class AnkiAllInOneExporter(AnkiExporter):
    """Exporter for Anki AllInOne note type (quiz format)."""

    HEADERS = [
        "#separator:Semicolon",
        "#html:false",
        "#notetype:AllInOne (kprim, mc, sc)",
        "#tags:quiz generated",
    ]

    def export(self, output_path: Path) -> int:
        """Export questions to AllInOne CSV format.

        Args:
            output_path: Path where the CSV file will be written

        Returns:
            Number of flashcards exported

        Raises:
            IOError: If writing to file fails
        """
        with open(output_path, "w", encoding="utf-8", newline="") as csvfile:
            # Write headers
            for header in self.HEADERS:
                csvfile.write(header + "\n")

            writer = csv.writer(csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for question in self.questions:
                row = self._format_question_row(question)
                writer.writerow(row)

        return len(self.questions)

    def _format_question_row(self, question: Question) -> list[str]:
        """Format a question as an AllInOne CSV row.

        Args:
            question: Question object to format

        Returns:
            List of field values for CSV row
        """
        # Field order: Question;Title;QType;Q_1;Q_2;Q_3;Q_4;Q_5;Answers;Sources;Extra1;Tags
        question_field = self._normalize_text(question.text)
        title_field = ""  # Empty title
        qtype_field = self._get_qtype(question)
        q1, q2, q3, q4, q5 = self._format_answer_options(question)
        answers_field = self._format_answers_binary(question)
        sources_field = ""  # Empty sources
        extra1_field = self._normalize_text(question.reason)
        tags_field = "quiz"

        return [
            question_field,
            title_field,
            qtype_field,
            q1,
            q2,
            q3,
            q4,
            q5,
            answers_field,
            sources_field,
            extra1_field,
            tags_field,
        ]

    def _get_qtype(self, question: Question) -> str:
        """Determine QType for the question.

        Args:
            question: Question object

        Returns:
            "2" for single choice, "1" for multiple choice
        """
        correct_count = sum(1 for ans in question.answers if ans.is_correct)

        # Single choice if radio buttons or exactly one correct answer
        if question.question_type == "single" or correct_count == 1:
            return "2"
        else:
            return "1"

    def _format_answer_options(self, question: Question) -> tuple[str, str, str, str, str]:
        """Format answer options for Q_1 through Q_5 fields.

        Args:
            question: Question object

        Returns:
            Tuple of 5 answer strings (padded with empty strings if needed)
        """
        options = [self._normalize_text(ans.text) for ans in question.answers]

        # Pad with empty strings to have exactly 5 options
        while len(options) < 5:
            options.append("")

        # Truncate if more than 5 (should warn in CLI)
        return (options[0], options[1], options[2], options[3], options[4])

    def _format_answers_binary(self, question: Question) -> str:
        """Format answers field as binary string.

        Args:
            question: Question object

        Returns:
            Space-separated binary string (e.g., "1 0 1 0 0")
        """
        binary = ["0"] * 5

        for i, answer in enumerate(question.answers):
            if i < 5 and answer.is_correct:
                binary[i] = "1"

        return " ".join(binary)

    def _normalize_text(self, text: str) -> str:
        """Normalize text for CSV output.

        Args:
            text: Input text

        Returns:
            Normalized text (single line, trimmed)
        """
        # Join multiple lines into single line
        text = " ".join(text.split())
        return text.strip()


class AnkiBasicExporter(AnkiExporter):
    """Exporter for Anki Basic note type (recall format)."""

    HEADERS = [
        "#separator:Semicolon",
        "#html:false",
        "#notetype:Basic",
        "#tags:quiz recall",
    ]

    def export(self, output_path: Path) -> int:
        """Export questions to Basic CSV format.

        Args:
            output_path: Path where the CSV file will be written

        Returns:
            Number of flashcards exported

        Raises:
            IOError: If writing to file fails
        """
        with open(output_path, "w", encoding="utf-8", newline="") as csvfile:
            # Write headers
            for header in self.HEADERS:
                csvfile.write(header + "\n")

            writer = csv.writer(csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for question in self.questions:
                row = self._format_question_row(question)
                writer.writerow(row)

        return len(self.questions)

    def _format_question_row(self, question: Question) -> list[str]:
        """Format a question as a Basic CSV row.

        Args:
            question: Question object to format

        Returns:
            List of field values for CSV row (Front, Back, Tags)
        """
        front = self._normalize_text(question.text)
        back = self._format_back(question)
        tags = "recall"

        return [front, back, tags]

    def _format_back(self, question: Question) -> str:
        """Format the back side with answers and explanation.

        Args:
            question: Question object

        Returns:
            Formatted back side text
        """
        correct_answers = [ans.text for ans in question.answers if ans.is_correct]

        # Format answer section
        if len(correct_answers) == 1:
            answer_text = f"Answer: {correct_answers[0]}"
        else:
            answer_text = "Answers: " + ", ".join(correct_answers)

        # Add explanation if available
        if question.reason.strip():
            explanation = self._normalize_text(question.reason)
            # Use <br> tags for line breaks in Anki
            return f"{answer_text}<br><br>Explanation: {explanation}"
        else:
            return answer_text

    def _normalize_text(self, text: str) -> str:
        """Normalize text for CSV output.

        Args:
            text: Input text

        Returns:
            Normalized text (single line, trimmed)
        """
        # Join multiple lines into single line
        text = " ".join(text.split())
        return text.strip()


def export_to_anki_allinone(questions: list[Question], output_path: Path) -> int:
    """Export questions to Anki AllInOne CSV format.

    Args:
        questions: List of Question objects to export
        output_path: Path where the CSV file will be written

    Returns:
        Number of flashcards exported

    Raises:
        IOError: If writing to file fails
    """
    exporter = AnkiAllInOneExporter(questions)
    return exporter.export(output_path)


def export_to_anki_basic(questions: list[Question], output_path: Path) -> int:
    """Export questions to Anki Basic CSV format.

    Args:
        questions: List of Question objects to export
        output_path: Path where the CSV file will be written

    Returns:
        Number of flashcards exported

    Raises:
        IOError: If writing to file fails
    """
    exporter = AnkiBasicExporter(questions)
    return exporter.export(output_path)
