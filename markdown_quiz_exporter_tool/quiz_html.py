"""HTML quiz generator for interactive single-page quiz applications.

This module generates self-contained HTML files with embedded quiz data,
CSS styling (Tailwind), and JavaScript application logic.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import html
import json
from pathlib import Path

from markdown_quiz_exporter_tool.quiz_parser import Question


class QuizHTMLGenerator:
    """Generator for interactive HTML quiz pages."""

    def __init__(self, questions: list[Question], title: str) -> None:
        """Initialize the HTML generator.

        Args:
            questions: List of Question objects to include in quiz
            title: Quiz title displayed on intro page
        """
        self.questions = questions
        self.title = title

    def generate(self, output_path: Path) -> int:
        """Generate complete HTML quiz file.

        Args:
            output_path: Path where HTML file will be written

        Returns:
            File size in bytes

        Raises:
            OSError: If writing to file fails
        """
        html_content = self._build_html()
        output_path.write_text(html_content, encoding="utf-8")
        return len(html_content.encode("utf-8"))

    def _build_html(self) -> str:
        """Build complete HTML document.

        Returns:
            Complete HTML document as string
        """
        return f"""<!DOCTYPE html>
<html lang="nl">
{self._build_head()}
{self._build_body()}
</html>"""

    def _build_head(self) -> str:
        """Build HTML head section.

        Returns:
            HTML head section with meta tags, title, and styles
        """
        escaped_title = html.escape(self.title)
        return f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escaped_title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked@11.1.1/marked.min.js"></script>
    {self._build_styles()}
</head>"""

    def _build_styles(self) -> str:
        """Build embedded CSS styles.

        Returns:
            Style tag with custom CSS
        """
        return """<style>
        /* Smooth transitions */
        * {
            transition-property: color, background-color, border-color;
            transition-duration: 200ms;
        }

        /* Progress bar animation */
        .progress-bar {
            transition: width 300ms ease-in-out;
        }

        /* Hide elements */
        .hidden {
            display: none !important;
        }

        /* Custom scrollbar for dark mode */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgb(31 41 55);
        }

        ::-webkit-scrollbar-thumb {
            background: rgb(75 85 99);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgb(107 114 128);
        }

        /* Focus visible for accessibility */
        button:focus-visible,
        input:focus-visible {
            outline: 2px solid rgb(59 130 246);
            outline-offset: 2px;
        }
    </style>"""

    def _build_body(self) -> str:
        """Build HTML body section.

        Returns:
            HTML body with app container and embedded scripts
        """
        return f"""<body class="bg-gray-50 dark:bg-gray-900 min-h-screen">
    <!-- Theme toggle button (fixed position) -->
    <button id="theme-toggle"
            class="fixed top-4 right-4 z-50 p-3 rounded-lg bg-white dark:bg-gray-800 shadow-xl hover:shadow-2xl border-2 border-gray-200 dark:border-gray-600"
            aria-label="Toggle dark mode">
        <svg id="sun-icon" class="w-7 h-7 text-yellow-500 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <svg id="moon-icon" class="w-7 h-7 text-indigo-600 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
    </button>

    <!-- App container -->
    <div id="app" class="container mx-auto px-4 py-8 max-w-4xl"></div>

    <!-- Quiz data -->
    <script>
        const QUIZ_DATA = {self._build_quiz_data()};
    </script>

    <!-- Quiz application -->
    <script>
        {self._build_javascript()}
    </script>
</body>"""

    def _build_quiz_data(self) -> str:
        """Convert questions to JSON format.

        Returns:
            JSON string with quiz data
        """
        quiz_data = {
            "title": self.title,
            "questions": [self._question_to_dict(q) for q in self.questions],
        }
        return json.dumps(quiz_data, ensure_ascii=False, separators=(",", ":"))

    def _question_to_dict(self, question: Question) -> dict[str, object]:
        """Convert Question object to dictionary.

        Args:
            question: Question object to convert

        Returns:
            Dictionary representation of question
        """
        # Extract category from question text if present
        category = self._extract_category(question.text)
        clean_text = self._clean_question_text(question.text)

        return {
            "category": category,
            "text": clean_text,
            "type": question.question_type,
            "answers": [{"text": ans.text, "correct": ans.is_correct} for ans in question.answers],
            "reason": question.reason,
        }

    def _extract_category(self, text: str) -> str:
        """Extract category tag from question text.

        Args:
            text: Question text that may contain category prefix

        Returns:
            Category name or empty string
        """
        # Look for pattern: "CATEGORY: Question text"
        if ":" in text:
            parts = text.split(":", 1)
            potential_category = parts[0].strip()
            # Check if it's all caps and short (likely a category)
            if potential_category.isupper() and len(potential_category) < 30:
                return potential_category
        return ""

    def _clean_question_text(self, text: str) -> str:
        """Remove category prefix from question text.

        Args:
            text: Question text that may contain category prefix

        Returns:
            Clean question text
        """
        category = self._extract_category(text)
        if category:
            return text.split(":", 1)[1].strip()
        return text

    def _build_javascript(self) -> str:
        """Build embedded JavaScript application.

        Returns:
            Complete JavaScript quiz application code
        """
        # ruff: noqa: E501
        # Long lines in HTML/JS templates are acceptable for readability
        return """
// Quiz Application
class QuizApp {
    constructor(quizData) {
        this.quizData = quizData;
        this.state = this.loadState() || this.initializeState();
        this.init();
    }

    // Initialize application
    init() {
        // Set up theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => this.toggleDarkMode());

        // Apply saved dark mode preference
        if (this.state.config.darkMode) {
            document.documentElement.classList.add('dark');
        }

        // Render initial page
        this.render();
    }

    // Initialize default state
    initializeState() {
        return {
            currentPage: 'intro',
            currentQuestionIndex: 0,
            config: {
                shuffleQuestions: false,
                shuffleAnswers: false,
                autoAdvance: false,
                autoAdvanceDelay: 3,
                darkMode: this.detectDarkMode()
            },
            questions: this.prepareQuestions(),
            answers: {},
            checked: {},
            startTime: null,
            endTime: null
        };
    }

    // Detect system dark mode preference
    detectDarkMode() {
        if (window.matchMedia) {
            return window.matchMedia('(prefers-color-scheme: dark)').matches;
        }
        return false;
    }

    // Prepare questions (with shuffling if configured)
    prepareQuestions() {
        let questions = [...this.quizData.questions];

        // Note: Shuffling will be applied when starting quiz from intro
        return questions.map((q, index) => ({
            ...q,
            originalIndex: index,
            answers: q.answers.map((a, i) => ({ ...a, originalIndex: i }))
        }));
    }

    // Apply shuffling based on config
    applyShuffling() {
        if (this.state.config.shuffleQuestions) {
            this.state.questions = this.shuffleArray(this.state.questions);
        }

        if (this.state.config.shuffleAnswers) {
            this.state.questions = this.state.questions.map(q => ({
                ...q,
                answers: this.shuffleArray([...q.answers])
            }));
        }
    }

    // Shuffle array (Fisher-Yates algorithm)
    shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    // State management
    saveState() {
        try {
            sessionStorage.setItem('quizState', JSON.stringify(this.state));
        } catch (e) {
            console.error('Failed to save state:', e);
        }
    }

    loadState() {
        try {
            const saved = sessionStorage.getItem('quizState');
            return saved ? JSON.parse(saved) : null;
        } catch (e) {
            console.error('Failed to load state:', e);
            return null;
        }
    }

    clearState() {
        try {
            sessionStorage.removeItem('quizState');
        } catch (e) {
            console.error('Failed to clear state:', e);
        }
    }

    // Toggle dark mode
    toggleDarkMode() {
        const html = document.documentElement;
        const isDark = html.classList.contains('dark');

        if (isDark) {
            html.classList.remove('dark');
        } else {
            html.classList.add('dark');
        }

        this.state.config.darkMode = !isDark;
        this.saveState();
    }

    // Navigation
    goToIntro() {
        this.state.currentPage = 'intro';
        this.saveState();
        this.render();
    }

    goToQuestion(index) {
        this.state.currentPage = 'question';
        this.state.currentQuestionIndex = index;
        this.saveState();
        this.render();
    }

    goToStatistics() {
        this.state.currentPage = 'statistics';
        this.state.endTime = Date.now();
        this.saveState();
        this.render();
    }

    goToReview(index) {
        this.state.currentPage = 'review';
        this.state.currentQuestionIndex = index;
        this.saveState();
        this.render();
    }

    nextQuestion() {
        if (this.state.currentQuestionIndex < this.state.questions.length - 1) {
            this.goToQuestion(this.state.currentQuestionIndex + 1);
        } else {
            this.goToStatistics();
        }
    }

    previousQuestion() {
        if (this.state.currentQuestionIndex > 0) {
            this.goToQuestion(this.state.currentQuestionIndex - 1);
        }
    }

    // Quiz logic
    startQuiz() {
        this.applyShuffling();
        this.state.startTime = Date.now();
        this.state.currentPage = 'question';
        this.state.currentQuestionIndex = 0;
        this.state.answers = {};
        this.state.checked = {};
        this.saveState();
        this.render();
    }

    selectAnswer(questionIndex, answerIndex, isMultiple) {
        if (this.state.checked[questionIndex]) {
            return; // Already checked, can't change
        }

        if (!this.state.answers[questionIndex]) {
            this.state.answers[questionIndex] = [];
        }

        if (isMultiple) {
            // Toggle checkbox
            const idx = this.state.answers[questionIndex].indexOf(answerIndex);
            if (idx > -1) {
                this.state.answers[questionIndex].splice(idx, 1);
            } else {
                this.state.answers[questionIndex].push(answerIndex);
            }
        } else {
            // Radio button - single selection
            this.state.answers[questionIndex] = [answerIndex];
        }

        this.saveState();
        this.render();
    }

    checkAnswer(questionIndex) {
        const selectedIndices = this.state.answers[questionIndex] || [];

        if (selectedIndices.length === 0) {
            alert('Selecteer eerst een antwoord');
            return;
        }

        this.state.checked[questionIndex] = true;
        this.saveState();
        this.render();
    }

    isAnswerCorrect(questionIndex) {
        const question = this.state.questions[questionIndex];
        const selectedIndices = this.state.answers[questionIndex] || [];
        const correctIndices = question.answers
            .map((a, i) => a.correct ? i : -1)
            .filter(i => i !== -1);

        if (selectedIndices.length !== correctIndices.length) {
            return false;
        }

        const sortedSelected = [...selectedIndices].sort();
        const sortedCorrect = [...correctIndices].sort();

        return sortedSelected.every((val, idx) => val === sortedCorrect[idx]);
    }

    calculateScore() {
        const total = this.state.questions.length;
        const answered = Object.keys(this.state.checked).length;
        const correct = Object.keys(this.state.checked)
            .filter(i => this.isAnswerCorrect(parseInt(i)))
            .length;

        return {
            total,
            answered,
            correct,
            percentage: total > 0 ? Math.round((correct / total) * 100) : 0
        };
    }

    getElapsedTime() {
        if (!this.state.startTime) return 0;
        const end = this.state.endTime || Date.now();
        return end - this.state.startTime;
    }

    formatTime(milliseconds) {
        const seconds = Math.floor(milliseconds / 1000);
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return minutes + ':' + remainingSeconds.toString().padStart(2, '0');
    }

    restartQuiz() {
        this.clearState();
        this.state = this.initializeState();
        this.saveState();
        this.render();
    }

    // Master render function
    render() {
        const app = document.getElementById('app');

        if (this.state.currentPage === 'intro') {
            app.innerHTML = this.renderIntro();
        } else if (this.state.currentPage === 'question') {
            app.innerHTML = this.renderQuestion(this.state.currentQuestionIndex);
        } else if (this.state.currentPage === 'statistics') {
            app.innerHTML = this.renderStatistics();
        } else if (this.state.currentPage === 'review') {
            app.innerHTML = this.renderReview(this.state.currentQuestionIndex);
        }

        // Attach event listeners after rendering
        this.attachEventListeners();
    }

    // Render intro/config page
    renderIntro() {
        const questionCount = this.quizData.questions.length;

        return `
            <div class="max-w-2xl mx-auto">
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
                    <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-4">
                        ${this.escapeHtml(this.quizData.title)}
                    </h1>

                    <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
                        Deze quiz bevat <strong>${questionCount}</strong> vragen.
                    </p>

                    <div class="space-y-4 mb-8">
                        <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
                            Instellingen
                        </h2>

                        <label class="flex items-center space-x-3 cursor-pointer">
                            <input type="checkbox"
                                   id="shuffle-questions"
                                   ${this.state.config.shuffleQuestions ? 'checked' : ''}
                                   class="w-5 h-5 text-blue-600 rounded">
                            <span class="text-gray-700 dark:text-gray-300">
                                Vragen in willekeurige volgorde
                            </span>
                        </label>

                        <label class="flex items-center space-x-3 cursor-pointer">
                            <input type="checkbox"
                                   id="shuffle-answers"
                                   ${this.state.config.shuffleAnswers ? 'checked' : ''}
                                   class="w-5 h-5 text-blue-600 rounded">
                            <span class="text-gray-700 dark:text-gray-300">
                                Antwoorden in willekeurige volgorde
                            </span>
                        </label>

                        <label class="flex items-center space-x-3 cursor-pointer">
                            <input type="checkbox"
                                   id="auto-advance"
                                   ${this.state.config.autoAdvance ? 'checked' : ''}
                                   class="w-5 h-5 text-blue-600 rounded">
                            <span class="text-gray-700 dark:text-gray-300">
                                Automatisch naar volgende vraag (na
                                <input type="number"
                                       id="auto-advance-delay"
                                       min="1"
                                       max="10"
                                       value="${this.state.config.autoAdvanceDelay}"
                                       class="w-12 px-2 py-1 text-center border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                                seconden)
                            </span>
                        </label>
                    </div>

                    <button id="start-quiz"
                            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-lg shadow-lg hover:shadow-xl">
                        Start Quiz →
                    </button>
                </div>
            </div>
        `;
    }

    // Render question page - CONTINUING IN NEXT PART...
    renderQuestion(index) {
        const question = this.state.questions[index];
        const isChecked = this.state.checked[index];
        const selectedIndices = this.state.answers[index] || [];
        const progress = ((index + 1) / this.state.questions.length) * 100;
        const isMultiple = question.type === 'multiple';

        let answersHtml = '';
        question.answers.forEach((answer, answerIndex) => {
            const isSelected = selectedIndices.includes(answerIndex);
            const isCorrect = answer.correct;

            let borderClass = 'border-gray-200 dark:border-gray-700';
            let bgClass = 'bg-white dark:bg-gray-800';
            let icon = '';

            if (isChecked) {
                if (isCorrect) {
                    borderClass = 'border-green-500';
                    bgClass = 'bg-green-50 dark:bg-green-900/20';
                    icon = '<span class="text-green-600 font-bold">✓</span>';
                } else if (isSelected) {
                    borderClass = 'border-red-500';
                    bgClass = 'bg-red-50 dark:bg-red-900/20';
                    icon = '<span class="text-red-600 font-bold">✗</span>';
                }
            } else if (isSelected) {
                borderClass = 'border-blue-500';
                bgClass = 'bg-blue-50 dark:bg-blue-900/20';
            }

            const inputType = isMultiple ? 'checkbox' : 'radio';
            const inputName = isMultiple ? '' : 'answer-' + index;

            answersHtml += `
                <div class="border-2 ${borderClass} ${bgClass} rounded-lg p-4 cursor-pointer hover:border-blue-400 transition-colors"
                     data-answer-index="${answerIndex}">
                    <label class="flex items-center cursor-pointer">
                        <input type="${inputType}"
                               ${inputName ? 'name="' + inputName + '"' : ''}
                               ${isSelected ? 'checked' : ''}
                               ${isChecked ? 'disabled' : ''}
                               class="w-5 h-5 text-blue-600 mr-3">
                        <span class="flex-1 text-gray-900 dark:text-gray-100">
                            ${this.escapeHtml(answer.text)}
                        </span>
                        ${icon}
                    </label>
                </div>
            `;
        });

        const reasonHtml = isChecked ? `
            <div class="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 rounded">
                <div class="flex items-center mb-2">
                    <span class="text-2xl mr-2">💡</span>
                    <span class="font-semibold text-blue-900 dark:text-blue-100">Uitleg</span>
                </div>
                <div class="text-gray-700 dark:text-gray-300 prose prose-sm dark:prose-invert max-w-none">
                    ${this.renderMarkdown(question.reason)}
                </div>
            </div>
        ` : '';

        const checkButton = isChecked
            ? '<button class="px-6 py-2 bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 rounded-lg cursor-not-allowed" disabled>Gecontroleerd ✓</button>'
            : '<button id="check-answer" class="px-6 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg shadow">Controleren</button>';

        const isLastQuestion = index === this.state.questions.length - 1;
        const nextButton = isLastQuestion
            ? '<button id="submit-quiz" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow">Afronden →</button>'
            : '<button id="next-question" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow">Volgende →</button>';

        const backButton = index > 0
            ? '<button id="prev-question" class="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold rounded-lg shadow hover:bg-gray-300 dark:hover:bg-gray-600">← Vorige</button>'
            : '';

        return `
            <div>
                <!-- Progress bar -->
                <div class="mb-6">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-sm text-gray-600 dark:text-gray-400">Voortgang</span>
                        <span class="text-sm font-semibold text-gray-900 dark:text-gray-100">
                            Vraag ${index + 1} / ${this.state.questions.length}
                        </span>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div class="progress-bar bg-blue-600 h-2 rounded-full"
                             style="width: ${progress}%"></div>
                    </div>
                </div>

                <!-- Question card -->
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
                    ${question.category ? `
                        <div class="inline-block px-3 py-1 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-sm font-semibold rounded mb-4">
                            ${this.escapeHtml(question.category)}
                        </div>
                    ` : ''}

                    <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
                        ${this.escapeHtml(question.text)}
                    </h2>

                    <div class="space-y-3 mb-6" id="answers-container">
                        ${answersHtml}
                    </div>

                    ${reasonHtml}
                </div>

                <!-- Navigation -->
                <div class="flex justify-between items-center mt-6">
                    <div>
                        ${backButton}
                    </div>
                    <div class="flex gap-3">
                        ${checkButton}
                        ${nextButton}
                    </div>
                </div>
            </div>
        `;
    }

    // Render statistics page - CONTINUING...
    renderStatistics() {
        const score = this.calculateScore();
        const timeElapsed = this.formatTime(this.getElapsedTime());

        let questionsList = '';
        this.state.questions.forEach((question, index) => {
            const isCorrect = this.isAnswerCorrect(index);
            const icon = isCorrect
                ? '<span class="text-green-600 text-xl">✓</span>'
                : '<span class="text-red-600 text-xl">✗</span>';

            const shortText = question.text.length > 60
                ? question.text.substring(0, 60) + '...'
                : question.text;

            questionsList += `
                <div class="flex items-center p-3 border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer"
                     data-review-index="${index}">
                    <span class="mr-3">${icon}</span>
                    <span class="flex-1 text-gray-700 dark:text-gray-300">
                        ${index + 1}. ${this.escapeHtml(shortText)}
                    </span>
                </div>
            `;
        });

        return `
            <div class="max-w-4xl mx-auto">
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
                    <div class="text-center mb-8">
                        <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                            Resultaten Analyse
                        </h1>
                        <p class="text-gray-600 dark:text-gray-400">
                            ${this.escapeHtml(this.quizData.title)}
                        </p>
                    </div>

                    <div class="grid md:grid-cols-2 gap-8 mb-8">
                        <!-- Score circle -->
                        <div class="flex flex-col items-center justify-center">
                            <div class="relative w-48 h-48">
                                <svg class="transform -rotate-90" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="45"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="10"
                                            class="text-gray-200 dark:text-gray-700" />
                                    <circle cx="50" cy="50" r="45"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="10"
                                            stroke-dasharray="${score.percentage * 2.827}, 282.7"
                                            class="${score.percentage >= 75 ? 'text-green-500' : score.percentage >= 50 ? 'text-yellow-500' : 'text-red-500'}"
                                            stroke-linecap="round" />
                                </svg>
                                <div class="absolute inset-0 flex items-center justify-center">
                                    <span class="text-4xl font-bold text-gray-900 dark:text-gray-100">
                                        ${score.percentage}%
                                    </span>
                                </div>
                            </div>
                            <p class="text-gray-600 dark:text-gray-400 mt-4">Eindscore</p>
                        </div>

                        <!-- Stats -->
                        <div class="flex flex-col justify-center space-y-4">
                            <div class="flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <span class="text-gray-600 dark:text-gray-400">Score:</span>
                                <span class="text-xl font-semibold text-gray-900 dark:text-gray-100">
                                    ${score.correct} / ${score.total}
                                </span>
                            </div>
                            <div class="flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <span class="text-gray-600 dark:text-gray-400">Tijd:</span>
                                <span class="text-xl font-semibold text-gray-900 dark:text-gray-100">
                                    ${timeElapsed}
                                </span>
                            </div>
                            <div class="flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <span class="text-gray-600 dark:text-gray-400">Status:</span>
                                <span class="text-xl font-semibold ${score.percentage >= 75 ? 'text-green-600' : score.percentage >= 50 ? 'text-yellow-600' : 'text-red-600'}">
                                    ${score.percentage >= 75 ? 'Geslaagd ✓' : score.percentage >= 50 ? 'Voldoende' : 'Onvoldoende'}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Questions review list -->
                    <div class="mt-8">
                        <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
                            Vraag overzicht
                        </h2>
                        <div class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden" id="questions-review">
                            ${questionsList}
                        </div>
                    </div>

                    <!-- Navigation -->
                    <div class="flex justify-between items-center mt-8">
                        <button id="back-to-last"
                                class="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold rounded-lg shadow hover:bg-gray-300 dark:hover:bg-gray-600">
                            ← Terug
                        </button>
                        <button id="restart-quiz"
                                class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow">
                            🔄 Opnieuw starten
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Render review page
    renderReview(index) {
        // Similar to renderQuestion but read-only
        const question = this.state.questions[index];
        const selectedIndices = this.state.answers[index] || [];
        const isCorrect = this.isAnswerCorrect(index);

        let answersHtml = '';
        question.answers.forEach((answer, answerIndex) => {
            const isSelected = selectedIndices.includes(answerIndex);
            const isAnswerCorrect = answer.correct;

            let borderClass = 'border-gray-200 dark:border-gray-700';
            let bgClass = 'bg-white dark:bg-gray-800';
            let icon = '';

            if (isAnswerCorrect) {
                borderClass = 'border-green-500';
                bgClass = 'bg-green-50 dark:bg-green-900/20';
                icon = '<span class="text-green-600 font-bold">✓</span>';
            } else if (isSelected) {
                borderClass = 'border-red-500';
                bgClass = 'bg-red-50 dark:bg-red-900/20';
                icon = '<span class="text-red-600 font-bold">✗</span>';
            }

            answersHtml += `
                <div class="border-2 ${borderClass} ${bgClass} rounded-lg p-4">
                    <div class="flex items-center">
                        <span class="flex-1 text-gray-900 dark:text-gray-100">
                            ${this.escapeHtml(answer.text)}
                        </span>
                        ${icon}
                    </div>
                </div>
            `;
        });

        return `
            <div>
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
                    <div class="flex items-center justify-between mb-6">
                        ${question.category ? `
                            <div class="inline-block px-3 py-1 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-sm font-semibold rounded">
                                ${this.escapeHtml(question.category)}
                            </div>
                        ` : '<div></div>'}

                        <span class="text-sm font-semibold ${isCorrect ? 'text-green-600' : 'text-red-600'}">
                            ${isCorrect ? 'Correct ✓' : 'Incorrect ✗'}
                        </span>
                    </div>

                    <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
                        ${this.escapeHtml(question.text)}
                    </h2>

                    <div class="space-y-3 mb-6">
                        ${answersHtml}
                    </div>

                    <div class="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 rounded">
                        <div class="flex items-center mb-2">
                            <span class="text-2xl mr-2">💡</span>
                            <span class="font-semibold text-blue-900 dark:text-blue-100">Uitleg</span>
                        </div>
                        <div class="text-gray-700 dark:text-gray-300 prose prose-sm dark:prose-invert max-w-none">
                            ${this.renderMarkdown(question.reason)}
                        </div>
                    </div>
                </div>

                <div class="mt-6">
                    <button id="back-to-statistics"
                            class="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold rounded-lg shadow hover:bg-gray-300 dark:hover:bg-gray-600">
                        ← Terug naar resultaten
                    </button>
                </div>
            </div>
        `;
    }

    // Attach event listeners after rendering
    attachEventListeners() {
        // Intro page
        const startButton = document.getElementById('start-quiz');
        if (startButton) {
            startButton.addEventListener('click', () => {
                // Save config
                this.state.config.shuffleQuestions = document.getElementById('shuffle-questions').checked;
                this.state.config.shuffleAnswers = document.getElementById('shuffle-answers').checked;
                this.state.config.autoAdvance = document.getElementById('auto-advance').checked;
                this.state.config.autoAdvanceDelay = parseInt(document.getElementById('auto-advance-delay').value);
                this.startQuiz();
            });
        }

        // Question page - answer selection
        const answersContainer = document.getElementById('answers-container');
        if (answersContainer) {
            const question = this.state.questions[this.state.currentQuestionIndex];
            const isMultiple = question.type === 'multiple';

            answersContainer.querySelectorAll('[data-answer-index]').forEach(div => {
                div.addEventListener('click', () => {
                    const answerIndex = parseInt(div.dataset.answerIndex);
                    this.selectAnswer(this.state.currentQuestionIndex, answerIndex, isMultiple);
                });
            });
        }

        // Check answer button
        const checkButton = document.getElementById('check-answer');
        if (checkButton) {
            checkButton.addEventListener('click', () => {
                this.checkAnswer(this.state.currentQuestionIndex);
            });
        }

        // Navigation buttons
        const nextButton = document.getElementById('next-question');
        if (nextButton) {
            nextButton.addEventListener('click', () => this.nextQuestion());
        }

        const prevButton = document.getElementById('prev-question');
        if (prevButton) {
            prevButton.addEventListener('click', () => this.previousQuestion());
        }

        const submitButton = document.getElementById('submit-quiz');
        if (submitButton) {
            submitButton.addEventListener('click', () => this.goToStatistics());
        }

        // Statistics page
        const restartButton = document.getElementById('restart-quiz');
        if (restartButton) {
            restartButton.addEventListener('click', () => {
                if (confirm('Weet je zeker dat je de quiz opnieuw wilt starten? Je huidige voortgang gaat verloren.')) {
                    this.restartQuiz();
                }
            });
        }

        const backToLastButton = document.getElementById('back-to-last');
        if (backToLastButton) {
            backToLastButton.addEventListener('click', () => {
                this.goToQuestion(this.state.questions.length - 1);
            });
        }

        // Review question clicks
        const reviewContainer = document.getElementById('questions-review');
        if (reviewContainer) {
            reviewContainer.querySelectorAll('[data-review-index]').forEach(div => {
                div.addEventListener('click', () => {
                    const index = parseInt(div.dataset.reviewIndex);
                    this.goToReview(index);
                });
            });
        }

        // Back to statistics from review
        const backToStatsButton = document.getElementById('back-to-statistics');
        if (backToStatsButton) {
            backToStatsButton.addEventListener('click', () => {
                this.goToStatistics();
            });
        }
    }

    // Utility: Escape HTML
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Utility: Render Markdown
    renderMarkdown(text) {
        if (typeof marked !== 'undefined') {
            return marked.parse(text);
        }
        // Fallback to escaped HTML if marked.js not loaded
        return this.escapeHtml(text);
    }
}

// Initialize the quiz application
const app = new QuizApp(QUIZ_DATA);
"""


def export_to_quiz_html(questions: list[Question], output_path: Path, title: str) -> int:
    """Export questions to interactive HTML quiz.

    Args:
        questions: List of Question objects to export
        output_path: Path where HTML file will be written
        title: Quiz title displayed on intro page

    Returns:
        File size in bytes

    Raises:
        OSError: If writing to file fails
    """
    generator = QuizHTMLGenerator(questions, title)
    return generator.generate(output_path)
