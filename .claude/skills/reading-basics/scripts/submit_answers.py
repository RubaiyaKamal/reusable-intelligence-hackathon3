#!/usr/bin/env python3
"""
Reading Basics - Answer Submission
Processes and scores student quiz submissions
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8001")

def load_quiz(quiz_id: str) -> Dict:
    """Load quiz from backend or local storage"""

    # Try backend first
    try:
        response = requests.get(
            f"{API_URL}/api/v1/reading-basics/quizzes/{quiz_id}",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass

    # Fallback to local file
    try:
        with open("reading_quizzes.json", 'r') as f:
            quizzes = json.load(f)
            for quiz in quizzes:
                if quiz['id'] == quiz_id:
                    return quiz
    except FileNotFoundError:
        pass

    return None

def score_quiz(quiz: Dict, answers: List[int]) -> Dict:
    """Score the quiz based on student answers"""

    if len(answers) != len(quiz['questions']):
        raise ValueError(f"Expected {len(quiz['questions'])} answers, got {len(answers)}")

    correct_count = 0
    results = []

    for i, (question, answer) in enumerate(zip(quiz['questions'], answers)):
        is_correct = (answer == question['correct_answer'])
        if is_correct:
            correct_count += 1

        results.append({
            "question_number": i + 1,
            "question": question['question'],
            "student_answer": question['options'][answer] if 0 <= answer < len(question['options']) else "Invalid",
            "correct_answer": question['options'][question['correct_answer']],
            "is_correct": is_correct,
            "explanation": question['explanation']
        })

    score = (correct_count / len(quiz['questions'])) * 100

    return {
        "total_questions": len(quiz['questions']),
        "correct_answers": correct_count,
        "incorrect_answers": len(quiz['questions']) - correct_count,
        "score_percentage": round(score, 2),
        "results": results
    }

def save_submission(submission: Dict) -> bool:
    """Save submission to backend or local storage"""

    # Try backend
    try:
        response = requests.post(
            f"{API_URL}/api/v1/reading-basics/submit",
            json=submission,
            timeout=10
        )
        if response.status_code in [200, 201]:
            print(f"✓ Submission saved to backend")
            return True
    except:
        pass

    # Fallback to local file
    submissions_file = "quiz_submissions.json"
    submissions = []

    try:
        with open(submissions_file, 'r') as f:
            submissions = json.load(f)
    except FileNotFoundError:
        pass

    submissions.append(submission)

    with open(submissions_file, 'w') as f:
        json.dump(submissions, f, indent=2)

    print(f"✓ Submission saved locally")
    return True

def main():
    parser = argparse.ArgumentParser(description="Submit and score quiz answers")
    parser.add_argument("--student-id", required=True, help="Student ID")
    parser.add_argument("--quiz-id", required=True, help="Quiz ID")
    parser.add_argument("--answers", required=True, help="Answer file (JSON array) or comma-separated indices")

    args = parser.parse_args()

    print(f"\n📤 Submitting Quiz Answers...")
    print(f"   Student: {args.student_id}")
    print(f"   Quiz: {args.quiz_id}\n")

    # Load quiz
    quiz = load_quiz(args.quiz_id)
    if not quiz:
        print(f"✗ Quiz {args.quiz_id} not found!")
        sys.exit(1)

    print(f"✓ Quiz loaded: {quiz['lesson_title']}")
    print(f"  Questions: {quiz['total_questions']}")

    # Parse answers
    try:
        if args.answers.endswith('.json'):
            with open(args.answers, 'r') as f:
                answers = json.load(f)
        else:
            answers = [int(x.strip()) for x in args.answers.split(',')]
    except Exception as e:
        print(f"✗ Error parsing answers: {e}")
        sys.exit(1)

    print(f"✓ Answers received: {len(answers)} responses\n")

    # Score quiz
    try:
        scoring_result = score_quiz(quiz, answers)
    except ValueError as e:
        print(f"✗ Scoring error: {e}")
        sys.exit(1)

    # Create submission record
    submission = {
        "student_id": args.student_id,
        "quiz_id": args.quiz_id,
        "lesson_id": quiz['lesson_id'],
        "lesson_title": quiz['lesson_title'],
        "level": quiz['level'],
        "answers": answers,
        "scoring": scoring_result,
        "submitted_at": datetime.now().isoformat()
    }

    # Save submission
    if save_submission(submission):
        print(f"\n{'='*60}")
        print(f"📊 QUIZ RESULTS")
        print(f"{'='*60}")
        print(f"Student: {args.student_id}")
        print(f"Quiz: {quiz['lesson_title']}")
        print(f"Level: {quiz['level']}")
        print(f"\n  Score: {scoring_result['correct_answers']}/{scoring_result['total_questions']} ({scoring_result['score_percentage']}%)")
        print(f"  ✓ Correct: {scoring_result['correct_answers']}")
        print(f"  ✗ Incorrect: {scoring_result['incorrect_answers']}")

        # Show grade
        score_pct = scoring_result['score_percentage']
        if score_pct >= 90:
            grade = "A (Excellent!)"
        elif score_pct >= 80:
            grade = "B (Great job!)"
        elif score_pct >= 70:
            grade = "C (Good effort!)"
        elif score_pct >= 60:
            grade = "D (Keep practicing!)"
        else:
            grade = "F (Let's review this together!)"

        print(f"\n  Grade: {grade}")

        # Show incorrect answers
        incorrect = [r for r in scoring_result['results'] if not r['is_correct']]
        if incorrect:
            print(f"\n  📝 Review These Questions:")
            for result in incorrect:
                print(f"\n  Q{result['question_number']}: {result['question']}")
                print(f"     Your answer: {result['student_answer']}")
                print(f"     Correct answer: {result['correct_answer']}")
                print(f"     💡 {result['explanation']}")

        print(f"\n{'='*60}")
        print(f"✓ Results saved successfully!")
        print(f"✓ Performance data updated")
        print(f"{'='*60}\n")
    else:
        print("✗ Failed to save submission")
        sys.exit(1)

if __name__ == "__main__":
    main()
