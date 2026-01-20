---
name: send-message
description: Communication agent for sending messages between teachers, students, and parents
version: 1.0.0
author: StoryForge Team
tags: [agent, communication, messaging, action, notifications]
---

# Send Message Agent

## When to Use
- Teachers need to communicate with students/parents
- Send assignment reminders and notifications
- Provide feedback and encouragement
- Broadcast announcements to classes

## What This Skill Does
An action agent for managing communication in the learning platform. Sends messages, notifications, and announcements to students and parents with delivery tracking and read receipts.

## Instructions

1. **Send Individual Message**
   ```bash
   python scripts/send_individual_message.py --from <teacher-id> --to <student-id> --subject "<subject>" --message "<text>"
   ```

2. **Send Class Announcement**
   ```bash
   python scripts/send_class_announcement.py --from <teacher-id> --class-id <class-id> --subject "<subject>" --message "<text>"
   ```

3. **Send Assignment Reminder**
   ```bash
   python scripts/send_assignment_reminder.py --assignment-id <id> --recipients <student-ids>
   ```

4. **View Message Status**
   ```bash
   python scripts/view_message_status.py --message-id <id>
   ```

## Validation Checklist
- [ ] Message composed with subject and body
- [ ] Recipients selected correctly
- [ ] Message delivered successfully
- [ ] Delivery status tracked
- [ ] Read receipts recorded (if enabled)

## Expected Output
```
✓ Message sent (ID: MSG-001)
✓ From: Teacher Sarah (TCH-456)
✓ To: 25 students (Class 4A)
✓ Subject: "Great work this week!"
✓ Delivered: 25/25 (100%)
✓ Read: 18/25 (72%)
✓ Delivery time: 0.8 seconds
```

## Features
- **Individual & Group Messaging**: One-to-one or one-to-many
- **Message Templates**: Pre-written messages for common scenarios
- **Delivery Tracking**: Monitor message delivery status
- **Read Receipts**: See who has read messages
- **Scheduled Messages**: Send messages at specific times
- **Rich Content**: Include links, images, and formatting

See [REFERENCE.md](./REFERENCE.md) for detailed documentation.
