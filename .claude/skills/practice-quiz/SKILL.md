---
name: practice-quiz
description: Interactive quiz practice agent with adaptive difficulty and immediate feedback
version: 1.0.0
author: StoryForge Team
tags: [agent, quiz, practice, assessment, adaptive]
---

# Practice Quiz Agent

## When to Use
- Students want to practice quizzes on any topic
- Need adaptive difficulty based on performance
- Provide immediate feedback and explanations
- Support multiple quiz types (reading, vocab, comprehension)

## What This Skill Does
An AI agent that helps students practice quizzes interactively. Adapts difficulty based on performance, provides immediate feedback, explains answers, and suggests areas for improvement.

## Instructions

1. **Start Quiz Practice**
   ```bash
   python scripts/start_quiz_practice.py --student-id <id> --topic <reading|vocabulary|comprehension>
   ```

2. **Get Next Question**
   ```bash
   python scripts/get_quiz_question.py --session-id <session-id>
   ```

3. **Submit Answer**
   ```bash
   python scripts/submit_quiz_answer.py --session-id <session-id> --answer <answer-index>
   ```

4. **End Practice Session**
   ```bash
   python scripts/end_quiz_practice.py --session-id <session-id>
   ```

## Validation Checklist
- [ ] Quiz practice session initiated
- [ ] Questions adapt to student performance
- [ ] Immediate feedback provided
- [ ] Explanations clear and helpful
- [ ] Session results saved

## Expected Output
```
✓ Quiz practice started (ID: QP-001)
✓ Topic: Vocabulary
✓ Difficulty: Intermediate (auto-adjusted)
✓ Question 1/10 displayed
✓ Answer submitted: Correct! ✓
✓ Difficulty increased to Advanced
✓ Session completed: 8/10 (80%)
```

## Features
- **Adaptive Difficulty**: Adjusts based on performance
- **Immediate Feedback**: Instant correctness indication
- **Detailed Explanations**: Learn from mistakes
- **Topic Focus**: Practice specific skill areas
- **Performance Analytics**: Track improvement over time

See [REFERENCE.md](./REFERENCE.md) for detailed documentation.
