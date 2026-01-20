# Create Assignment - Reference Documentation

## Overview
Teacher action agent for creating and managing student assignments with scheduling and tracking.

## Assignment Types

### 1. Reading Assignment
- Assign specific stories or chapters
- Set reading level requirements
- Include comprehension quiz

### 2. Quiz Assignment
- Assign practice quizzes
- Set topic and difficulty
- Configure time limits

### 3. Writing Assignment
- Provide writing prompts
- Set word count requirements
- Include rubric

### 4. Custom Assignment
- Flexible task definition
- Custom requirements
- Manual grading

## API Reference

### Create Assignment
```python
from scripts.create_assignment import create_assignment

assignment = create_assignment(
    teacher_id="TCH-123",
    assignment_type="reading",
    title="Chapter 5 Reading",
    story_id="STY-456",
    due_date="2026-01-20",
    points=20,
    instructions="Read chapter 5 and complete the quiz"
)
```

### Assign to Students
```python
from scripts.assign_to_students import assign_assignment

assign_assignment(
    assignment_id="ASGN-001",
    student_ids=["STU-001", "STU-002"],
    class_ids=["CLS-4A"],
    send_notifications=True
)
```

## Database Schema

### `assignments` Table
```sql
CREATE TABLE assignments (
    id VARCHAR(50) PRIMARY KEY,
    teacher_id VARCHAR(50),
    type VARCHAR(20),
    title VARCHAR(200),
    instructions TEXT,
    due_date TIMESTAMP,
    points INT,
    created_at TIMESTAMP
);
```

### `student_assignments` Table
```sql
CREATE TABLE student_assignments (
    id SERIAL PRIMARY KEY,
    assignment_id VARCHAR(50),
    student_id VARCHAR(50),
    status VARCHAR(20),  -- assigned, in_progress, submitted, graded
    submitted_at TIMESTAMP,
    score INT,
    feedback TEXT
);
```

## Assignment Statuses
- **assigned**: Created and assigned to students
- **in_progress**: Student has started work
- **submitted**: Student completed submission
- **graded**: Teacher has graded submission

## Integration
POST /api/v1/assignments/create
POST /api/v1/assignments/:id/assign
GET /api/v1/assignments/:id/status
PATCH /api/v1/assignments/:id/update
