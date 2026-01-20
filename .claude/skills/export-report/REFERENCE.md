# Export Report - Reference Documentation

## Overview
Report generation and export agent for comprehensive student analytics.

## Report Types

### 1. Student Progress Report
Comprehensive view of individual student performance

### 2. Class Summary Report
Aggregated performance metrics for entire class

### 3. Report Card
Formal grade report with letter grades and comments

### 4. Performance Data Export
Raw data export for custom analysis

## Export Formats

### PDF
- Professional layout
- Charts and visualizations
- Printable format
- File size: 0.5-2 MB

### Excel
- Multiple worksheets
- Sortable data tables
- Pivot table ready
- File size: 0.1-0.5 MB

### CSV
- Raw data format
- Easy to import
- Compatible with all tools
- File size: 10-100 KB

## API Reference

### Generate Report
```python
from scripts.generate_student_report import generate_report

report = generate_report(
    student_id="STU-123",
    period="month",
    format="pdf",
    include_charts=True,
    sections=["summary", "quizzes", "reading", "vocabulary"]
)
```

## Report Sections

### Performance Summary
- Overall accuracy
- Quizzes completed
- Reading progress
- Grade assessment

### Quiz Results
- Breakdown by topic
- Accuracy trends
- Time per quiz
- Difficulty progression

### Reading Progress
- Stories completed
- Reading level advancement
- Comprehension scores
- Time spent reading

### Vocabulary Growth
- New words learned
- Word mastery levels
- Retention rate
- Usage in writing

## Database Schema

### `reports` Table
```sql
CREATE TABLE reports (
    id VARCHAR(50) PRIMARY KEY,
    student_id VARCHAR(50),
    report_type VARCHAR(50),
    period VARCHAR(20),
    format VARCHAR(10),
    file_path VARCHAR(500),
    generated_at TIMESTAMP
);
```

## Chart Types

1. **Line Chart**: Progress over time
2. **Bar Chart**: Performance by topic
3. **Pie Chart**: Time distribution
4. **Radar Chart**: Skill comparison

## Integration
POST /api/v1/reports/generate
GET /api/v1/reports/:id/download
GET /api/v1/reports/student/:studentId
