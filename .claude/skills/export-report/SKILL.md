---
name: export-report
description: Report generation and export agent for student performance and analytics
version: 1.0.0
author: StoryForge Team
tags: [agent, reporting, export, analytics, action]
---

# Export Report Agent

## When to Use
- Generate student progress reports
- Export performance data for analysis
- Create printable report cards
- Share analytics with parents/administrators

## What This Skill Does
An action agent that generates comprehensive reports from student performance data. Exports reports in multiple formats (PDF, Excel, CSV) with customizable metrics and visualizations.

## Instructions

1. **Generate Student Report**
   ```bash
   python scripts/generate_student_report.py --student-id <id> --period <week|month|semester> --format <pdf|excel|csv>
   ```

2. **Generate Class Report**
   ```bash
   python scripts/generate_class_report.py --class-id <id> --period <week|month|semester> --format <pdf|excel>
   ```

3. **Export Performance Data**
   ```bash
   python scripts/export_performance_data.py --student-ids <ids> --metrics <accuracy|progress|time> --format <csv|excel>
   ```

4. **Create Report Card**
   ```bash
   python scripts/create_report_card.py --student-id <id> --semester <semester> --format pdf
   ```

## Validation Checklist
- [ ] Report generated with all requested metrics
- [ ] Data accurately reflects student performance
- [ ] Format is correct (PDF/Excel/CSV)
- [ ] Visualizations render properly
- [ ] File saved to correct location

## Expected Output
```
✓ Student report generated (STU-123)
✓ Period: Last 30 days
✓ Format: PDF
✓ Sections:
  - Performance Summary
  - Quiz Results (24 quizzes)
  - Reading Progress (8 stories)
  - Vocabulary Growth (45 new words)
  - Recommendations
✓ Charts: 5 visualizations included
✓ File saved: reports/STU-123_2026-01.pdf
✓ File size: 1.2 MB
```

## Features
- **Multiple Formats**: PDF, Excel, CSV, JSON
- **Customizable Metrics**: Choose what data to include
- **Visual Analytics**: Charts and graphs
- **Batch Export**: Generate multiple reports at once
- **Scheduled Reports**: Auto-generate weekly/monthly
- **Email Integration**: Send reports directly to parents

See [REFERENCE.md](./REFERENCE.md) for detailed documentation.
