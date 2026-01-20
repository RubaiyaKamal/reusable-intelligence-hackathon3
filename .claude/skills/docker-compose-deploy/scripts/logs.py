#!/usr/bin/env python3
"""
View logs for specific services.
"""

import subprocess
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='View service logs')
    parser.add_argument('--service', default='backend', help='Service name to view logs')
    parser.add_argument('--tail', default='50', help='Number of lines to show')
    parser.add_argument('--follow', '-f', action='store_true', help='Follow log output')
    args = parser.parse_args()

    cmd = f"docker-compose -f docker-compose.production.yml logs --tail={args.tail}"

    if args.follow:
        cmd += " -f"

    cmd += f" {args.service}"

    print(f"Showing logs for {args.service}...")
    print("-" * 50)

    # Execute and stream output
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
