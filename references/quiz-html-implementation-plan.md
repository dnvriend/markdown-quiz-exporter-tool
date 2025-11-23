# Quiz HTML Implementation Plan

Step-by-step implementation plan for the quiz-html command.

## Implementation Phases

### Phase 1: Core Infrastructure ✓ (Reuse Existing)

**Components Already Available**:
- Quiz markdown parser (`quiz_parser.py`)
- Question and Answer data models
- CLI framework setup (Click)
- Logging infrastructure
- Test framework

**No changes needed**: We can reuse the existing parser completely.

### Phase 2: HTML Template Generator (New Module)

**File**: `markdown_quiz_exporter/quiz_html.py`

**Purpose**: Generate complete HTML file with embedded quiz data

**Class Structure**:

```python
class QuizHTMLGenerator:
    """Generator for interactive HTML quiz pages."""

    def __init__(self, questions: list[Question], title: str):
        self.questions = questions
        self.title = title

    def generate(self, output_path: Path) -> None:
        """Generate complete HTML file."""
        html_content = self._build_html()
        output_path.write_text(html_content, encoding='utf-8')

    def _build_html(self) -> str:
        """Build complete HTML document."""
        return f"""<!DOCTYPE html>
<html lang="nl">
{self._build_head()}
{self._build_body()}
</html>"""

    def _build_head(self) -> str:
        """Build HTML head section."""
        return f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    {self._build_styles()}
</head>"""

    def _build_styles(self) -> str:
        """Build embedded CSS styles."""
        return """<style>
        /* Dark mode and custom styles */
    </style>"""

    def _build_body(self) -> str:
        """Build HTML body section."""
        return f"""<body class="bg-gray-50 dark:bg-gray-900">
    <div id="app"></div>
    <script>
        const QUIZ_DATA = {self._build_quiz_data()};
        {self._build_javascript()}
    </script>
</body>"""

    def _build_quiz_data(self) -> str:
        """Convert questions to JSON."""
        quiz_data = {
            'title': self.title,
            'questions': [self._question_to_dict(q) for q in self.questions]
        }
        return json.dumps(quiz_data, ensure_ascii=False)

    def _question_to_dict(self, question: Question) -> dict:
        """Convert Question object to dictionary."""
        return {
            'category': self._extract_category(question.text),
            'text': self._clean_question_text(question.text),
            'type': question.question_type,
            'answers': [
                {'text': ans.text, 'correct': ans.is_correct}
                for ans in question.answers
            ],
            'reason': question.reason
        }

    def _build_javascript(self) -> str:
        """Build embedded JavaScript application."""
        # Return complete quiz application JavaScript
        pass
```

**Key Methods**:

1. `_build_head()`: Generates HTML head with Tailwind CDN
2. `_build_styles()`: Custom CSS for dark mode and components
3. `_build_quiz_data()`: Converts Question objects to JSON
4. `_build_javascript()`: Embeds complete quiz application

### Phase 3: JavaScript Quiz Application (Embedded in HTML)

**Structure**: Single JavaScript class embedded in HTML template

**File Organization**:
- Create separate `.js` template file for development
- Minify and embed into HTML during generation
- OR: Keep as template string in Python for simplicity

**Option A: Template String (Recommended)**

```python
# In quiz_html.py
QUIZ_APP_JS = """
class QuizApp {
    constructor(quizData) {
        this.quizData = quizData;
        this.state = this.loadState() || this.initializeState();
        this.init();
    }

    // ... complete implementation
}

// Initialize app
const app = new QuizApp(QUIZ_DATA);
"""
```

**Option B: Separate Template File**

```python
# Load from file
def _load_js_template(self) -> str:
    template_path = Path(__file__).parent / 'templates' / 'quiz-app.js'
    return template_path.read_text()
```

**Recommendation**: Use Option A (template string) for simplicity and single-file deployment.

### Phase 4: CLI Command Implementation

**File**: `markdown_quiz_exporter/cli.py` (add new command)

**Command Structure**:

```python
@click.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "--title",
    required=True,
    help="Quiz title displayed on intro page",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Overwrite output file if exists",
)
def quiz_html(
    input_file: Path,
    output_file: Path,
    title: str,
    verbose: int,
    force: bool,
) -> None:
    """Generate interactive HTML quiz from markdown.

    Creates a single-page application with embedded quiz data,
    requiring no external dependencies after generation.

    \b
    Arguments:
        INPUT_FILE   Path to quiz markdown file (*.md)
        OUTPUT_FILE  Path where HTML file will be written (*.html)

    \b
    Examples:

        \b
        # Generate quiz HTML
        markdown-quiz-exporter quiz-html quiz.md quiz.html --title "My Quiz"

        \b
        # Overwrite existing file
        markdown-quiz-exporter quiz-html quiz.md quiz.html --title "Quiz" --force

        \b
        # With verbose output
        markdown-quiz-exporter quiz-html quiz.md quiz.html --title "Quiz" -vv
    """
    setup_logging(verbose)

    logger.info("Starting HTML quiz generation")
    logger.debug("Input: %s, Output: %s, Title: %s", input_file, output_file, title)

    # Check output file
    if output_file.exists() and not force:
        click.echo(
            f"Error: Output file '{output_file}' already exists. Use --force.",
            err=True,
        )
        raise click.Abort()

    # Parse quiz
    try:
        questions = parse_quiz_file(input_file)
        logger.info("Parsed %d questions", len(questions))
    except Exception as e:
        click.echo(f"Error parsing quiz: {e}", err=True)
        raise click.Abort()

    # Generate HTML
    try:
        generator = QuizHTMLGenerator(questions, title)
        generator.generate(output_file)
        logger.info("Generated HTML quiz: %s", output_file)

        file_size = output_file.stat().st_size / 1024
        click.echo(f"✓ Generated {output_file} ({file_size:.1f} KB)")
    except Exception as e:
        click.echo(f"Error generating HTML: {e}", err=True)
        raise click.Abort()
```

### Phase 5: Testing Strategy

**Test Files**:

1. `tests/test_quiz_html.py` - Unit tests for HTML generator
2. Manual testing with browser

**Unit Tests**:

```python
def test_quiz_html_generation(tmp_path):
    """Test basic HTML generation."""
    questions = [create_sample_question()]
    generator = QuizHTMLGenerator(questions, "Test Quiz")

    output = tmp_path / "test.html"
    generator.generate(output)

    assert output.exists()
    content = output.read_text()

    # Verify HTML structure
    assert "<!DOCTYPE html>" in content
    assert "<title>Test Quiz</title>" in content
    assert "tailwindcss.com" in content
    assert "QUIZ_DATA" in content
    assert "class QuizApp" in content

def test_quiz_data_json(tmp_path):
    """Test quiz data JSON generation."""
    questions = [
        create_single_choice_question(),
        create_multiple_choice_question(),
    ]
    generator = QuizHTMLGenerator(questions, "Test")

    quiz_data = generator._build_quiz_data()
    data = json.loads(quiz_data)

    assert data['title'] == "Test"
    assert len(data['questions']) == 2
    assert data['questions'][0]['type'] == 'single'
    assert data['questions'][1]['type'] == 'multiple'

def test_dark_mode_included(tmp_path):
    """Test that dark mode classes are included."""
    generator = QuizHTMLGenerator([], "Test")
    html = generator._build_html()

    assert "dark:bg-gray-900" in html
    assert "dark:bg-gray-800" in html

def test_responsive_classes(tmp_path):
    """Test responsive Tailwind classes."""
    generator = QuizHTMLGenerator([], "Test")
    html = generator._build_html()

    # Check for responsive breakpoints
    assert "md:" in html or "lg:" in html or "sm:" in html
```

**Manual Testing Checklist**:

- [ ] Quiz loads in Chrome/Firefox/Safari/Edge
- [ ] Intro page displays correctly
- [ ] All config options work
- [ ] Dark/light mode toggle works
- [ ] Questions display correctly (single/multiple choice)
- [ ] Answer selection works
- [ ] Check button validates and shows feedback
- [ ] Navigation works (back/next/submit)
- [ ] Statistics page shows correct score
- [ ] Timer displays correctly
- [ ] Review mode works
- [ ] Restart works
- [ ] Session storage persists state
- [ ] Refresh page maintains state
- [ ] Mobile responsive on small screens

## Implementation Order

### Step 1: Create HTML Generator Module (Day 1)

```bash
# Create new module
touch markdown_quiz_exporter/quiz_html.py

# Implement:
- QuizHTMLGenerator class
- _build_html() with basic structure
- _build_quiz_data() JSON conversion
- Basic _build_javascript() placeholder
```

### Step 2: Develop JavaScript Application (Day 2-3)

**Approach**: Develop separately first, then embed

```bash
# Create development file
mkdir -p markdown_quiz_exporter/templates
touch markdown_quiz_exporter/templates/quiz-app.js

# Develop interactively:
1. Create standalone HTML file for testing
2. Develop QuizApp class with hot reload
3. Test all features in browser
4. Once stable, copy to Python template string
```

**JavaScript Development Phases**:

1. **Phase A**: State management and storage
   - `initializeState()`
   - `saveState()` / `loadState()`
   - `clearState()`

2. **Phase B**: Rendering system
   - `render()` master renderer
   - `renderIntro()`
   - `renderQuestion()`
   - `renderStatistics()`
   - `renderReview()`

3. **Phase C**: Navigation
   - `goToIntro()`
   - `goToQuestion()`
   - `nextQuestion()` / `previousQuestion()`
   - `goToStatistics()`

4. **Phase D**: Quiz logic
   - `selectAnswer()`
   - `checkAnswer()`
   - `submitQuiz()`
   - `calculateScore()`

5. **Phase E**: Utilities
   - `shuffleArray()`
   - `formatTime()`
   - `toggleDarkMode()`

### Step 3: Integrate and Test (Day 4)

```bash
# Add CLI command
# Test end-to-end flow
# Fix bugs
# Optimize
```

### Step 4: Documentation and Polish (Day 4-5)

```bash
# Update README
# Add examples
# Create demo quiz
# Final testing
```

## Development Tools & Workflow

### Live Development Setup

For JavaScript development, create a development HTML file:

```html
<!-- dev-quiz.html -->
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Dev</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 dark:bg-gray-900">
    <div id="app"></div>

    <script>
        // Sample quiz data for development
        const QUIZ_DATA = {
            title: "Sample Quiz",
            questions: [
                {
                    category: "TEST",
                    text: "Sample question?",
                    type: "single",
                    answers: [
                        {text: "Option 1", correct: false},
                        {text: "Option 2", correct: true},
                        {text: "Option 3", correct: false}
                    ],
                    reason: "This is the explanation."
                }
            ]
        };
    </script>

    <!-- Load quiz app from separate file during dev -->
    <script src="quiz-app.js"></script>
</body>
</html>
```

**Benefits**:
- Live reload with browser DevTools
- Console debugging
- Inspect element styling
- Faster iteration

### Python to JavaScript Integration

Once JavaScript is stable:

```python
# In quiz_html.py

# Option 1: Inline template string
QUIZ_APP_TEMPLATE = """
class QuizApp {
    // ... complete implementation
}
const app = new QuizApp(QUIZ_DATA);
"""

# Option 2: Load from file (better for large JS)
def _load_quiz_app_js(self) -> str:
    js_path = Path(__file__).parent / 'templates' / 'quiz-app.js'
    return js_path.read_text()
```

## File Size Optimization

Target: Keep HTML file under 500KB

**Strategies**:

1. **Minify JSON**:
   ```python
   json.dumps(quiz_data, ensure_ascii=False, separators=(',', ':'))
   ```

2. **Compress JavaScript** (optional):
   ```python
   import jsmin  # or use rjsmin
   minified = jsmin.jsmin(js_code)
   ```

3. **Remove comments and whitespace**:
   - Keep during development
   - Strip before embedding

4. **Lazy load Tailwind** (already from CDN):
   - CDN handles caching
   - No local bloat

## Error Handling Strategy

### Python Side (Generation)

- Validate input file exists
- Validate markdown parses correctly
- Check minimum requirements (1 question, etc.)
- Handle file write permissions
- Catch and display user-friendly errors

### JavaScript Side (Runtime)

- Check sessionStorage availability
- Validate quiz data structure
- Handle missing/corrupted state
- Graceful fallbacks for browser features

## Security Considerations

- **XSS Prevention**: Escape user content in HTML
  ```python
  import html
  escaped = html.escape(question.text)
  ```

- **No external dependencies**: All code is embedded
- **No server communication**: Pure client-side
- **SessionStorage only**: No localStorage persistence

## Performance Targets

- **HTML Generation**: < 1 second for 100 questions
- **Page Load**: < 500ms on modern browser
- **Page Transitions**: Instant (state-based, no reload)
- **File Size**: < 500KB for typical quiz (40 questions)

## Browser Compatibility Matrix

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Edge | 90+ | ✅ Full |
| Mobile Safari | 14+ | ✅ Full |
| Chrome Mobile | 90+ | ✅ Full |

**Required Features**:
- ES6+ (classes, arrow functions, template literals)
- SessionStorage API
- CSS Grid/Flexbox
- Dark mode media query support

## Deliverables Checklist

- [ ] `quiz_html.py` module
- [ ] `quiz-app.js` template (embedded or separate)
- [ ] CLI command `quiz-html`
- [ ] Unit tests
- [ ] Manual test checklist
- [ ] Example quiz HTML output
- [ ] Documentation in README
- [ ] Reference specs (already created)

## Timeline Estimate

- **Day 1**: Python HTML generator (~4 hours)
- **Day 2-3**: JavaScript quiz app (~12 hours)
- **Day 4**: Integration & testing (~6 hours)
- **Day 5**: Polish & documentation (~2 hours)

**Total**: ~24 hours

## Next Steps

1. ✅ Specification complete
2. ✅ Implementation plan complete
3. Create HTML generator module
4. Develop JavaScript application
5. Integrate and test
6. Document and deliver
