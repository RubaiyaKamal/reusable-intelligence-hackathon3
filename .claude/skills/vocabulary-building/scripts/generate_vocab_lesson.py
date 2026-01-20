#!/usr/bin/env python3
"""Vocabulary Building - Lesson Generator"""
import argparse, json, sys, requests, os
from datetime import datetime

API_URL = os.getenv("API_URL", "http://localhost:8001")

VOCABULARY_WORDS = {
    "beginner": [
        {"word": "happy", "definition": "feeling or showing pleasure", "synonyms": ["joyful", "glad"], "example": "She was happy to see her friend."},
        {"word": "big", "definition": "of considerable size or extent", "synonyms": ["large", "huge"], "example": "The elephant is a big animal."},
        {"word": "fast", "definition": "moving or capable of moving at high speed", "synonyms": ["quick", "rapid"], "example": "The car is very fast."}
    ],
    "intermediate": [
        {"word": "benevolent", "definition": "well meaning and kindly", "synonyms": ["kind", "compassionate"], "example": "The benevolent teacher helped struggling students."},
        {"word": "abundant", "definition": "existing or available in large quantities", "synonyms": ["plentiful", "ample"], "example": "The forest has abundant wildlife."}
    ],
    "advanced": [
        {"word": "eloquent", "definition": "fluent or persuasive in speaking or writing", "synonyms": ["articulate", "expressive"], "example": "Her eloquent speech moved the audience."},
        {"word": "meticulous", "definition": "showing great attention to detail", "synonyms": ["careful", "precise"], "example": "The meticulous craftsman created perfect furniture."}
    ]
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", required=True, choices=["beginner", "intermediate", "advanced"])
    parser.add_argument("--word-count", type=int, default=10)
    args = parser.parse_args()

    words = VOCABULARY_WORDS[args.level][:args.word_count]
    lesson_id = f"VB-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    lesson = {
        "id": lesson_id,
        "title": f"{args.level.capitalize()} Vocabulary",
        "level": args.level,
        "words": words,
        "created_at": datetime.now().isoformat()
    }

    with open("vocabulary_lessons.json", 'a') as f:
        json.dump(lesson, f)
        f.write('\n')

    print(f"✓ Vocabulary lesson '{lesson['title']}' created (ID: {lesson_id})")
    print(f"  Words: {len(words)}")

if __name__ == "__main__":
    main()
