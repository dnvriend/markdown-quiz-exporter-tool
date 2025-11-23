# Quiz Markdown Format Specification

Complete technical specification for quiz markdown files.

## Overview

Quiz files are plain markdown (`.md`) files containing questions, answer options, and explanations. Each file can contain multiple questions separated by `---` delimiters.

## File Structure

```
question-text
[blank line]
answer-options
[blank line]
reasoning
---
next-question
...
```

## Question Format

### Question Text

The question text appears at the start of each block:
- Can be single or multiple lines
- Should end with a question mark (?)
- No special formatting required
- Supports markdown formatting if needed

Example:
```markdown
Wat wordt bedoeld met een 'onderneming' volgens het hoofdstuk?
```

Multi-line example:
```markdown
Een onderneming wil haar strategische positie verbeteren.
Welke analysemethode is het meest geschikt voor het identificeren
van concurrentievoordelen?
```

### Answer Options

Answer options come after a blank line following the question text.

#### Single Choice Questions

Use parentheses notation `( )` for single-choice (radio button) questions:

```markdown
- (X) Correct answer
- ( ) Incorrect option 1
- ( ) Incorrect option 2
- ( ) Incorrect option 3
```

**Notation:**
- `(X)` or `(x)` = correct answer (case-insensitive)
- `( )` = incorrect answer

#### Multiple Choice Questions

Use square brackets notation `[ ]` for multiple-choice (checkbox) questions:

```markdown
- [X] Correct answer 1
- [ ] Incorrect option
- [X] Correct answer 2
- [ ] Incorrect option 2
```

**Notation:**
- `[X]` or `[x]` = correct answer (case-insensitive)
- `[ ]` = incorrect answer

#### Option Guidelines

- Each option starts with `- ` (dash + space)
- Followed by checkbox/radio notation
- Then option text
- Typically 4 options per question (can be 2-6)
- At least one correct answer required
- Avoid "all of the above" or "none of the above" options

### Reasoning Section

The reasoning section explains the correct answer and references source material.

#### Format

```markdown
# reason
Explanation text with **bold terms** and source references.
```

- Starts with `# reason` (markdown heading level 1)
- Followed by explanation text
- Must be on separate lines (not inline)
- Supports full markdown formatting

#### Content Requirements

The reasoning should:
1. Explain WHY the answer is correct
2. Reference the source material
3. Use **bold** for key terms
4. Quote definitions when applicable
5. Be clear and educational

Example:
```markdown
# reason
**Management** wordt gedefinieerd als "het optimaal laten samenwerken van mensen en middelen om een bepaald doel te bereiken." Het hoofdstuk benadrukt drie kernwoorden: samenwerken, optimaal, en bepaald doel.
```

### Question Separator

Questions are separated by three dashes on a single line:

```markdown
---
```

- Must be on its own line
- Exactly three dashes
- No spaces before or after
- Separates all questions in the file

## Complete Example

### Single Choice Question

```markdown
Wat is de definitie van 'management' volgens het hoofdstuk?

- (X) Het optimaal laten samenwerken van mensen en middelen om een bepaald doel te bereiken
- ( ) Het uitsluitend leiden van financiële processen
- ( ) Het maken van strategische beslissingen zonder implementatie
- ( ) Het beheren van alleen menselijke resources

# reason
**Management** wordt gedefinieerd als "het optimaal laten samenwerken van mensen en middelen om een bepaald doel te bereiken." Het hoofdstuk benadrukt drie kernwoorden: samenwerken, optimaal, en bepaald doel.

---
```

### Multiple Choice Question

```markdown
Welke van de volgende zijn kenmerken van effectief leiderschap? (Meerdere antwoorden mogelijk)

- [X] Het vermogen om een team te motiveren
- [X] Duidelijke communicatie van doelstellingen
- [ ] Autoritair beslissingen nemen zonder input
- [ ] Alleen focussen op korte termijn resultaten

# reason
Effectief leiderschap vereist **motivatie** en **duidelijke communicatie**. Het hoofdstuk stelt dat "een goede leider het team motiveert en doelstellingen helder communiceert." Autoritair leiderschap en korte termijn focus worden niet als effectieve kenmerken beschouwd.

---
```

### AWS Case Scenario Question

```markdown
Een multinational heeft vestigingen in 15 landen met verschillende compliance-eisen.
Het bedrijf wil een centrale HR-database implementeren die voldoet aan GDPR en
lokale regelgeving. Welke architectuur-aanpak is het meest geschikt?

- ( ) Single global database in US-East region voor alle data
- (X) Multi-region setup met data residency per land en centrale federatie
- ( ) Separate databases zonder integratie tussen landen
- ( ) Cloud-only oplossing zonder on-premise componenten

# reason
**Multi-region setup met data residency** is de juiste aanpak omdat het voldoet aan GDPR-vereisten voor data locatie terwijl centrale toegang mogelijk blijft. Een single global database voldoet niet aan data residency eisen. Separate databases zonder integratie verliezen centrale HR-functionaliteit. Cloud-only kan conflicteren met sommige lokale compliance eisen die on-premise opslag vereisen.

---
```

## File Naming Convention

Quiz files should follow this naming pattern:

```
quiz-<module>-<topic>.md
```

Examples:
- `quiz-mo-1-1-introductie.md`
- `quiz-bav-wetenschappelijk-onderzoek.md`
- `quiz-mo-strategie.md`

## Validation Rules

A valid quiz file must:
1. Have at least one question
2. Each question has 2-6 answer options
3. Each question has at least one correct answer
4. Questions are separated by `---`
5. Each question has a `# reason` section
6. Use consistent notation (all `()` or all `[]` per question)

## Common Mistakes to Avoid

❌ **Missing blank lines**
```markdown
Question text?
- ( ) Option 1  # Wrong: no blank line before options
```

✅ **Correct format**
```markdown
Question text?

- ( ) Option 1
```

---

❌ **Mixing checkbox styles**
```markdown
- [X] Option 1
- ( ) Option 2  # Wrong: mixing [] and ()
```

✅ **Consistent style**
```markdown
- [X] Option 1
- [ ] Option 2
```

---

❌ **Inline reason**
```markdown
- (X) Correct answer # reason: because...  # Wrong
```

✅ **Separate reason section**
```markdown
- (X) Correct answer

# reason
Explanation here...
```

---

❌ **No separator between questions**
```markdown
Question 1?
- (X) Answer

# reason
Explanation.

Question 2?  # Wrong: no --- separator
```

✅ **Proper separation**
```markdown
Question 1?
- (X) Answer

# reason
Explanation.

---

Question 2?
```
