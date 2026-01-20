---
name: create-assignment
description: Teacher action agent for creating and managing student assignments
version: 1.0.0
author: StoryForge Team
tags: [agent, teacher, assignment, action, management]
---

# Create Assignment Agent

## When to Use
- Teachers need to create new assignments
- Assign reading materials to students
- Set quiz deadlines and requirements
- Manage assignment distribution to classes

## What This Skill Does
An action agent for teachers to create, configure, and assign learning activities to students. Supports reading assignments, quiz assignments, and custom learning tasks with due dates and requirements.

## Instructions

1. **Create New Assignment**
   ```bash
   python scripts/create_assignment.py --teacher-id <id> --type <reading|quiz|writing> --title "<title>"
   ```

2. **Configure Assignment Details**
   ```bash
   python scripts/configure_assignment.py --assignment-id <id> --due-date <date> --points <points> --instructions "<text>"
   ```

3. **Assign to Students/Classes**
   ```bash
   python scripts/assign_to_students.py --assignment-id <id> --student-ids <id1,id2> --class-ids <class1,class2>
   ```

4. **View Assignment Status**
   ```bash
   python scripts/view_assignment_status.py --assignment-id <id>
   ```

## Validation Checklist
- [ ] Assignment created with all required fields
- [ ] Due date and points configured
- [ ] Assigned to correct students/classes
- [ ] Notifications sent to students
- [ ] Assignment visible in student dashboard

## Expected Output
```
✓ Assignment created (ID: ASGN-001)
✓ Type: Reading
✓ Title: "Read Chapter 5 and Complete Quiz"
✓ Due date: 2026-01-20
✓ Points: 20
✓ Assigned to: 25 students (Class 4A)
✓ Notifications sent: 25/25
✓ Status: Active
```

## Features
- **Multiple Assignment Types**: Reading, quizzes, writing, custom
- **Flexible Scheduling**: Set due dates and reminders
- **Bulk Assignment**: Assign to classes or individual students
- **Progress Tracking**: Monitor completion status
- **Grading Support**: Point-based grading system

See [REFERENCE.md](./REFERENCE.md) for detailed documentation.
