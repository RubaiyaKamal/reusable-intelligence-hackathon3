#!/usr/bin/env python3
"""Create Assignment - Assignment Creator"""
import argparse, json, sys, requests, os
from datetime import datetime

API_URL = os.getenv("API_URL", "http://localhost:8001")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--teacher-id", required=True)
    parser.add_argument("--type", required=True, choices=["reading", "quiz", "writing", "custom"])
    parser.add_argument("--title", required=True)
    parser.add_argument("--due-date", required=True)
    parser.add_argument("--points", type=int, default=10)
    parser.add_argument("--instructions", default="")
    args = parser.parse_args()

    assignment_id = f"ASGN-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    assignment = {
        "id": assignment_id,
        "teacher_id": args.teacher_id,
        "type": args.type,
        "title": args.title,
        "due_date": args.due_date,
        "points": args.points,
        "instructions": args.instructions,
        "status": "draft",
        "created_at": datetime.now().isoformat()
    }

    with open("assignments.json", 'a') as f:
        json.dump(assignment, f)
        f.write('\n')

    print(f"✓ Assignment created (ID: {assignment_id})")
    print(f"  Type: {args.type}")
    print(f"  Title: {args.title}")
    print(f"  Due: {args.due_date}")
    print(f"  Points: {args.points}")
    print(f"  Status: Draft (use assign_to_students.py to activate)")

if __name__ == "__main__":
    main()
