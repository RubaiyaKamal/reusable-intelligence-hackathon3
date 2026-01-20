---
name: reading-basics
description: Interactive reading basics with MCQ quizzes for student assessment
version: 1.0.0
author: StoryForge Team
tags: [education, reading, quiz, assessment, mcq]
---

# Reading Basics

## When to Use
- Teaching fundamental reading skills to students
- Creating interactive reading exercises with assessment
- Generating MCQ quizzes for reading comprehension
- Tracking student performance on reading basics

## What This Skill Does
Creates interactive reading basics lessons with multiple-choice questions. Students can complete exercises, submit answers, and track their performance through the quiz system.

## Instructions

1. **Generate Reading Basics Lesson**
   ```bash
   python scripts/generate_lesson.py --level <beginner|intermediate|advanced> --topic <topic-name>
   ```

2. **Create MCQ Quiz**
   ```bash
   python scripts/create_quiz.py --lesson-id <lesson-id> --questions 10
   ```

3. **Submit Student Answers**
   ```bash
   python scripts/submit_answers.py --student-id <id> --quiz-id <quiz-id> --answers <json-file>
   ```

4. **View Performance**
   ```bash
   python scripts/view_performance.py --student-id <id>
   ```

## Validation Checklist
- [ ] Reading lesson generated with appropriate difficulty level
- [ ] MCQ quiz created with 10+ questions
- [ ] Student can submit answers
- [ ] Performance metrics calculated correctly
- [ ] Results saved to database

## Expected Output
```
✓ Reading lesson "Phonics Basics" created (ID: RB-001)
✓ MCQ quiz generated with 12 questions
✓ Student answers submitted successfully
✓ Score: 10/12 (83.3%)
✓ Performance data saved
```

## Features
- **Adaptive Difficulty**: Adjusts content based on student reading level
- **Interactive MCQs**: Multiple-choice questions with immediate feedback
- **Progress Tracking**: Monitors student performance over time
- **Detailed Analytics**: Provides insights into learning patterns

See [REFERENCE.md](./REFERENCE.md) for detailed documentation and API reference.
