# Quiz Markdown Specification

This document defines the markdown format for quiz files used by `markdown-quiz-exporter-tool`.

## Overview

A quiz file contains one or more questions separated by horizontal rules (`---`). Each question consists of:

1. **Question text** - The question being asked (supports markdown)
2. **Answer options** - List of possible answers with correctness markers
3. **Reason block** - Explanation shown after answering (supports markdown)

## Question Separator

Questions are separated by a horizontal rule on its own line:

```
---
```

## Question Types

### Single Choice (Radio Buttons)

Use parentheses `( )` for single-choice questions where only one answer is correct.

- `(X)` or `(x)` - Correct answer
- `( )` - Incorrect answer

### Multiple Choice (Checkboxes)

Use square brackets `[ ]` for multiple-choice questions where multiple answers can be correct.

- `[X]` or `[x]` - Correct answer
- `[ ]` - Incorrect answer

## Basic Structure

```markdown
Question text goes here. Can be multiple lines.

- (X) Correct answer
- ( ) Incorrect answer
- ( ) Another incorrect answer
- ( ) Yet another incorrect answer

# reason
Explanation of why the correct answer is correct.
This section supports full markdown formatting.
```

## Answer Format

Answers follow this pattern:

```
- (X) Answer text
- ( ) Answer text
```

Or for multiple choice:

```
- [X] Correct answer 1
- [X] Correct answer 2
- [ ] Incorrect answer
```

### Rules

- Each answer starts with `- ` followed by the marker
- Marker is either `(X)`, `(x)`, `( )` for single choice
- Marker is either `[X]`, `[x]`, `[ ]` for multiple choice
- Answer text follows the marker on the same line
- Answer text can be empty if followed by a codeblock on subsequent lines

## Reason Block

The reason section starts with `# reason` on its own line:

```markdown
# reason
Your explanation here.

Supports **bold**, *italic*, `inline code`, and other markdown.
```

## Markdown Support

The following parts of a question support GitHub Flavored Markdown (GFM):

| Part | Markdown Support | Notes |
|------|------------------|-------|
| Question text | Yes | Full markdown including code blocks |
| Answer text | Yes | Full markdown including code blocks |
| Reason block | Yes | Full markdown including code blocks |

### Supported Markdown Features

- **Bold** (`**text**`) and *italic* (`*text*`)
- `Inline code` (`` `code` ``)
- Fenced code blocks with syntax highlighting (`` ```language ``)
- Bullet lists (`- item`) and numbered lists (`1. item`)
- Links (`[text](url)`)
- Paragraph breaks (blank lines between paragraphs)

## Code Block Support

### In Questions

Code blocks can appear inline with the question text:

```markdown
What does the following code output?

​```python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
​```

- (X) Hello, World!
- ( ) Hello, name!
- ( ) Error
- ( ) None
```

### In Answers

Answers can contain code blocks. The answer text can be on the same line as the marker, or the marker line can be empty with the code block on subsequent lines:

**With text and code:**

```markdown
- (X) The correct policy statement:
​```json
{
    "Action": ["s3:DeleteObject"],
    "Resource": ["arn:aws:s3:::bucket/*"],
    "Effect": "Allow"
}
​```
- ( ) Incorrect option
​```json
{
    "Action": ["s3:*"],
    "Resource": ["arn:aws:s3:::bucket/*"],
    "Effect": "Allow"
}
​```
```

**With empty marker line:**

```markdown
- (X)
​```json
{
    "Action": ["s3:DeleteObject"],
    "Resource": ["arn:aws:s3:::bucket/*"]
}
​```
- ( )
​```json
{
    "Action": ["s3:*"],
    "Resource": ["arn:aws:s3:::bucket/*"]
}
​```
```

### In Reasons

Reasons fully support code blocks with syntax highlighting:

```markdown
# reason
The correct answer uses the principle of least privilege.

​```json
{
    "Action": ["s3:DeleteObject"],
    "Resource": ["arn:aws:s3:::bucket/*"],
    "Effect": "Allow"
}
​```

Key points:
- Use specific actions, not wildcards
- Include `/*` after bucket name for object-level operations

**Reference:** https://example.com/docs
```

## Complete Examples

### Example 1: Simple Single Choice

```markdown
What is the capital of France?

- ( ) London
- ( ) Berlin
- (X) Paris
- ( ) Madrid

# reason
Paris is the capital and largest city of France, located on the Seine River.
```

### Example 2: Multiple Choice

```markdown
Which of the following are AWS compute services? (Select all that apply)

- [X] Amazon EC2
- [X] AWS Lambda
- [ ] Amazon S3
- [X] Amazon ECS
- [ ] Amazon RDS

# reason
AWS compute services include:
- **Amazon EC2** - Virtual servers
- **AWS Lambda** - Serverless functions
- **Amazon ECS** - Container orchestration

Amazon S3 is storage, and Amazon RDS is a database service.
```

### Example 3: Question with Code Block

```markdown
What will be the output of this Python code?

​```python
numbers = [1, 2, 3, 4, 5]
result = [x * 2 for x in numbers if x % 2 == 0]
print(result)
​```

- ( ) [2, 4, 6, 8, 10]
- (X) [4, 8]
- ( ) [1, 2, 3, 4, 5]
- ( ) Error

# reason
The list comprehension filters for even numbers (`x % 2 == 0`) and then doubles them.

1. Filter: `[2, 4]` (even numbers)
2. Transform: `[4, 8]` (doubled)

​```python
# Step by step:
numbers = [1, 2, 3, 4, 5]
evens = [x for x in numbers if x % 2 == 0]  # [2, 4]
result = [x * 2 for x in evens]              # [4, 8]
​```
```

### Example 4: Answers with Code Blocks

```markdown
Which IAM policy correctly grants DeleteObject permission on bucket objects?

- ( )
​```json
{
    "Action": ["s3:DeleteObject"],
    "Resource": ["arn:aws:s3:::my-bucket"],
    "Effect": "Allow"
}
​```
- (X)
​```json
{
    "Action": ["s3:DeleteObject"],
    "Resource": ["arn:aws:s3:::my-bucket/*"],
    "Effect": "Allow"
}
​```
- ( )
​```json
{
    "Action": ["s3:*"],
    "Resource": ["arn:aws:s3:::my-bucket/*"],
    "Effect": "Allow"
}
​```

# reason
The correct answer includes `/*` after the bucket name to target objects within the bucket.

- Option 1 targets the bucket itself, not objects
- Option 3 grants all S3 permissions, violating least privilege

**Reference:** https://aws.amazon.com/blogs/security/techniques-for-writing-least-privilege-iam-policies/
```

### Example 5: Multi-Question Quiz File

```markdown
What is 2 + 2?

- ( ) 3
- (X) 4
- ( ) 5
- ( ) 6

# reason
Basic arithmetic: 2 + 2 = 4

---

Which HTTP methods are considered safe? (Select all that apply)

- [X] GET
- [ ] POST
- [X] HEAD
- [ ] DELETE
- [X] OPTIONS

# reason
Safe HTTP methods do not modify server state:
- **GET** - Retrieve data
- **HEAD** - Like GET but no body
- **OPTIONS** - Get supported methods

POST and DELETE modify data and are not safe.

---

What does `ls -la` display?

- ( ) Only files
- ( ) Only directories
- (X) All files including hidden, in long format
- ( ) Only hidden files

# reason
The `ls` command options:
- `-l` - Long format (permissions, owner, size, date)
- `-a` - All files, including hidden (starting with `.`)

​```bash
$ ls -la
drwxr-xr-x  5 user group 160 Jan  1 12:00 .
drwxr-xr-x 10 user group 320 Jan  1 11:00 ..
-rw-r--r--  1 user group  42 Jan  1 12:00 .hidden
-rw-r--r--  1 user group 100 Jan  1 12:00 file.txt
​```
```

## Parser Behavior

1. Questions are split by `---` on a single line
2. The parser identifies answer markers to separate question text from answers
3. Answer text continues until the next answer marker or `# reason`
4. Everything after `# reason` until the next `---` or end of file is the reason
5. Whitespace is preserved for markdown rendering
6. Empty lines create paragraph breaks in the rendered output
