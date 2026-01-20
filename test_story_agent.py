"""
Test script for Story Agent functionality
"""

import requests
import json
from typing import Dict, Any


# Test configuration
BASE_URL = "http://localhost:8001"
API_URL = f"{BASE_URL}/api/v1"


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_response(response: Dict[str, Any]):
    """Print formatted response"""
    print(json.dumps(response, indent=2))


def test_story_generation():
    """Test basic story generation"""
    print_header("TEST 1: Basic Story Generation")

    payload = {
        "story_type": "adventure",
        "reading_level": 50,
        "length": "short",
        "student_id": "test_user_001"
    }

    print(f"\nRequest: {json.dumps(payload, indent=2)}")

    response = requests.post(
        f"{API_URL}/story/generate",
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        print(f"\n[OK] Story Generated!")
        print(f"\nTitle: {data.get('title')}")
        print(f"\nStory Preview (first 200 chars):\n{data.get('story', '')[:200]}...")
        print(f"\nReading Level: {data.get('reading_level')}")
        print(f"Word Count: {data.get('metadata', {}).get('word_count')}")
        print(f"Vocabulary Words: {', '.join(data.get('vocabulary_words', [])[:5])}")
    else:
        print(f"[ERROR] Status: {response.status_code}")
        print(f"Response: {response.text}")


def test_story_with_theme():
    """Test story generation with specific theme"""
    print_header("TEST 2: Story with Specific Theme")

    payload = {
        "story_type": "friendship",
        "reading_level": 60,
        "length": "medium",
        "theme": "two friends solving a mystery together",
        "moral_lesson": "teamwork makes challenges easier",
        "student_id": "test_user_002"
    }

    print(f"\nRequest theme: {payload['theme']}")
    print(f"Moral lesson: {payload['moral_lesson']}")

    response = requests.post(
        f"{API_URL}/story/generate",
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        print(f"\n[OK] Themed Story Generated!")
        print(f"\nTitle: {data.get('title')}")
        print(f"Story Type: {data.get('story_type')}")
        print(f"Reading Time: {data.get('metadata', {}).get('estimated_reading_time')} min")
    else:
        print(f"[ERROR] Status: {response.status_code}")


def test_story_with_characters():
    """Test story generation with specific characters"""
    print_header("TEST 3: Story with Custom Characters")

    payload = {
        "story_type": "fantasy",
        "reading_level": 40,
        "length": "short",
        "characters": ["Luna the brave cat", "Max the wise owl"],
        "student_id": "test_user_003"
    }

    print(f"\nCharacters: {', '.join(payload['characters'])}")

    response = requests.post(
        f"{API_URL}/story/generate",
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        print(f"\n[OK] Character Story Generated!")
        print(f"\nTitle: {data.get('title')}")
        print(f"Characters in metadata: {data.get('metadata', {}).get('characters')}")
    else:
        print(f"[ERROR] Status: {response.status_code}")


def test_different_reading_levels():
    """Test stories at different reading levels"""
    print_header("TEST 4: Different Reading Levels")

    levels = [
        (20, "beginner"),
        (40, "early"),
        (60, "intermediate"),
        (90, "advanced")
    ]

    for level_num, level_name in levels:
        print(f"\nGenerating {level_name} level story (level {level_num})...")

        payload = {
            "story_type": "animal",
            "reading_level": level_num,
            "length": "short",
            "student_id": f"test_user_{level_name}"
        }

        response = requests.post(
            f"{API_URL}/story/generate",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            vocab_count = len(data.get('vocabulary_words', []))
            word_count = data.get('metadata', {}).get('word_count', 0)
            print(f"  [OK] {level_name}: {word_count} words, {vocab_count} vocab words")
        else:
            print(f"  [ERROR] {level_name}: {response.status_code}")


def test_story_continuation():
    """Test story continuation"""
    print_header("TEST 5: Story Continuation")

    # First generate a story
    print("\nStep 1: Generate initial story...")
    gen_response = requests.post(
        f"{API_URL}/story/generate",
        json={
            "story_type": "mystery",
            "reading_level": 50,
            "length": "short",
            "student_id": "test_user_005"
        }
    )

    if gen_response.status_code != 200:
        print(f"[ERROR] Initial generation failed: {gen_response.status_code}")
        return

    story_data = gen_response.json()
    initial_story = story_data.get('story', '')
    print(f"[OK] Initial story generated ({len(initial_story)} chars)")

    # Now continue it
    print("\nStep 2: Continue the story...")
    cont_response = requests.post(
        f"{API_URL}/story/continue",
        json={
            "previous_story": initial_story,
            "user_input": "the characters discover a hidden clue",
            "reading_level": 50,
            "student_id": "test_user_005"
        }
    )

    if cont_response.status_code == 200:
        cont_data = cont_response.json()
        continuation = cont_data.get('continuation', '')
        print(f"[OK] Continuation generated!")
        print(f"\nContinuation preview:\n{continuation[:200]}...")
        print(f"\nFull story length: {len(cont_data.get('full_story', ''))} chars")
    else:
        print(f"[ERROR] Continuation failed: {cont_response.status_code}")


def test_story_types():
    """Test getting available story types"""
    print_header("TEST 6: Available Story Types")

    response = requests.get(f"{API_URL}/story/types")

    if response.status_code == 200:
        data = response.json()
        print(f"\n[OK] Available story types:")
        for story_type in data.get('story_types', []):
            print(f"  - {story_type}")
    else:
        print(f"[ERROR] Status: {response.status_code}")


def test_story_stats():
    """Test story statistics"""
    print_header("TEST 7: Story Statistics")

    response = requests.get(f"{API_URL}/story/stats")

    if response.status_code == 200:
        data = response.json()
        print("\n[OK] Story Statistics:")
        print_response(data)
    else:
        print(f"[ERROR] Status: {response.status_code}")


def test_integrated_routing():
    """Test integrated routing to story agent"""
    print_header("TEST 8: Integrated Routing")

    payload = {
        "query": "Tell me a story about a brave dragon",
        "student_id": "test_user_008",
        "context": {
            "reading_level": 55
        }
    }

    print(f"\nQuery: {payload['query']}")

    response = requests.post(
        f"{API_URL}/query",
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        print(f"\n[OK] Integrated routing successful!")
        print(f"\nResponse preview:\n{data.get('response', '')[:300]}...")
    else:
        print(f"[ERROR] Status: {response.status_code}")


def check_health():
    """Check if backend is healthy"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        return response.status_code == 200
    except:
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  STORYFORGE STORY AGENT TEST SUITE")
    print("=" * 60)

    # Check health first
    print("\n[HEALTH CHECK] Checking backend health...")
    if not check_health():
        print("[ERROR] Backend is not responding. Please ensure:")
        print("   1. Docker containers are running: docker-compose ps")
        print("   2. Backend is healthy: curl http://localhost:8001/health")
        return

    print("[OK] Backend is healthy!")

    # Run all tests
    try:
        test_story_generation()
        test_story_with_theme()
        test_story_with_characters()
        test_different_reading_levels()
        test_story_continuation()
        test_story_types()
        test_story_stats()
        test_integrated_routing()

        print_header("[SUCCESS] ALL TESTS COMPLETED")

    except Exception as e:
        print(f"\n[ERROR] Test failed with error: {e}")


if __name__ == "__main__":
    main()
