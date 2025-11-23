# Anki CSV Format Specification

Technical specification for exporting flashcards to Anki CSV format.

## Overview

Anki supports importing CSV files with specific formats. This specification covers two note types:
1. **AllInOne** - For quiz-style cards with multiple choice questions
2. **Basic** - For simple question/answer recall cards

## File Format

### Structure

```
#separator:Semicolon
#html:false
#notetype:<note type>
#tags:<tags>
Field1;Field2;Field3;...
```

### Requirements

- **Encoding**: UTF-8
- **Line Ending**: Unix-style (`\n`) or Windows-style (`\r\n`)
- **Separator**: Semicolon (`;`)
- **Extension**: `.csv`

## AllInOne Note Type (Quiz Format)

### Purpose

For quiz-style learning with multiple choice questions. Supports:
- Single choice (radio buttons)
- Multiple choice (checkboxes)
- KPRIM format (not used in this implementation)

### Field Structure

```
Question;Title;QType;Q_1;Q_2;Q_3;Q_4;Q_5;Answers;Sources;Extra1;Tags
```

**Fields:**
1. **Question**: The question text
2. **Title**: Optional title (usually empty)
3. **QType**: Question type indicator
   - `0` = KPRIM (all answers must be evaluated)
   - `1` = Multiple choice (one or more correct)
   - `2` = Single choice (exactly one correct)
4. **Q_1 through Q_5**: Answer options (up to 5)
5. **Answers**: Binary string indicating correct answers
   - Format: `1 0 0 0 0` (spaces between digits)
   - `1` = correct, `0` = incorrect
   - Position corresponds to Q_1 through Q_5
6. **Sources**: Optional source reference (usually empty)
7. **Extra1**: Explanation/reasoning text
8. **Tags**: Space-separated tags

### Example

**Headers:**
```
#separator:Semicolon
#html:false
#notetype:AllInOne (kprim, mc, sc)
#tags:quiz generated
```

**Single Choice Question:**
```
What is the max size of an S3 object in GB?;;2;1000;5000;10000;Unlimited;;1 0 0 0 0;;The maximum size for a single S3 object is 5TB or 5000GB.;quiz
```

**Multiple Choice Question:**
```
What are characteristics of effective leadership?;;1;Ability to motivate;Clear communication;Authoritarian approach;Short-term focus;;1 1 0 0 0;;Leadership requires motivation and clear communication.;quiz
```

### QType Selection Logic

- **Single choice (QType = 2)**:
  - Question uses radio button format `(X)` / `( )`
  - OR exactly one correct answer

- **Multiple choice (QType = 1)**:
  - Question uses checkbox format `[X]` / `[ ]`
  - AND multiple correct answers

## Basic Note Type (Recall Format)

### Purpose

For simple question/answer flashcards focused on recall rather than multiple choice.

### Field Structure

```
Front;Back;Tags
```

**Fields:**
1. **Front**: Question text
2. **Back**: Answer text with explanation
3. **Tags**: Space-separated tags

### Example

**Headers:**
```
#separator:Semicolon
#html:false
#notetype:Basic
#tags:quiz recall
```

**Single Answer:**
```
What is the max size of an S3 object in GB?;Answer: 5000\n\nExplanation: The maximum size for a single S3 object is 5TB or 5000GB.;recall
```

**Multiple Answers:**
```
What are characteristics of effective leadership?;Answers: Ability to motivate, Clear communication\n\nExplanation: Leadership requires motivation and clear communication.;recall
```

## Conversion Strategy

### From Quiz Markdown to Anki CSV

#### AllInOne Format (Quiz)

1. **Parse question type**:
   - Detect radio `( )` vs checkbox `[ ]` format
   - Count correct answers
   - Determine QType (1 or 2)

2. **Extract up to 5 answer options**:
   - Store in Q_1 through Q_5
   - If less than 5, leave remaining fields empty

3. **Generate Answers field**:
   - Create binary string with 5 positions
   - Mark correct answers with `1`, incorrect with `0`

4. **Include explanation**:
   - Place reason section in Extra1 field

#### Basic Format (Recall)

1. **Front**: Use question text as-is

2. **Back**: Format answer with explanation:
   ```
   Answer: <correct answer>

   Explanation: <reason>
   ```

   For multiple correct answers:
   ```
   Answers: <answer1>, <answer2>, ...

   Explanation: <reason>
   ```

## Edge Cases and Handling

### More Than 5 Answer Options

If a question has more than 5 options, only the first 5 are included in AllInOne format. Consider:
- Warning the user
- Using Basic format instead
- Splitting into multiple questions

### No Correct Answer

- Should not occur with valid quiz markdown
- Parser should raise error during validation

### Missing Reason Section

- AllInOne: Leave Extra1 field empty
- Basic: Omit "Explanation:" line from back

### Special Characters

**Semicolons in content:**
- CSV field quoting handles this automatically
- No special escaping needed if using Python csv module

**Newlines in content:**
- Use `\n` literal in Basic format
- Keep single line for AllInOne format (join multi-line text)

**HTML entities:**
- Set `#html:false` in headers
- No need to escape HTML entities

## Validation Rules

A valid Anki CSV export must:
1. Have correct headers for the note type
2. Have correct number of fields per row
3. Be UTF-8 encoded
4. Have at least one flashcard
5. QType must match the actual question structure
6. Answers field must have exactly 5 positions for AllInOne

## Testing

To verify the CSV output:
1. Open in spreadsheet application (semicolon-delimited)
2. Check headers are correct
3. Import into Anki
4. Test flashcards display correctly:
   - Question text readable
   - Answer options visible
   - Correct answers marked properly
   - Explanation displays

## Implementation Notes

When implementing the converter:

1. **Parse quiz markdown** → extract questions, answers, and reasons
2. **Determine format** → based on user choice (--quiz or --recall)
3. **Generate CSV** → using Python csv module with semicolon delimiter
4. **Write headers** → appropriate for note type
5. **Format rows** → according to note type specification
6. **Validate** → ensure all fields present and properly formatted

## Usage Recommendations

**Use AllInOne (Quiz) format when:**
- Learning requires testing multiple choice knowledge
- Want to practice identifying correct answers
- Need to evaluate similar-looking options
- Studying for multiple choice exams

**Use Basic (Recall) format when:**
- Focus on direct recall
- Want simpler flashcard interaction
- Content is more definitional
- Don't need multiple choice practice

Can generate both formats from the same quiz markdown file for comprehensive study.
