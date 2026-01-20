#!/usr/bin/env python3
"""
Stop all Docker Compose services.
"""

import subprocess
import sys

def main():
    print("Stopping all services...")

    result = subprocess.run(
        ["docker-compose", "-f", "docker-compose.production.yml", "down"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✓ All services stopped")
        print("\nTo remove volumes as well, run:")
        print("docker-compose -f docker-compose.production.yml down -v")
        sys.exit(0)
    else:
        print(f"✗ Error stopping services: {result.stderr}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
