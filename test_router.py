"""
Test script for Router Agent functionality
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


def test_story_intent():
    """Test routing for story generation queries"""
    print_header("TEST 1: Story Intent Detection")

    queries = [
        "Tell me a story about a dragon",
        "Can you create a story about friendship?",
        "Once upon a time there was a brave knight"
    ]

    for query in queries:
        print(f"\nQuery: \"{query}\"")
        response = requests.post(
            f"{API_URL}/router/route",
            json={
                "query": query,
                "student_id": "test_user_001"
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] Routed to: {data['agent'].upper()} Agent")
            print(f"   [OK] Engagement: {data['engagement']}")
            print(f"   [OK] Confidence: {data['confidence']:.1%}")
        else:
            print(f"   [ERROR] Status: {response.status_code}")


def test_comprehension_intent():
    """Test routing for comprehension queries"""
    print_header("TEST 2: Comprehension Intent Detection")

    queries = [
        "What happened in the story?",
        "Who is the main character?",
        "Why did the hero go on a quest?",
        "Summarize the story for me"
    ]

    for query in queries:
        print(f"\n📝 Query: \"{query}\"")
        response = requests.post(
            f"{API_URL}/router/route",
            json={
                "query": query,
                "student_id": "test_user_002"
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Routed to: {data['agent'].upper()} Agent")
            print(f"   ✓ Engagement: {data['engagement']}")
        else:
            print(f"   ✗ Error: {response.status_code}")


def test_vocabulary_intent():
    """Test routing for vocabulary queries"""
    print_header("TEST 3: Vocabulary Intent Detection")

    queries = [
        "What does 'brave' mean?",
        "What is a dragon?",
        "I don't understand the word 'quest'",
        "Define friendship"
    ]

    for query in queries:
        print(f"\n📝 Query: \"{query}\"")
        response = requests.post(
            f"{API_URL}/router/route",
            json={
                "query": query,
                "student_id": "test_user_003"
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Routed to: {data['agent'].upper()} Agent")
            print(f"   ✓ Engagement: {data['engagement']}")
        else:
            print(f"   ✗ Error: {response.status_code}")


def test_engagement_detection():
    """Test engagement level detection"""
    print_header("TEST 4: Engagement Detection")

    test_cases = [
        ("Wow! This is amazing! Tell me more!", "excited"),
        ("I don't understand this at all", "confused"),
        ("This is too hard, I give up", "frustrated"),
        ("This is boring, show me something else", "bored"),
        ("Why does the character do that?", "curious")
    ]

    for query, expected_engagement in test_cases:
        print(f"\n📝 Query: \"{query}\"")
        print(f"   Expected: {expected_engagement}")

        response = requests.post(
            f"{API_URL}/router/route",
            json={
                "query": query,
                "student_id": "test_user_004"
            }
        )

        if response.status_code == 200:
            data = response.json()
            actual = data['engagement']
            match = "✓" if actual == expected_engagement else "?"
            print(f"   {match} Detected: {actual}")
        else:
            print(f"   ✗ Error: {response.status_code}")


def test_context_awareness():
    """Test routing with context (reading level, failures)"""
    print_header("TEST 5: Context-Aware Routing")

    # Test with low reading level
    print("\n📝 Low reading level context:")
    response = requests.post(
        f"{API_URL}/router/route",
        json={
            "query": "Tell me a story",
            "student_id": "test_user_005",
            "context": {
                "reading_level": 25,
                "age": 6
            }
        }
    )

    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Routed to: {data['agent'].upper()} Agent")
        print(f"   ✓ Metadata: {data['metadata']}")

    # Test with repeated failures
    print("\n📝 Repeated failures context:")
    response = requests.post(
        f"{API_URL}/router/route",
        json={
            "query": "What does this mean?",
            "student_id": "test_user_006",
            "context": {
                "consecutive_failures": 3,
                "reading_level": 60
            }
        }
    )

    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Routed to: {data['agent'].upper()} Agent")
        print(f"   ✓ Engagement: {data['engagement']} (should detect frustration)")


def test_router_stats():
    """Test router statistics endpoint"""
    print_header("TEST 6: Router Statistics")

    response = requests.get(f"{API_URL}/router/stats")

    if response.status_code == 200:
        data = response.json()
        print("\n📊 Routing Statistics:")
        print_response(data)
    else:
        print(f"✗ Error: {response.status_code}")


def test_query_processing():
    """Test full query processing with routing"""
    print_header("TEST 7: Full Query Processing")

    queries = [
        "Tell me a story about a magical forest",
        "What does 'magical' mean?",
        "Quiz me on the story!"
    ]

    for query in queries:
        print(f"\n📝 Query: \"{query}\"")
        response = requests.post(
            f"{API_URL}/query",
            json={
                "query": query,
                "student_id": "test_user_007"
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"\n   Response:\n{data['response']}\n")
        else:
            print(f"   ✗ Error: {response.status_code}")


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
    print("  STORYFORGE ROUTER AGENT TEST SUITE")
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
        test_story_intent()
        test_comprehension_intent()
        test_vocabulary_intent()
        test_engagement_detection()
        test_context_awareness()
        test_router_stats()
        test_query_processing()

        print_header("[SUCCESS] ALL TESTS COMPLETED")

    except Exception as e:
        print(f"\n[ERROR] Test failed with error: {e}")


if __name__ == "__main__":
    main()
