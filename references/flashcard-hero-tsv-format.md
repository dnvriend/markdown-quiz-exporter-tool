# Flashcard Hero TSV Format Specification

Technical specification for exporting flashcards to Flashcard Hero TSV format.

## Overview

Flashcard Hero accepts tab-separated values (TSV) files for bulk importing flashcards. Each line represents one flashcard with the front side (question) and back side (answer) separated by a tab character.

## File Format

### Structure

```
Front text<TAB>Back text
Front text<TAB>Back text
...
```

### Requirements

- **Encoding**: UTF-8
- **Line Ending**: Unix-style (`\n`) or Windows-style (`\r\n`)
- **Separator**: Single tab character (`\t`)
- **Extension**: `.tsv` or `.txt`

### Field Specifications

#### Front Field (Question/Prompt)

The front field contains the question or prompt that will be shown to the user.

**Format Guidelines:**
- Can contain any text
- Newlines should be preserved if supported (test with target app)
- Special characters should be escaped if necessary
- Typically shorter than the back field
- Should be clear and unambiguous

**Examples:**
```
S3: What is the max size of an S3 object in GB?
IAM: Max number of users per account
What is the definition of 'management' according to the chapter?
```

#### Back Field (Answer)

The back field contains the answer or information revealed when the card is flipped.

**Format Guidelines:**
- Can contain the answer text
- For multiple choice questions, include all options with indicators
- Should be concise but complete
- Can include additional context if needed

**Examples for Single Answer:**
```
5000
100
Het optimaal laten samenwerken van mensen en middelen om een bepaald doel te bereiken
```

**Examples for Multiple Choice (with indicator):**
```
- Single global database (wrong)
- Multi-region setup with data residency ✓
- Separate databases (wrong)
- Cloud-only solution (wrong)
```

## Conversion Strategy

### From Quiz Markdown to Flashcard Hero TSV

When converting quiz markdown to Flashcard Hero format:

1. **Question Text → Front Field**
   - Use the complete question text as-is
   - Preserve multi-line questions (if supported)
   - Strip markdown formatting or keep minimal formatting

2. **Answer Options → Back Field**
   - **Option A (Simple)**: Only include correct answer(s)
   - **Option B (Full Context)**: Include all options with indicator for correct answer
   - **Option C (Extended)**: Include correct answer + reason section

#### Conversion Option A: Correct Answer Only

**Input:**
```markdown
S3: What is the max size of an S3 object in GB?

- ( ) 1000
- (X) 5000
- ( ) 10000
- ( ) Unlimited

# reason
The maximum size for a single S3 object is 5TB or 5000GB.
```

**Output:**
```tsv
S3: What is the max size of an S3 object in GB?	5000
```

**Pros:**
- Clean and simple
- Focuses on memorization
- Smaller file size

**Cons:**
- Loses context of wrong answers
- User doesn't see other options

#### Conversion Option B: All Options with Indicator

**Input:**
```markdown
What is the definition of 'management' according to the chapter?

- (X) Optimal cooperation of people and resources to achieve a goal
- ( ) Exclusively leading financial processes
- ( ) Making strategic decisions without implementation
- ( ) Managing only human resources

# reason
**Management** is defined as "optimal cooperation of people and resources to achieve a goal."
```

**Output:**
```tsv
What is the definition of 'management' according to the chapter?	✓ Optimal cooperation of people and resources to achieve a goal\n- Exclusively leading financial processes\n- Making strategic decisions without implementation\n- Managing only human resources
```

**Pros:**
- Maintains quiz context
- Shows alternative options
- User can self-test before flipping

**Cons:**
- More text on back side
- May reveal pattern if indicator is visible

#### Conversion Option C: Answer + Reason

**Input:**
```markdown
AWS: Which architecture approach is most suitable for GDPR compliance?

- ( ) Single global database in US-East region
- (X) Multi-region setup with data residency per country
- ( ) Separate databases without integration
- ( ) Cloud-only solution without on-premise components

# reason
**Multi-region setup with data residency** is correct because it meets GDPR requirements for data location while maintaining central access.
```

**Output:**
```tsv
AWS: Which architecture approach is most suitable for GDPR compliance?	Multi-region setup with data residency per country\n\nReason: Multi-region setup with data residency is correct because it meets GDPR requirements for data location while maintaining central access.
```

**Pros:**
- Educational value
- Complete context
- Explains why answer is correct

**Cons:**
- Longest back-side text
- May be too much information
- Flashcard Hero may not display reason section well

## Recommended Approach

**For this implementation, use Option A: Correct Answer Only**

Rationale:
- Flashcard Hero doesn't have native support for displaying reason sections
- Keeps cards focused and simple
- Users can reference original quiz markdown for detailed explanations
- Cleaner import experience
- Faster review sessions

## Example TSV Output

Based on the provided example, here's what the TSV should look like:

```tsv
S3: What is the max size of an S3 object in GB?	5000
S3: How many buckets can an account have?	100
S3: Max number of chars for a bucket name	63
S3: Min number of chars for a bucket name	3
IAM: Max number of users per account	5000
IAM: Max number of groups per account	100
DynamoDB: Min number of reserved capacity	100
DynamoDB: Max number of read/write capacity units	10000
EC2: What is a security group?	an AWS-provided firewall for the EC2 instance
What is the definition of 'management'?	Het optimaal laten samenwerken van mensen en middelen om een bepaald doel te bereiken
```

## Edge Cases and Handling

### Multiple Correct Answers

For multiple-choice questions with multiple correct answers:

**Input:**
```markdown
Which are characteristics of effective leadership? (Multiple answers possible)

- [X] Ability to motivate a team
- [X] Clear communication of objectives
- [ ] Authoritarian decision making
- [ ] Only focusing on short-term results
```

**Output Option 1 (Concatenate):**
```tsv
Which are characteristics of effective leadership?	Ability to motivate a team; Clear communication of objectives
```

**Output Option 2 (List):**
```tsv
Which are characteristics of effective leadership?	- Ability to motivate a team\n- Clear communication of objectives
```

### Special Characters in Text

**Tab characters in content:**
- Replace with spaces or escape

**Newlines in content:**
- Replace with `\n` literal or space depending on Flashcard Hero support

**Quotes:**
- Escape if necessary: `\"` or use smart quotes if supported

### Formatting

**Markdown formatting in answer:**
- **Bold** (`**text**`): Convert to plain text or keep asterisks
- *Italic* (`*text*`): Convert to plain text
- Code: Remove backticks

**Example:**
```markdown
# reason
**Management** is defined as "optimal *cooperation*" according to the text.
```

Should become:
```
Management is defined as "optimal cooperation" according to the text.
```

## Validation Rules

A valid TSV export must:
1. Have exactly 2 fields per line (front and back)
2. Use tab character as separator
3. Be UTF-8 encoded
4. Have at least one flashcard
5. Not have empty front or back fields
6. Properly escape special characters

## Testing

To verify the TSV output:
1. Open in spreadsheet application (should show 2 columns)
2. Import into Flashcard Hero
3. Check for proper display of:
   - Special characters (accents, symbols)
   - Multi-line content (if used)
   - Long text fields

## Implementation Notes

When implementing the converter:

1. **Parse quiz markdown** → extract questions and correct answers
2. **Extract correct answers** → from options marked with (X) or [X]
3. **Clean text** → remove markdown formatting
4. **Format TSV** → question<TAB>answer<NEWLINE>
5. **Validate** → ensure no empty fields, proper encoding
6. **Write file** → UTF-8 encoded TSV

The reason section from the quiz markdown should be **ignored** for Flashcard Hero export as the application doesn't have good support for displaying this additional context.
