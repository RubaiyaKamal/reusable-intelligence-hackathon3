#!/usr/bin/env python3
"""
Health check script for deployed services.
Tests actual connectivity and returns minimal results.
"""

import requests
import sys
import time

def check_endpoint(name: str, url: str, timeout: int = 5) -> bool:
    """Check if an endpoint is responding."""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code < 500:
            print(f"✓ {name}: responding (status {response.status_code})")
            return True
        else:
            print(f"✗ {name}: error (status {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ {name}: unreachable")
        return False

def main():
    print("Running health checks...")
    print("-" * 50)

    # Wait a bit for services to fully start
    time.sleep(5)

    endpoints = {
        "Backend API": "http://localhost:8001/docs",
        "Frontend": "http://localhost:3002",
        "Prometheus": "http://localhost:9090/-/healthy",
        "Grafana": "http://localhost:3000/api/health",
    }

    results = {}
    for name, url in endpoints.items():
        results[name] = check_endpoint(name, url)

    print("-" * 50)

    # Summary (minimal output)
    passing = sum(1 for v in results.values() if v)
    total = len(results)

    if passing == total:
        print(f"\n✓ All {total} health checks passed")
        print("\nAccess URLs:")
        print("- Frontend: http://localhost:3002")
        print("- Backend API: http://localhost:8001/docs")
        print("- Grafana: http://localhost:3000 (admin/admin)")
        print("- Prometheus: http://localhost:9090")
        sys.exit(0)
    else:
        print(f"\n✗ {passing}/{total} health checks passed")
        print("Some services may still be starting. Wait 30s and retry.")
        sys.exit(1)

if __name__ == "__main__":
    main()
