---
name: pg-data-backup-restore
description: Automated PostgreSQL backup and recovery system
version: 1.0.0
author: Hackathon Team
tags: [postgresql, backup, disaster-recovery, automation]
---

# Pg Data Backup Restore

## When to Use
- Automated PostgreSQL backup and recovery system
- Need automated postgresql operations
- Part of CI/CD or infrastructure automation

## What This Skill Does
Automates pg data backup restore with production-ready scripts and configurations.

## Instructions

1. **Setup/Deploy**
   ```bash
   ./scripts/backup_db.sh
   ```

2. **Configure/Create**
   ```bash
   python scripts/restore_db.sh
   ```

3. **Verify/Test**
   ```bash
   python scripts/schedule_backups.py
   ```

## Validation Checklist
- [ ] Setup completed successfully
- [ ] Configuration applied
- [ ] Tests pass
- [ ] Integrated with existing services

## Expected Output
```
✓ pg-data-backup-restore configured
✓ All components operational
✓ Tests passed
```

See [REFERENCE.md](./REFERENCE.md) for detailed documentation and advanced usage.
