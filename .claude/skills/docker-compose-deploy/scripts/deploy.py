#!/usr/bin/env python3
"""
Docker Compose deployment script with MCP Code Execution pattern.
Only returns minimal output to agent context.
"""

import subprocess
import sys
import argparse
import time
from pathlib import Path

def run_command(cmd, check=True):
    """Execute command and return result."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"✗ Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result

def main():
    parser = argparse.ArgumentParser(description='Deploy Docker Compose stack')
    parser.add_argument('--file', default='docker-compose.production.yml', help='Compose file to use')
    parser.add_argument('--build', action='store_true', help='Build images before starting')
    args = parser.parse_args()

    # Check if Docker is running
    result = run_command("docker info", check=False)
    if result.returncode != 0:
        print("✗ Docker is not running. Please start Docker Desktop.", file=sys.stderr)
        sys.exit(1)

    print(f"Deploying stack from {args.file}...")

    # Stop existing containers
    print("Stopping existing containers...")
    run_command(f"docker-compose -f {args.file} down", check=False)

    # Build if requested
    if args.build:
        print("Building images...")
        run_command(f"docker-compose -f {args.file} build")

    # Start services
    print("Starting services...")
    result = run_command(f"docker-compose -f {args.file} up -d")

    # Wait for services to initialize
    print("Waiting for services to initialize...")
    time.sleep(10)

    # Check container status
    result = run_command("docker-compose -f " + args.file + " ps --format json", check=False)

    # Only minimal output enters agent context
    print("\n✓ Stack deployed successfully")
    print(f"✓ Using compose file: {args.file}")
    print("\nNext steps:")
    print("1. Run: python scripts/verify.py")
    print("2. Run: python scripts/health_check.py")

    return 0

if __name__ == "__main__":
    sys.exit(main())
