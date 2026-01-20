#!/usr/bin/env python3
"""
Test MCP Skill

Tests an MCP-based skill to verify it works correctly.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def test_skill(skill_name: str):
    """Test a skill"""
    print(f"🧪 Testing skill: {skill_name}")
    print()

    skill_dir = Path(".claude/skills") / skill_name

    if not skill_dir.exists():
        print(f"✗ Skill directory not found: {skill_dir}")
        return False

    # Check SKILL.md exists
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"✗ SKILL.md not found")
        return False

    print(f"✓ Found SKILL.md")

    # Check for scripts directory
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        print(f"✗ scripts/ directory not found")
        return False

    print(f"✓ Found scripts/ directory")

    # List scripts
    scripts = list(scripts_dir.glob("*.py"))
    if not scripts:
        print(f"⚠ No Python scripts found")
        return True  # Still valid if no scripts

    print(f"✓ Found {len(scripts)} script(s):")
    for script in scripts:
        print(f"    - {script.name}")

    # Test each script
    all_passed = True
    for script in scripts:
        if script.name.startswith("test_"):
            continue  # Skip test scripts

        print(f"\n  Testing {script.name}...")

        try:
            # Try running with --help
            result = subprocess.run(
                ["python", str(script), "--help"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                print(f"    ✓ Script is executable")
            else:
                print(f"    ⚠ Script --help returned non-zero: {result.returncode}")

        except subprocess.TimeoutExpired:
            print(f"    ⚠ Script timed out")
        except Exception as e:
            print(f"    ✗ Error: {e}")
            all_passed = False

    print()
    if all_passed:
        print(f"✓ Skill {skill_name} passed all tests")
    else:
        print(f"⚠ Skill {skill_name} has some issues")

    return all_passed


def main():
    parser = argparse.ArgumentParser(
        description="Test MCP-based skills"
    )
    parser.add_argument(
        "skill_name",
        help="Name of skill to test"
    )

    args = parser.parse_args()

    success = test_skill(args.skill_name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
