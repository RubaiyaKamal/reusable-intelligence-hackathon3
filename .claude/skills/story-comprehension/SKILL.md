---
name: story-comprehension
description: Story comprehension assessment with MCQ quizzes for understanding and analysis
version: 1.0.0
author: StoryForge Team
tags: [education, comprehension, reading, quiz, assessment, mcq]
---

# Story Comprehension

## When to Use
- Assessing reading comprehension after story completion
- Testing understanding of plot, characters, and themes
- Evaluating inference and critical thinking skills
- Tracking comprehension progress over time

## What This Skill Does
Creates comprehension quizzes based on stories students have read. Tests literal understanding, inference, theme identification, and character analysis through MCQ assessments.

## Instructions

1. **Generate Comprehension Quiz from Story**
   ```bash
   python scripts/generate_comprehension_quiz.py --story-id <story-id> --questions 12
   ```

2. **Submit Student Answers**
   ```bash
   python scripts/submit_comprehension.py --student-id <id> --quiz-id <quiz-id> --answers <json-file>
   ```

3. **View Comprehension Progress**
   ```bash
   python scripts/view_comprehension_progress.py --student-id <id>
   ```

## Validation Checklist
- [ ] Quiz covers main plot points and details
- [ ] Questions test multiple comprehension levels (literal, inferential, evaluative)
- [ ] Character and theme questions included
- [ ] Answers provide explanations with story references
- [ ] Progress tracked by comprehension skill type

## Expected Output
```
✓ Comprehension quiz for "The Adventure Begins" created (ID: SC-001)
✓ 12 questions covering plot, characters, and themes
✓ Student answers submitted
✓ Score: 10/12 (83.3%)
✓ Strong in: Plot recall, Character understanding
✓ Needs work: Theme identification, Inference
```

## Features
- **Multi-level Questions**: Literal, inferential, evaluative
- **Story References**: Questions cite specific story passages
- **Skill Breakdown**: Performance by comprehension type
- **Progressive Difficulty**: Adapts to student level

See [REFERENCE.md](./REFERENCE.md) for detailed documentation.
