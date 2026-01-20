---
name: vocabulary-building
description: Interactive vocabulary learning with MCQ quizzes and word mastery tracking
version: 1.0.0
author: StoryForge Team
tags: [education, vocabulary, quiz, assessment, mcq, words]
---

# Vocabulary Building

## When to Use
- Teaching new vocabulary to students
- Creating word definition and usage quizzes
- Building vocabulary through contextual learning
- Tracking word mastery progress

## What This Skill Does
Creates interactive vocabulary lessons with MCQ-based assessments. Students learn new words, their meanings, usage, and synonyms through engaging quizzes that track their vocabulary mastery.

## Instructions

1. **Generate Vocabulary Lesson**
   ```bash
   python scripts/generate_vocab_lesson.py --level <beginner|intermediate|advanced> --word-count 10
   ```

2. **Create Vocabulary Quiz**
   ```bash
   python scripts/create_vocab_quiz.py --lesson-id <lesson-id> --questions 15
   ```

3. **Submit Student Answers**
   ```bash
   python scripts/submit_vocab_answers.py --student-id <id> --quiz-id <quiz-id> --answers <json-file>
   ```

4. **View Vocabulary Progress**
   ```bash
   python scripts/view_vocab_progress.py --student-id <id>
   ```

## Validation Checklist
- [ ] Vocabulary lesson generated with age-appropriate words
- [ ] MCQ quiz includes definitions, synonyms, and usage questions
- [ ] Student can submit answers and receive immediate feedback
- [ ] Word mastery levels tracked (learning, practicing, mastered)
- [ ] Progress metrics saved to database

## Expected Output
```
✓ Vocabulary lesson "Common Adjectives" created (ID: VB-001)
✓ MCQ quiz generated with 15 questions
✓ Student answers submitted successfully
✓ Score: 13/15 (86.7%)
✓ New words mastered: 3
✓ Words to review: 2
```

## Features
- **Word Categories**: Nouns, verbs, adjectives, adverbs
- **Contextual Learning**: Words shown in example sentences
- **Spaced Repetition**: Reviews words based on mastery level
- **Synonym/Antonym Practice**: Expands vocabulary connections
- **Usage Examples**: Real-world sentence construction

See [REFERENCE.md](./REFERENCE.md) for detailed documentation.
