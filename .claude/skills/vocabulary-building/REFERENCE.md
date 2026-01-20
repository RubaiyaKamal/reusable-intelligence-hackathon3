# Vocabulary Building - Reference Documentation

## Overview
Interactive vocabulary learning system with MCQ-based assessments and spaced repetition.

## Key Features
- Word definitions and meanings
- Synonym and antonym practice
- Contextual usage examples
- Spaced repetition for retention
- Word mastery tracking

## API Reference

### Generate Vocabulary Lesson
```python
from scripts.generate_vocab_lesson import create_vocabulary_lesson

lesson = create_vocabulary_lesson(
    level="intermediate",
    word_count=10,
    category="adjectives"  # nouns, verbs, adjectives, adverbs
)
```

### MCQ Question Types
1. **Definition**: "What does 'benevolent' mean?"
2. **Synonym**: "Which word is closest in meaning to 'happy'?"
3. **Antonym**: "What is the opposite of 'difficult'?"
4. **Usage**: "Which sentence uses 'abundant' correctly?"
5. **Context Clues**: Read passage and identify word meaning

## Database Schema

### `vocabulary_lessons` Table
```sql
CREATE TABLE vocabulary_lessons (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(200),
    level VARCHAR(20),
    words JSONB,
    category VARCHAR(50),
    created_at TIMESTAMP
);
```

### `word_mastery` Table
```sql
CREATE TABLE word_mastery (
    student_id VARCHAR(50),
    word VARCHAR(100),
    mastery_level VARCHAR(20),  -- learning, practicing, mastered
    attempts INT,
    correct_count INT,
    last_reviewed TIMESTAMP,
    PRIMARY KEY (student_id, word)
);
```

## Word Mastery Levels
- **Learning**: 0-40% accuracy, review daily
- **Practicing**: 41-79% accuracy, review weekly
- **Mastered**: 80%+ accuracy, review monthly

## Integration
POST /api/v1/vocabulary/lessons
POST /api/v1/vocabulary/quizzes
POST /api/v1/vocabulary/submit
GET /api/v1/vocabulary/progress/:studentId
