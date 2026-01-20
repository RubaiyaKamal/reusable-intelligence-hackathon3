# Reading Basics - Reference Documentation

## Overview
The Reading Basics skill provides interactive reading lessons with MCQ-based assessments for elementary students.

## Architecture

### Components
1. **Lesson Generator**: Creates age-appropriate reading content
2. **Quiz Engine**: Generates multiple-choice questions
3. **Answer Processor**: Validates and scores student submissions
4. **Performance Tracker**: Records and analyzes student progress

### Data Flow
```
Student → Reading Lesson → MCQ Quiz → Submit Answers → Score → Performance DB
```

## API Reference

### Generate Lesson
```python
from scripts.generate_lesson import create_reading_lesson

lesson = create_reading_lesson(
    level="beginner",  # beginner, intermediate, advanced
    topic="Phonics",
    student_age=7
)
```

### Create Quiz
```python
from scripts.create_quiz import generate_mcq_quiz

quiz = generate_mcq_quiz(
    lesson_id="RB-001",
    num_questions=10,
    difficulty="easy"
)
```

### Submit Answers
```python
from scripts.submit_answers import submit_student_answers

result = submit_student_answers(
    student_id="STU-123",
    quiz_id="QUIZ-456",
    answers=[0, 2, 1, 3, 0, 1, 2, 3, 1, 0]  # Answer indices
)
```

## Database Schema

### `reading_lessons` Table
```sql
CREATE TABLE reading_lessons (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    level VARCHAR(20),
    topic VARCHAR(100),
    created_at TIMESTAMP
);
```

### `reading_quizzes` Table
```sql
CREATE TABLE reading_quizzes (
    id VARCHAR(50) PRIMARY KEY,
    lesson_id VARCHAR(50),
    questions JSONB,
    created_at TIMESTAMP
);
```

### `quiz_submissions` Table
```sql
CREATE TABLE quiz_submissions (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50),
    quiz_id VARCHAR(50),
    answers JSONB,
    score FLOAT,
    submitted_at TIMESTAMP
);
```

## MCQ Question Format

```json
{
  "question": "What sound does the letter 'A' make?",
  "options": ["Ah", "Bee", "See", "Dee"],
  "correct_answer": 0,
  "explanation": "The letter A makes the 'Ah' sound in most words."
}
```

## Performance Metrics

- **Accuracy**: Percentage of correct answers
- **Speed**: Time taken per question
- **Improvement**: Progress over time
- **Weak Areas**: Topics needing reinforcement

## Integration

### With Backend API
```bash
POST /api/v1/reading-basics/lessons
POST /api/v1/reading-basics/quizzes
POST /api/v1/reading-basics/submit
GET /api/v1/reading-basics/performance/:studentId
```

### With Frontend
The skill integrates with the StoryForge frontend through the quiz interface components.

## Examples

### Complete Workflow
```bash
# 1. Generate lesson
python scripts/generate_lesson.py --level beginner --topic "Letter Sounds"

# 2. Create quiz
python scripts/create_quiz.py --lesson-id RB-001 --questions 10

# 3. Student takes quiz and submits
python scripts/submit_answers.py --student-id STU-123 --quiz-id QUIZ-001 --answers answers.json

# 4. View results
python scripts/view_performance.py --student-id STU-123
```

## Troubleshooting

### Common Issues
1. **Quiz not generating**: Check if lesson exists in database
2. **Submission failed**: Validate answer format (array of integers)
3. **Performance not updating**: Verify database connection

## Best Practices
- Keep questions age-appropriate
- Provide clear, helpful explanations
- Track progress consistently
- Adjust difficulty based on performance
