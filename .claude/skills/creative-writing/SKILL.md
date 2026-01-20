---
name: creative-writing
description: Creative writing exercises with MCQ-based grammar, style, and structure assessment
version: 1.0.0
author: StoryForge Team
tags: [education, writing, creativity, quiz, assessment, mcq, grammar]
---

# Creative Writing

## When to Use
- Teaching creative writing techniques
- Assessing grammar and style understanding
- Evaluating narrative structure knowledge
- Providing writing prompts and feedback

## What This Skill Does
Provides creative writing prompts and exercises with MCQ assessments covering grammar, sentence structure, narrative techniques, and creative elements. Students practice writing and demonstrate understanding through quizzes.

## Instructions

1. **Generate Writing Prompt**
   ```bash
   python scripts/generate_writing_prompt.py --type <story|poem|essay> --level <beginner|intermediate|advanced>
   ```

2. **Create Writing Skills Quiz**
   ```bash
   python scripts/create_writing_quiz.py --prompt-id <prompt-id> --focus <grammar|structure|creativity>
   ```

3. **Submit Student Answers**
   ```bash
   python scripts/submit_writing_quiz.py --student-id <id> --quiz-id <quiz-id> --answers <json-file>
   ```

4. **View Writing Progress**
   ```bash
   python scripts/view_writing_progress.py --student-id <id>
   ```

## Validation Checklist
- [ ] Writing prompt generated with clear guidelines
- [ ] Quiz covers grammar, structure, and creativity
- [ ] Examples demonstrate good writing techniques
- [ ] Feedback provided on writing skills
- [ ] Progress tracked by writing component

## Expected Output
```
✓ Writing prompt "Adventure Story Starter" created (ID: CW-001)
✓ Skills quiz generated with 10 questions
✓ Topics: Grammar (4), Structure (3), Creativity (3)
✓ Student answers submitted
✓ Score: 8/10 (80%)
✓ Strong in: Grammar, Creativity
✓ Needs work: Story structure
```

## Features
- **Diverse Prompts**: Stories, poems, essays, descriptions
- **Grammar Focus**: Sentence structure, punctuation, parts of speech
- **Narrative Elements**: Plot, character, setting, dialogue
- **Style Techniques**: Show vs tell, descriptive language, voice

See [REFERENCE.md](./REFERENCE.md) for detailed documentation.
