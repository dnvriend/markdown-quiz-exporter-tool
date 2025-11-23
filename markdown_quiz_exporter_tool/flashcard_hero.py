"""Flashcard Hero TSV exporter for quiz questions.

This module exports parsed quiz questions to Flashcard Hero TSV format.
The TSV format consists of two columns: question and answer, separated by tabs.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import re
from pathlib import Path

from markdown_quiz_exporter_tool.quiz_parser import Question


class FlashcardHeroExporter:
    """Exporter for Flashcard Hero TSV format."""

    def __init__(self, questions: list[Question]) -> None:
        """Initialize the exporter with parsed questions.

        Args:
            questions: List of Question objects to export
        """
        self.questions = questions

    def export(self, output_path: Path) -> int:
        """Export questions to Flashcard Hero TSV format.

        Args:
            output_path: Path where the TSV file will be written

        Returns:
            Number of flashcards exported

        Raises:
            IOError: If writing to file fails
        """
        lines = []

        for question in self.questions:
            front = self._format_question(question.text)
            back = self._format_answer(question)

            # TSV format: front<TAB>back
            line = f"{front}\t{back}"
            lines.append(line)

        # Write to file with UTF-8 encoding
        content = "\n".join(lines) + "\n"
        output_path.write_text(content, encoding="utf-8")

        return len(lines)

    def _format_question(self, text: str) -> str:
        """Format question text for flashcard front.

        Args:
            text: Raw question text

        Returns:
            Formatted question text
        """
        # Remove markdown formatting
        text = self._strip_markdown(text)

        # Normalize whitespace
        text = " ".join(text.split())

        # Remove any tab characters
        text = text.replace("\t", " ")

        return text

    def _format_answer(self, question: Question) -> str:
        """Format answer text for flashcard back.

        This uses Option A: Correct Answer Only
        For multiple correct answers, they are separated by semicolons.

        Args:
            question: Question object with answers

        Returns:
            Formatted answer text
        """
        correct_answers = [ans for ans in question.answers if ans.is_correct]

        if not correct_answers:
            return "No correct answer found"

        # Get answer texts
        answer_texts = [self._format_answer_text(ans.text) for ans in correct_answers]

        # Join multiple answers
        if len(answer_texts) == 1:
            return answer_texts[0]
        else:
            # Multiple correct answers: separate with semicolon
            return "; ".join(answer_texts)

    def _format_answer_text(self, text: str) -> str:
        """Format individual answer text.

        Args:
            text: Raw answer text

        Returns:
            Formatted answer text
        """
        # Remove markdown formatting
        text = self._strip_markdown(text)

        # Normalize whitespace
        text = " ".join(text.split())

        # Remove any tab characters
        text = text.replace("\t", " ")

        return text

    def _strip_markdown(self, text: str) -> str:
        """Remove markdown formatting from text.

        Args:
            text: Text with markdown formatting

        Returns:
            Plain text without markdown
        """
        # Remove bold **text**
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)

        # Remove italic *text*
        text = re.sub(r"\*(.+?)\*", r"\1", text)

        # Remove code `text`
        text = re.sub(r"`(.+?)`", r"\1", text)

        # Remove markdown links [text](url)
        text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)

        return text


def export_to_flashcard_hero(questions: list[Question], output_path: Path) -> int:
    """Export questions to Flashcard Hero TSV format.

    Args:
        questions: List of Question objects to export
        output_path: Path where the TSV file will be written

    Returns:
        Number of flashcards exported

    Raises:
        IOError: If writing to file fails
    """
    exporter = FlashcardHeroExporter(questions)
    return exporter.export(output_path)
