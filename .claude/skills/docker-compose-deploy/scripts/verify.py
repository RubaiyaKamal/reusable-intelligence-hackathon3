#!/usr/bin/env python3
"""
Verification script for Docker Compose deployment.
Returns minimal status - not full container details.
"""

import subprocess
import json
import sys
from typing import Dict, List

def get_container_status() -> List[Dict]:
    """Get status of all containers."""
    result = subprocess.run(
        ["docker-compose", "-f", "docker-compose.production.yml", "ps", "--format", "json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return []

    # Parse JSON output (one JSON object per line)
    containers = []
    for line in result.stdout.strip().split('\n'):
        if line:
            try:
                containers.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return containers

def check_service_health(service_name: str) -> str:
    """Check health status of a specific service."""
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{.State.Health.Status}}", f"storyforge-{service_name}"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return result.stdout.strip()
    return "no-health-check"

def main():
    containers = get_container_status()

    if not containers:
        print("✗ No containers found. Run deploy.py first.", file=sys.stderr)
        sys.exit(1)

    # Count statuses
    running = sum(1 for c in containers if c.get('State') == 'running')
    total = len(containers)

    # Check key services health
    critical_services = ['postgres', 'kafka', 'backend']
    health_status = {}

    for service in critical_services:
        health = check_service_health(service)
        health_status[service] = health

    # Minimal output for agent context
    print(f"\nContainer Status: {running}/{total} running")

    print("\nCritical Services:")
    for service, health in health_status.items():
        status_icon = "✓" if health in ["healthy", "no-health-check"] else "✗"
        print(f"{status_icon} {service}: {health}")

    if running == total:
        print(f"\n✓ All {total} services are running")
        sys.exit(0)
    else:
        print(f"\n✗ Only {running}/{total} services running")
        print("Run: docker-compose -f docker-compose.production.yml logs")
        sys.exit(1)

if __name__ == "__main__":
    main()
