#!/usr/bin/env python3
"""
Reading Basics - Quiz Creator
Creates MCQ quizzes based on reading lessons
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8001")

def load_lesson(lesson_id: str) -> Dict:
    """Load lesson from backend or local storage"""

    # Try backend first
    try:
        response = requests.get(
            f"{API_URL}/api/v1/reading-basics/lessons/{lesson_id}",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass

    # Fallback to local file
    try:
        with open("reading_lessons.json", 'r') as f:
            lessons = json.load(f)
            for lesson in lessons:
                if lesson['id'] == lesson_id:
                    return lesson
    except FileNotFoundError:
        pass

    return None

def generate_mcq_questions(lesson: Dict, num_questions: int) -> List[Dict]:
    """Generate MCQ questions based on lesson content"""

    questions = []

    # Sample questions for different levels
    if lesson['level'] == 'beginner' and 'Letter' in lesson['title']:
        questions = [
            {
                "question": "What sound does the letter 'A' make?",
                "options": ["Ah", "Bee", "See", "Dee"],
                "correct_answer": 0,
                "explanation": "The letter A makes the 'Ah' sound like in Apple."
            },
            {
                "question": "Which word starts with the 'A' sound?",
                "options": ["Cat", "Apple", "Dog", "Fish"],
                "correct_answer": 1,
                "explanation": "Apple starts with the 'A' sound."
            },
            {
                "question": "Point to the letter that makes the 'Ah' sound:",
                "options": ["B", "C", "A", "D"],
                "correct_answer": 2,
                "explanation": "The letter A makes the 'Ah' sound."
            },
            {
                "question": "Which animal name starts with 'A'?",
                "options": ["Ant", "Bee", "Cat", "Dog"],
                "correct_answer": 0,
                "explanation": "Ant starts with the letter A."
            },
            {
                "question": "What is the first letter in 'Alligator'?",
                "options": ["L", "I", "G", "A"],
                "correct_answer": 3,
                "explanation": "Alligator starts with the letter A."
            },
            {
                "question": "Which word does NOT start with 'A'?",
                "options": ["Apple", "Ant", "Ball", "Ask"],
                "correct_answer": 2,
                "explanation": "Ball starts with B, not A."
            },
            {
                "question": "The letter A sounds like:",
                "options": ["ah", "bee", "see", "dee"],
                "correct_answer": 0,
                "explanation": "A makes the 'ah' sound."
            },
            {
                "question": "How many words start with A: Apple, Cat, Ant?",
                "options": ["1", "2", "3", "0"],
                "correct_answer": 1,
                "explanation": "Apple and Ant start with A, that's 2 words."
            },
            {
                "question": "Which letter comes after A in the alphabet?",
                "options": ["B", "C", "Z", "A"],
                "correct_answer": 0,
                "explanation": "B comes after A in the alphabet."
            },
            {
                "question": "Is 'Ambulance' a word that starts with A?",
                "options": ["Yes", "No"],
                "correct_answer": 0,
                "explanation": "Yes, Ambulance starts with the letter A."
            }
        ]
    elif 'Word Families' in lesson['title'] or '-at' in lesson['title']:
        questions = [
            {
                "question": "Which word is in the -at family?",
                "options": ["dog", "cat", "run", "big"],
                "correct_answer": 1,
                "explanation": "Cat ends with -at, so it's in the -at family."
            },
            {
                "question": "What do words in a word family have in common?",
                "options": ["Same ending", "Same beginning", "Same length", "Nothing"],
                "correct_answer": 0,
                "explanation": "Word families have the same ending and rhyme."
            },
            {
                "question": "Which word rhymes with 'cat'?",
                "options": ["dog", "hat", "pig", "sun"],
                "correct_answer": 1,
                "explanation": "Hat rhymes with cat (both end in -at)."
            },
            {
                "question": "Add 'r' to the front of '-at'. What word do you make?",
                "options": ["rat", "tar", "art", "tra"],
                "correct_answer": 0,
                "explanation": "r + at = rat"
            },
            {
                "question": "Which is NOT in the -at word family?",
                "options": ["mat", "hat", "cat", "run"],
                "correct_answer": 3,
                "explanation": "Run doesn't end with -at."
            }
        ]
    else:
        # Generic questions
        questions = [
            {
                "question": f"What is the main topic of this lesson?",
                "options": [lesson['title'], "Math", "Science", "Art"],
                "correct_answer": 0,
                "explanation": f"This lesson is about {lesson['title']}."
            },
            {
                "question": "What level is this reading lesson?",
                "options": [lesson['level'], "advanced", "expert", "master"],
                "correct_answer": 0,
                "explanation": f"This is a {lesson['level']} level lesson."
            }
        ]

    # Return requested number of questions
    return questions[:num_questions]

def save_quiz(quiz: Dict) -> bool:
    """Save quiz to backend or local storage"""

    # Try backend
    try:
        response = requests.post(
            f"{API_URL}/api/v1/reading-basics/quizzes",
            json=quiz,
            timeout=10
        )
        if response.status_code in [200, 201]:
            print(f"✓ Quiz saved to backend: {quiz['id']}")
            return True
    except:
        pass

    # Fallback to local file
    quizzes_file = "reading_quizzes.json"
    quizzes = []

    try:
        with open(quizzes_file, 'r') as f:
            quizzes = json.load(f)
    except FileNotFoundError:
        pass

    quizzes.append(quiz)

    with open(quizzes_file, 'w') as f:
        json.dump(quizzes, f, indent=2)

    print(f"✓ Quiz saved locally: {quiz['id']}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Create MCQ quiz for reading lesson")
    parser.add_argument("--lesson-id", required=True, help="Lesson ID")
    parser.add_argument("--questions", type=int, default=10, help="Number of questions (default: 10)")

    args = parser.parse_args()

    print(f"\n📝 Creating MCQ Quiz...")
    print(f"   Lesson ID: {args.lesson_id}")
    print(f"   Questions: {args.questions}\n")

    # Load lesson
    lesson = load_lesson(args.lesson_id)
    if not lesson:
        print(f"✗ Lesson {args.lesson_id} not found!")
        sys.exit(1)

    print(f"✓ Lesson loaded: {lesson['title']}")

    # Generate questions
    questions = generate_mcq_questions(lesson, args.questions)

    quiz_id = f"QUIZ-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    quiz = {
        "id": quiz_id,
        "lesson_id": args.lesson_id,
        "lesson_title": lesson['title'],
        "level": lesson['level'],
        "questions": questions,
        "total_questions": len(questions),
        "created_at": datetime.now().isoformat()
    }

    # Save quiz
    if save_quiz(quiz):
        print(f"\n✓ Quiz '{quiz_id}' created successfully!")
        print(f"  Lesson: {lesson['title']}")
        print(f"  Questions: {len(questions)}")
        print(f"\n📋 Sample Questions:")
        for i, q in enumerate(questions[:3]):
            print(f"  {i+1}. {q['question']}")
            for j, opt in enumerate(q['options']):
                marker = "✓" if j == q['correct_answer'] else " "
                print(f"     {marker} {chr(65+j)}. {opt}")
        if len(questions) > 3:
            print(f"  ... and {len(questions) - 3} more questions")
        print(f"\n✓ Ready for student submissions!")
    else:
        print("✗ Failed to save quiz")
        sys.exit(1)

if __name__ == "__main__":
    main()
