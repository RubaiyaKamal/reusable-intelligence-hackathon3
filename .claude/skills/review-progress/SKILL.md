---
name: review-progress
description: AI agent for reviewing student progress with insights and recommendations
version: 1.0.0
author: StoryForge Team
tags: [agent, progress, analytics, reporting, insights]
---

# Review Progress Agent

## When to Use
- Students want to see their learning progress
- Teachers need performance summaries
- Generate progress reports and insights
- Identify strengths and areas for improvement

## What This Skill Does
An AI agent that analyzes student performance data and provides comprehensive progress reviews. Generates insights, identifies trends, and recommends personalized learning paths.

## Instructions

1. **Generate Progress Report**
   ```bash
   python scripts/generate_progress_report.py --student-id <id> --period <week|month|all>
   ```

2. **Get Performance Insights**
   ```bash
   python scripts/get_insights.py --student-id <id>
   ```

3. **Get Recommendations**
   ```bash
   python scripts/get_recommendations.py --student-id <id>
   ```

4. **Compare Performance**
   ```bash
   python scripts/compare_performance.py --student-id <id> --compare-to <class-average|previous-period>
   ```

## Validation Checklist
- [ ] Progress data aggregated correctly
- [ ] Visual progress charts generated
- [ ] Insights accurately reflect performance
- [ ] Recommendations personalized and actionable
- [ ] Report formatted for readability

## Expected Output
```
✓ Progress report generated for STU-123
✓ Period: Last 30 days
✓ Quizzes completed: 24
✓ Overall accuracy: 84%
✓ Improvement trend: +12% from previous period
✓ Strengths: Vocabulary (92%), Reading (87%)
✓ Focus areas: Comprehension (76%)
✓ Recommendations:
  - Practice more comprehension quizzes
  - Review inference and theme identification
  - Try intermediate-level stories
```

## Features
- **Comprehensive Analytics**: All learning activities tracked
- **Trend Analysis**: Performance over time
- **Skill Breakdown**: Performance by topic/skill
- **Personalized Recommendations**: AI-generated learning paths
- **Visual Reports**: Charts and graphs for clarity

See [REFERENCE.md](./REFERENCE.md) for detailed documentation.
