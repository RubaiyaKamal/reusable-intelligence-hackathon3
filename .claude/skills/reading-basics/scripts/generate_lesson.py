#!/usr/bin/env python3
"""
Reading Basics - Lesson Generator
Generates age-appropriate reading lessons for students
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List
import requests
import os

# Backend API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8001")

READING_TOPICS = {
    "beginner": [
        "Letter Sounds (Phonics)",
        "CVC Words (Cat, Dog, Run)",
        "Sight Words (The, And, Is)",
        "Simple Sentences",
        "Picture Reading"
    ],
    "intermediate": [
        "Word Families (-at, -an, -it)",
        "Blends and Digraphs (ch, sh, th)",
        "Long and Short Vowels",
        "Compound Words",
        "Reading Fluency"
    ],
    "advanced": [
        "Silent Letters (know, write)",
        "Multi-syllable Words",
        "Prefixes and Suffixes",
        "Context Clues",
        "Reading Comprehension"
    ]
}

def generate_lesson_content(level: str, topic: str, student_age: int) -> Dict:
    """Generate reading lesson content using AI"""

    lesson_templates = {
        "beginner": {
            "Letter Sounds (Phonics)": {
                "intro": "Let's learn about letter sounds! Each letter makes a special sound.",
                "content": """
Today we'll explore the sounds that letters make!

**The Letter A**
The letter A makes the "ah" sound like in:
- Apple
- Ant
- Ask

**Practice:**
Say these words out loud:
1. Alligator
2. Ambulance
3. Animal

Can you think of more words that start with the "ah" sound?
""",
                "key_points": [
                    "Letter A makes the 'ah' sound",
                    "Listen for the sound at the beginning of words",
                    "Practice makes perfect!"
                ]
            }
        },
        "intermediate": {
            "Word Families (-at, -an, -it)": {
                "intro": "Word families are groups of words that end the same way!",
                "content": """
Let's learn about the -at word family!

**Words in the -at family:**
- cat
- hat
- mat
- rat
- bat
- sat

Notice how they all rhyme? They end with the same sound!

**Practice:**
Can you make new -at words by changing the first letter?
""",
                "key_points": [
                    "Word families rhyme",
                    "They have the same ending",
                    "Change the first letter to make new words"
                ]
            }
        }
    }

    # Get template or generate simple content
    template = lesson_templates.get(level, {}).get(topic, {
        "intro": f"Welcome to {topic}!",
        "content": f"This lesson teaches you about {topic}.",
        "key_points": [f"Learn {topic}", "Practice regularly", "Have fun!"]
    })

    lesson_id = f"RB-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "id": lesson_id,
        "title": topic,
        "level": level,
        "student_age": student_age,
        "intro": template["intro"],
        "content": template["content"],
        "key_points": template["key_points"],
        "created_at": datetime.now().isoformat()
    }

def save_lesson(lesson: Dict) -> bool:
    """Save lesson to backend or local storage"""

    # Try to save to backend API
    try:
        response = requests.post(
            f"{API_URL}/api/v1/reading-basics/lessons",
            json=lesson,
            timeout=10
        )
        if response.status_code in [200, 201]:
            print(f"✓ Lesson saved to backend: {lesson['id']}")
            return True
    except:
        # Fallback to local JSON file
        lessons_file = "reading_lessons.json"
        lessons = []

        try:
            with open(lessons_file, 'r') as f:
                lessons = json.load(f)
        except FileNotFoundError:
            pass

        lessons.append(lesson)

        with open(lessons_file, 'w') as f:
            json.dump(lessons, f, indent=2)

        print(f"✓ Lesson saved locally: {lesson['id']}")
        return True

    return False

def main():
    parser = argparse.ArgumentParser(description="Generate reading basics lesson")
    parser.add_argument("--level", required=True, choices=["beginner", "intermediate", "advanced"],
                       help="Reading level")
    parser.add_argument("--topic", required=True, help="Lesson topic")
    parser.add_argument("--age", type=int, default=7, help="Student age (default: 7)")

    args = parser.parse_args()

    print(f"\n📚 Generating Reading Basics Lesson...")
    print(f"   Level: {args.level}")
    print(f"   Topic: {args.topic}")
    print(f"   Age: {args.age}\n")

    # Generate lesson
    lesson = generate_lesson_content(args.level, args.topic, args.age)

    # Save lesson
    if save_lesson(lesson):
        print(f"\n✓ Lesson '{lesson['title']}' created successfully!")
        print(f"  ID: {lesson['id']}")
        print(f"  Level: {lesson['level']}")
        print(f"\n📖 Preview:")
        print(f"  {lesson['intro']}")
        print(f"\n  Key Points:")
        for point in lesson['key_points']:
            print(f"    • {point}")
        print(f"\n✓ Ready for quiz creation!")
    else:
        print("✗ Failed to save lesson")
        sys.exit(1)

if __name__ == "__main__":
    main()
