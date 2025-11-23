# Quiz HTML Generator Specification

Complete technical specification for generating interactive HTML quiz pages from quiz markdown files.

## Overview

The `quiz-html` command generates a single, self-contained HTML file that runs an interactive quiz application. The HTML file includes all necessary CSS (Tailwind CDN), JavaScript, and quiz data embedded within it, requiring no external dependencies after generation.

## Command Syntax

```bash
markdown-quiz-exporter quiz-html <input.md> <output.html> --title "Quiz Title"
```

### Arguments

- `input.md` (required): Path to quiz markdown file
- `output.html` (required): Path where HTML file will be written
- `--title` (required): Quiz title displayed on intro page

### Options

- `-v, --verbose`: Enable verbose output
- `-f, --force`: Overwrite output file if exists

## Page Structure & State Flow

The quiz application consists of multiple pages managed by JavaScript state:

### 1. Intro/Configuration Page (State: 'intro')

**Purpose**: Welcome screen and quiz configuration

**Elements**:
- Quiz title (large heading)
- Question count: "This quiz has X questions"
- Configuration options (checkboxes):
  - [ ] Shuffle questions order
  - [ ] Shuffle answer options
  - [ ] Auto-advance after checking (with seconds input)
- Dark/light mode toggle (sun/moon icon)
- Start Quiz button

**Navigation**: No back button, only forward to first question

**State Stored**:
```javascript
{
  shuffleQuestions: boolean,
  shuffleAnswers: boolean,
  autoAdvance: boolean,
  autoAdvanceDelay: number (seconds),
  darkMode: boolean
}
```

### 2. Question Pages (State: 'question-N')

**Purpose**: Display and answer quiz questions

**Layout**:
```
┌─────────────────────────────────────────────────────┐
│ Progress Bar: ████████░░░░░░░░░░     Question 6/40 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  CATEGORY TAG                                       │
│                                                     │
│  Question text here?                                │
│                                                     │
│  [ ] Answer option 1                                │
│  [ ] Answer option 2                                │
│  [ ] Answer option 3                                │
│  [ ] Answer option 4                                │
│                                                     │
│  [After check: reason section here]                 │
│                                                     │
├─────────────────────────────────────────────────────┤
│           [< Back]  [✓ Check]  [Next >]             │
└─────────────────────────────────────────────────────┘
```

**States per Question**:
- `unanswered`: No selection made
- `answered`: Selection made, not checked yet
- `checked`: Answer checked, feedback shown

**Navigation**:
- **First question (0)**: No Back button, Check + Next
- **Middle questions (1 to n-1)**: Back + Check + Next
- **Last question (n)**: Back + Check + Submit

**Behavior**:
- Radio buttons for single choice `( )`
- Checkboxes for multiple choice `[ ]`
- Check button:
  - Validates selection is made
  - Shows green border for correct answers
  - Shows red border for incorrect answers
  - Displays reason section below options
  - Disables answer selection (lock answers)
  - Changes Check button to "Checked ✓" (disabled)
- Next/Submit button:
  - Only enabled after checking
  - Saves answer and proceeds

**Reason Display**:
```html
<div class="reason-section">
  <div class="reason-icon">💡 Uitleg</div>
  <p>Explanation text here...</p>
</div>
```

### 3. Statistics/Results Page (State: 'statistics')

**Purpose**: Show quiz results and review

**Layout**:
```
┌─────────────────────────────────────────────────────┐
│              Resultaten Analyse                      │
│           Quiz Title                                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│   ┌─────────┐        Score: 32/40 (80%)            │
│   │         │        Time: 15:23                    │
│   │   80%   │        Status: Passed ✓               │
│   │         │                                       │
│   └─────────┘                                       │
│                                                     │
│  Question Review:                                   │
│  ✓ 1. Bij welke stakeholders...                    │
│  ✗ 2. Wat is geen P volgens...                     │
│  ✓ 3. Welke van de onderstaande...                 │
│  ...                                                │
│                                                     │
├─────────────────────────────────────────────────────┤
│           [< Back]  [🔄 Restart]                    │
└─────────────────────────────────────────────────────┘
```

**Elements**:
- Score percentage display (circular or numeric)
- Time taken (MM:SS format)
- Per-question review list:
  - Green checkmark (✓) for correct
  - Red X (✗) for incorrect
  - Clickable to review question
- Navigation: Back to last question, Restart quiz

**Review Mode** (clicking a question):
- Navigate to question in read-only mode
- Show user's answer marked
- Show correct/incorrect indicators
- Show reason section
- Special back button: "Back to Results"

### 4. Review Question Page (State: 'review-N')

**Purpose**: Read-only view of answered question from statistics

**Display**:
- Same layout as question page
- User's selected answer(s) marked
- Correct answers highlighted in green
- Incorrect selections highlighted in red
- Reason section always visible
- Navigation: "Back to Statistics" button only

## Technical Architecture

### Technology Stack

| Component | Technology | Source |
|-----------|-----------|---------|
| **CSS Framework** | Tailwind CSS 3.x | CDN (unpkg/jsdelivr) |
| **JavaScript** | Vanilla ES6+ | Embedded |
| **Icons** | Heroicons or Unicode | Inline SVG or emoji |
| **State Management** | SessionStorage API | Browser native |
| **Timer** | setInterval | Browser native |

### HTML Structure

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{QUIZ_TITLE}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Dark mode configuration */
        /* Custom styles */
    </style>
</head>
<body class="bg-gray-50 dark:bg-gray-900">
    <div id="app" class="min-h-screen">
        <!-- Vue-like reactive content rendered by JavaScript -->
    </div>

    <script>
        // Quiz data embedded as JSON
        const QUIZ_DATA = {{JSON_DATA}};

        // Quiz application logic
        class QuizApp { ... }

        // Initialize
        const app = new QuizApp();
    </script>
</body>
</html>
```

### JavaScript Quiz Application

**Class Structure**:

```javascript
class QuizApp {
  constructor(quizData) {
    this.quizData = quizData;
    this.state = this.loadState() || this.initializeState();
    this.startTime = Date.now();
    this.render();
  }

  initializeState() {
    return {
      currentPage: 'intro',
      config: {
        shuffleQuestions: false,
        shuffleAnswers: false,
        autoAdvance: false,
        autoAdvanceDelay: 3,
        darkMode: this.detectDarkMode()
      },
      questions: this.prepareQuestions(),
      answers: {}, // questionIndex: [selectedAnswerIndices]
      checked: {}, // questionIndex: boolean
      startTime: null,
      endTime: null
    };
  }

  // State management
  saveState() { ... }
  loadState() { ... }
  clearState() { ... }

  // Rendering
  render() { ... }
  renderIntro() { ... }
  renderQuestion(index) { ... }
  renderStatistics() { ... }
  renderReview(index) { ... }

  // Navigation
  goToIntro() { ... }
  goToQuestion(index) { ... }
  goToStatistics() { ... }
  goToReview(index) { ... }
  nextQuestion() { ... }
  previousQuestion() { ... }

  // Quiz logic
  selectAnswer(questionIndex, answerIndex) { ... }
  checkAnswer(questionIndex) { ... }
  submitQuiz() { ... }
  restartQuiz() { ... }

  // Utilities
  shuffleArray(array) { ... }
  calculateScore() { ... }
  formatTime(milliseconds) { ... }
}
```

### Data Structure

**Quiz Data JSON**:

```json
{
  "title": "MB2422 - Management & Organisatie",
  "questions": [
    {
      "category": "STAKEHOLDERS",
      "text": "Bij welke stakeholders ligt het belang...",
      "type": "single",
      "answers": [
        {"text": "aandeelhouders", "correct": false},
        {"text": "overheden", "correct": true},
        {"text": "banken en investeerders", "correct": false},
        {"text": "medewerkers", "correct": false}
      ],
      "reason": "Volgens hoofdstuk 2.5.9: **Aandeelhouders** zijn de eigenaars..."
    }
  ]
}
```

**Session Storage State**:

```json
{
  "currentPage": "question-5",
  "config": {
    "shuffleQuestions": false,
    "shuffleAnswers": true,
    "autoAdvance": false,
    "darkMode": true
  },
  "questions": [...],
  "answers": {
    "0": [1],
    "1": [0, 2],
    "2": [3]
  },
  "checked": {
    "0": true,
    "1": true,
    "2": false
  },
  "startTime": 1699999999999,
  "endTime": null
}
```

## Styling & Theme

### Color Palette

**Light Mode**:
- Primary: Blue-600 (#2563eb)
- Background: Gray-50 (#f9fafb)
- Card: White (#ffffff)
- Text: Gray-900 (#111827)
- Border: Gray-200 (#e5e7eb)
- Success: Green-500 (#10b981)
- Error: Red-500 (#ef4444)

**Dark Mode**:
- Primary: Blue-500 (#3b82f6)
- Background: Gray-900 (#111827)
- Card: Gray-800 (#1f2937)
- Text: Gray-100 (#f3f4f6)
- Border: Gray-700 (#374151)
- Success: Green-400 (#4ade80)
- Error: Red-400 (#f87171)

### Responsive Breakpoints

```css
/* Mobile-first approach */
- sm: 640px   /* Small tablets */
- md: 768px   /* Tablets */
- lg: 1024px  /* Small desktops */
- xl: 1280px  /* Large desktops */
```

### Component Styling

**Progress Bar**:
```html
<div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
  <div class="bg-blue-600 h-2 rounded-full transition-all duration-300"
       style="width: {{percentage}}%"></div>
</div>
```

**Answer Option (Unchecked)**:
```html
<div class="border-2 border-gray-200 dark:border-gray-700
            rounded-lg p-4 cursor-pointer
            hover:border-blue-400 transition-colors">
  <input type="radio" ... />
  <label>Answer text</label>
</div>
```

**Answer Option (Correct - After Check)**:
```html
<div class="border-2 border-green-500 bg-green-50 dark:bg-green-900/20
            rounded-lg p-4">
  <span class="text-green-600">✓</span>
  <label>Answer text</label>
</div>
```

**Answer Option (Incorrect - After Check)**:
```html
<div class="border-2 border-red-500 bg-red-50 dark:bg-red-900/20
            rounded-lg p-4">
  <span class="text-red-600">✗</span>
  <label>Answer text</label>
</div>
```

### Dark Mode Implementation

**Strategy**: Tailwind's `dark:` variant with manual toggle

```javascript
// Detect system preference
function detectDarkMode() {
  if (window.matchMedia) {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  return false;
}

// Toggle dark mode
function toggleDarkMode() {
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

// Apply on load
if (this.state.config.darkMode) {
  document.documentElement.classList.add('dark');
}
```

**Toggle Button**:
```html
<!-- Sun icon for light mode, moon icon for dark mode -->
<button onclick="app.toggleDarkMode()"
        class="fixed top-4 right-4 p-2 rounded-lg
               bg-gray-200 dark:bg-gray-700">
  <svg class="w-6 h-6 hidden dark:block"><!-- moon --></svg>
  <svg class="w-6 h-6 block dark:hidden"><!-- sun --></svg>
</button>
```

## Features Implementation

### 1. Question Shuffling

```javascript
prepareQuestions() {
  let questions = [...this.quizData.questions];

  if (this.state.config.shuffleQuestions) {
    questions = this.shuffleArray(questions);
  }

  if (this.state.config.shuffleAnswers) {
    questions = questions.map(q => ({
      ...q,
      answers: this.shuffleArray([...q.answers])
    }));
  }

  return questions;
}
```

### 2. Timer Implementation

```javascript
startTimer() {
  this.state.startTime = Date.now();
  this.saveState();
}

stopTimer() {
  this.state.endTime = Date.now();
  this.saveState();
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
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}
```

### 3. Answer Validation

```javascript
checkAnswer(questionIndex) {
  const question = this.state.questions[questionIndex];
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

  // Check if arrays are equal (order doesn't matter)
  if (selectedIndices.length !== correctIndices.length) {
    return false;
  }

  return selectedIndices.every(i => correctIndices.includes(i));
}
```

### 4. Score Calculation

```javascript
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
    percentage: Math.round((correct / total) * 100)
  };
}
```

### 5. Session Storage Persistence

```javascript
saveState() {
  sessionStorage.setItem('quizState', JSON.stringify(this.state));
}

loadState() {
  const saved = sessionStorage.getItem('quizState');
  return saved ? JSON.parse(saved) : null;
}

clearState() {
  sessionStorage.removeItem('quizState');
}
```

## Accessibility Considerations

While keyboard navigation was explicitly excluded, the following accessibility features should be implemented:

- Semantic HTML elements (`<button>`, `<input type="radio">`, etc.)
- Proper `aria-label` attributes for icon buttons
- Color contrast meeting WCAG AA standards
- Focus visible indicators for interactive elements
- Screen reader friendly text labels

## Edge Cases & Error Handling

### Empty or Invalid Quiz

- Minimum 1 question required
- Each question must have at least 2 answers
- Each question must have at least 1 correct answer
- Show user-friendly error message if validation fails

### Browser Compatibility

- Target: Modern browsers (Chrome/Edge/Firefox/Safari last 2 versions)
- SessionStorage support required
- ES6+ JavaScript features used
- Tailwind CSS compatibility

### Performance

- Single HTML file size target: < 500KB
- Quiz data embedded as minified JSON
- No external API calls
- Instant page transitions (state-based rendering)

## Testing Strategy

1. **Unit Tests**: Quiz logic functions (scoring, validation, etc.)
2. **Integration Tests**: Full quiz flow simulation
3. **Manual Tests**:
   - Different screen sizes (mobile, tablet, desktop)
   - Dark/light mode switching
   - Session storage persistence
   - All navigation paths

## Future Enhancements (Not in Scope)

- Export results to PDF/CSV
- Multiple quiz attempts tracking
- Share results functionality
- Detailed analytics per category
- Keyboard shortcuts
- Print-friendly version
- Offline PWA support
- Multi-language support
