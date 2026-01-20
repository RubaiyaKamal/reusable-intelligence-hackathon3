---
name: read-story
description: Interactive story reading agent with narration and comprehension support
version: 1.0.0
author: StoryForge Team
tags: [agent, reading, story, education, interactive]
---

# Read Story Agent

## When to Use
- Students want to read a story interactively
- Need narration or text-to-speech support
- Provide reading assistance and vocabulary help
- Track reading progress and engagement

## What This Skill Does
An AI agent that helps students read stories interactively. Provides narration, explains difficult words, answers questions about the story, and tracks reading progress.

## Instructions

1. **Start Reading Session**
   ```bash
   python scripts/start_reading_session.py --student-id <id> --story-id <story-id>
   ```

2. **Get Story Content**
   ```bash
   python scripts/get_story_content.py --session-id <session-id> --page <page-num>
   ```

3. **Ask Question During Reading**
   ```bash
   python scripts/ask_reading_question.py --session-id <session-id> --question "<question>"
   ```

4. **Complete Reading Session**
   ```bash
   python scripts/complete_reading.py --session-id <session-id>
   ```

## Validation Checklist
- [ ] Reading session created with story content
- [ ] Story displayed with proper formatting
- [ ] Word definitions available on request
- [ ] Questions answered contextually
- [ ] Reading progress tracked

## Expected Output
```
✓ Reading session started (ID: RS-001)
✓ Story: "The Magical Forest" (12 pages)
✓ Reading level: Intermediate
✓ Page 1/12 displayed
✓ Vocabulary help available
✓ Progress: 8% complete
```

## Features
- **Interactive Reading**: Page-by-page navigation
- **Vocabulary Assistant**: Click words for definitions
- **Q&A Support**: Answer questions about story content
- **Progress Tracking**: Monitor reading completion
- **Bookmarking**: Save reading position

See [REFERENCE.md](./REFERENCE.md) for detailed documentation.
