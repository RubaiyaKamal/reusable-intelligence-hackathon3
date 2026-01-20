#!/usr/bin/env python3
"""
Reading Basics - Performance Viewer
Displays student performance metrics and progress
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List
import requests
import os
from collections import defaultdict

API_URL = os.getenv("API_URL", "http://localhost:8001")

def load_student_submissions(student_id: str) -> List[Dict]:
    """Load all submissions for a student"""

    submissions = []

    # Try backend first
    try:
        response = requests.get(
            f"{API_URL}/api/v1/reading-basics/performance/{student_id}",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass

    # Fallback to local file
    try:
        with open("quiz_submissions.json", 'r') as f:
            all_submissions = json.load(f)
            submissions = [s for s in all_submissions if s['student_id'] == student_id]
    except FileNotFoundError:
        pass

    return submissions

def calculate_performance_metrics(submissions: List[Dict]) -> Dict:
    """Calculate comprehensive performance metrics"""

    if not submissions:
        return None

    total_quizzes = len(submissions)
    total_questions = sum(s['scoring']['total_questions'] for s in submissions)
    total_correct = sum(s['scoring']['correct_answers'] for s in submissions)

    # Calculate average score
    avg_score = (total_correct / total_questions * 100) if total_questions > 0 else 0

    # Track performance by level
    by_level = defaultdict(lambda: {'quizzes': 0, 'correct': 0, 'total': 0})
    for sub in submissions:
        level = sub.get('level', 'unknown')
        by_level[level]['quizzes'] += 1
        by_level[level]['correct'] += sub['scoring']['correct_answers']
        by_level[level]['total'] += sub['scoring']['total_questions']

    level_performance = {}
    for level, data in by_level.items():
        level_performance[level] = {
            'quizzes_taken': data['quizzes'],
            'accuracy': round((data['correct'] / data['total'] * 100) if data['total'] > 0 else 0, 2)
        }

    # Track performance by topic
    by_topic = defaultdict(lambda: {'correct': 0, 'total': 0})
    for sub in submissions:
        topic = sub.get('lesson_title', 'Unknown')
        by_topic[topic]['correct'] += sub['scoring']['correct_answers']
        by_topic[topic]['total'] += sub['scoring']['total_questions']

    topic_performance = {}
    for topic, data in by_topic.items():
        topic_performance[topic] = {
            'accuracy': round((data['correct'] / data['total'] * 100) if data['total'] > 0 else 0, 2),
            'questions_answered': data['total']
        }

    # Recent performance trend
    sorted_submissions = sorted(submissions, key=lambda x: x['submitted_at'])
    recent_scores = [s['scoring']['score_percentage'] for s in sorted_submissions[-5:]]

    return {
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'total_correct': total_correct,
        'overall_accuracy': round(avg_score, 2),
        'level_performance': level_performance,
        'topic_performance': topic_performance,
        'recent_scores': recent_scores,
        'latest_submission': sorted_submissions[-1]['submitted_at'] if sorted_submissions else None
    }

def display_performance(student_id: str, metrics: Dict):
    """Display performance metrics in a readable format"""

    print(f"\n{'='*70}")
    print(f"📈 STUDENT PERFORMANCE REPORT")
    print(f"{'='*70}")
    print(f"Student ID: {student_id}")
    if metrics['latest_submission']:
        print(f"Last Activity: {metrics['latest_submission'][:10]}")
    print(f"{'-'*70}")

    # Overall Stats
    print(f"\n📊 OVERALL STATISTICS")
    print(f"  Quizzes Completed: {metrics['total_quizzes']}")
    print(f"  Questions Answered: {metrics['total_questions']}")
    print(f"  Correct Answers: {metrics['total_correct']}")
    print(f"  Overall Accuracy: {metrics['overall_accuracy']}%")

    # Grade assessment
    accuracy = metrics['overall_accuracy']
    if accuracy >= 90:
        assessment = "Excellent! Outstanding performance! 🌟"
    elif accuracy >= 80:
        assessment = "Great work! Keep it up! 💪"
    elif accuracy >= 70:
        assessment = "Good progress! 👍"
    elif accuracy >= 60:
        assessment = "Making progress. Keep practicing! 📚"
    else:
        assessment = "Needs improvement. Let's review together! 🤝"

    print(f"  Assessment: {assessment}")

    # Performance by level
    if metrics['level_performance']:
        print(f"\n📚 PERFORMANCE BY LEVEL")
        for level, data in metrics['level_performance'].items():
            print(f"  {level.capitalize()}:")
            print(f"    Quizzes: {data['quizzes_taken']}")
            print(f"    Accuracy: {data['accuracy']}%")

    # Performance by topic
    if metrics['topic_performance']:
        print(f"\n📖 PERFORMANCE BY TOPIC")
        sorted_topics = sorted(
            metrics['topic_performance'].items(),
            key=lambda x: x[1]['accuracy'],
            reverse=True
        )
        for topic, data in sorted_topics[:5]:
            print(f"  {topic}:")
            print(f"    Accuracy: {data['accuracy']}% ({data['questions_answered']} questions)")

    # Recent performance trend
    if metrics['recent_scores']:
        print(f"\n📈 RECENT PERFORMANCE TREND")
        print(f"  Last 5 quizzes: {', '.join(f'{s:.1f}%' for s in metrics['recent_scores'])}")

        if len(metrics['recent_scores']) >= 2:
            trend = metrics['recent_scores'][-1] - metrics['recent_scores'][0]
            if trend > 0:
                print(f"  Trend: ⬆️ Improving (+{trend:.1f}%)")
            elif trend < 0:
                print(f"  Trend: ⬇️ Declining ({trend:.1f}%)")
            else:
                print(f"  Trend: ➡️ Stable")

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    weak_topics = [
        topic for topic, data in metrics['topic_performance'].items()
        if data['accuracy'] < 70
    ]

    if weak_topics:
        print(f"  Focus on these topics:")
        for topic in weak_topics[:3]:
            print(f"    • {topic}")
    else:
        print(f"  • Great work across all topics!")
        print(f"  • Try advancing to the next level")

    if accuracy < 80:
        print(f"  • Review incorrect answers and explanations")
        print(f"  • Practice more quizzes on challenging topics")

    print(f"\n{'='*70}\n")

def main():
    parser = argparse.ArgumentParser(description="View student performance metrics")
    parser.add_argument("--student-id", required=True, help="Student ID")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    print(f"\n📊 Loading performance data for {args.student_id}...")

    # Load submissions
    submissions = load_student_submissions(args.student_id)

    if not submissions:
        print(f"\n✗ No quiz submissions found for student {args.student_id}")
        print(f"  Student hasn't taken any quizzes yet.")
        sys.exit(0)

    print(f"✓ Found {len(submissions)} quiz submission(s)\n")

    # Calculate metrics
    metrics = calculate_performance_metrics(submissions)

    if not metrics:
        print(f"✗ Unable to calculate performance metrics")
        sys.exit(1)

    # Display results
    if args.format == "json":
        print(json.dumps(metrics, indent=2))
    else:
        display_performance(args.student_id, metrics)

if __name__ == "__main__":
    main()
