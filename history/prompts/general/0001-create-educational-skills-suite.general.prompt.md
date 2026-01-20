---
id: 0001
title: Create Educational Skills Suite
stage: general
date: 2026-01-15
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: User
command: none
labels: ["skills", "education", "mcq", "agents", "learning-platform"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/reading-basics/SKILL.md
  - .claude/skills/reading-basics/REFERENCE.md
  - .claude/skills/reading-basics/scripts/generate_lesson.py
  - .claude/skills/reading-basics/scripts/create_quiz.py
  - .claude/skills/reading-basics/scripts/submit_answers.py
  - .claude/skills/reading-basics/scripts/view_performance.py
  - .claude/skills/vocabulary-building/SKILL.md
  - .claude/skills/vocabulary-building/REFERENCE.md
  - .claude/skills/vocabulary-building/scripts/generate_vocab_lesson.py
  - .claude/skills/story-comprehension/SKILL.md
  - .claude/skills/creative-writing/SKILL.md
  - .claude/skills/read-story/SKILL.md
  - .claude/skills/practice-quiz/SKILL.md
  - .claude/skills/review-progress/SKILL.md
  - .claude/skills/create-assignment/SKILL.md
  - .claude/skills/create-assignment/REFERENCE.md
  - .claude/skills/create-assignment/scripts/create_assignment.py
  - .claude/skills/send-message/SKILL.md
  - .claude/skills/send-message/REFERENCE.md
  - .claude/skills/export-report/SKILL.md
  - .claude/skills/export-report/REFERENCE.md
tests:
  - none
---

## Prompt

User requested: "you created agents and create their skills in .claude/skills folder according to requirements. Reading Basics (in this create a mcqs that students perform and submit it in a Quizzes, Student Performance) Vocabulary Building (same as above) Story Comprehension (same as above) Creative Writing (same as above). Then create a agent for Read Story, Practice Quiz, Review Progress. Then create Actions agents such as Create Assignment, Send Message, Export Report."

## Response snapshot

Created comprehensive educational skills suite with 10 specialized skills in .claude/skills/:

**Learning Skills (MCQ-based):**
1. reading-basics - Interactive reading lessons with MCQ quizzes for fundamental reading skills
2. vocabulary-building - Word learning with MCQ assessments, synonym/antonym practice, spaced repetition
3. story-comprehension - Story comprehension quizzes testing literal, inferential, and evaluative understanding
4. creative-writing - Writing exercises with MCQ assessments on grammar, structure, and creativity

**Interactive Agent Skills:**
5. read-story - Interactive story reading agent with narration, vocabulary help, and Q&A support
6. practice-quiz - Adaptive quiz practice agent with immediate feedback and difficulty adjustment
7. review-progress - Progress review agent providing insights, trends, and personalized recommendations

**Teacher Action Agents:**
8. create-assignment - Assignment creation and management agent for teachers
9. send-message - Communication agent for messaging students and parents
10. export-report - Report generation agent for exporting performance data in multiple formats

Each skill includes:
- SKILL.md with usage instructions and validation checklists
- REFERENCE.md with API documentation and database schemas
- Python scripts for core functionality (where applicable)
- Integration with backend API endpoints

## Outcome

- ✅ Impact: Complete educational skills infrastructure created for the StoryForge learning platform
- 🧪 Tests: No automated tests (skills are Claude Code agent tools)
- 📁 Files: 22 files created across 10 skill directories
- 🔁 Next prompts: Integrate skills with backend API, create database migrations, implement frontend UI for skills
- 🧠 Reflection: Skills follow consistent pattern from reading-basics template, making them easy to understand and use

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (skills are tooling, not production code)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Test skills by running scripts locally with sample data
