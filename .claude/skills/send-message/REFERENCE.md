# Send Message - Reference Documentation

## Overview
Communication agent for messaging and notifications in the learning platform.

## Message Types

### 1. Individual Message
Direct one-on-one communication between teacher and student/parent

### 2. Class Announcement
Broadcast message to entire class

### 3. Assignment Notification
Automated reminders for upcoming assignments

### 4. Progress Update
Performance feedback and encouragement

## API Reference

### Send Message
```python
from scripts.send_individual_message import send_message

message = send_message(
    from_id="TCH-123",
    to_id="STU-456",
    subject="Great progress!",
    message="You're doing excellent work in reading!",
    priority="normal"  # low, normal, high
)
```

## Database Schema

### `messages` Table
```sql
CREATE TABLE messages (
    id VARCHAR(50) PRIMARY KEY,
    from_id VARCHAR(50),
    to_id VARCHAR(50),
    subject VARCHAR(200),
    message TEXT,
    priority VARCHAR(20),
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    read_at TIMESTAMP
);
```

## Message Templates

### Assignment Reminder
```text
Subject: Assignment Due Soon
Message: Hi {student_name}, your assignment "{assignment_title}" is due on {due_date}.
Good luck!
```

### Progress Congratulations
```text
Subject: Great Progress!
Message: Congratulations {student_name}! You've improved your reading score by {percentage}%.
Keep up the excellent work!
```

## Integration
POST /api/v1/messages/send
POST /api/v1/messages/broadcast
GET /api/v1/messages/:id/status
