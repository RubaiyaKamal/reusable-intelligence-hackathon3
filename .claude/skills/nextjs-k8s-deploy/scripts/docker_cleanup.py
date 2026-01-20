#!/usr/bin/env python3
"""
Docker Cleanup Utility

Helps manage Docker Desktop memory and disk space issues.
"""

import subprocess
import sys
import argparse


def run_command(cmd: list, description: str) -> tuple:
    """Run a command and return result"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_docker_info():
    """Get Docker disk usage information"""
    print("📊 Docker Disk Usage:")
    print()

    success, stdout, stderr = run_command(
        ["docker", "system", "df"],
        "Getting disk usage"
    )

    if success:
        print(stdout)
    else:
        print(f"✗ Failed to get disk usage: {stderr}")


def list_large_images():
    """List images sorted by size"""
    print("\n📦 Largest Docker Images:")
    print()

    success, stdout, stderr = run_command(
        ["docker", "images", "--format", "table {{.Repository}}:{{.Tag}}\t{{.Size}}", "--filter", "dangling=false"],
        "Listing images"
    )

    if success:
        lines = stdout.strip().split('\n')
        if len(lines) > 1:
            print(lines[0])  # Header
            for line in sorted(lines[1:], key=lambda x: x.split()[-1], reverse=True)[:10]:
                print(line)
        else:
            print("No images found")
    else:
        print(f"✗ Failed: {stderr}")


def list_stopped_containers():
    """List stopped containers"""
    print("\n🔴 Stopped Containers:")
    print()

    success, stdout, stderr = run_command(
        ["docker", "ps", "-a", "--filter", "status=exited", "--format", "table {{.Names}}\t{{.Image}}\t{{.Status}}"],
        "Listing stopped containers"
    )

    if success:
        lines = stdout.strip().split('\n')
        if len(lines) > 1:
            print(stdout)
            return len(lines) - 1
        else:
            print("No stopped containers")
            return 0
    else:
        print(f"✗ Failed: {stderr}")
        return 0


def list_dangling_images():
    """List dangling images"""
    print("\n🗑️  Dangling Images (unused layers):")
    print()

    success, stdout, stderr = run_command(
        ["docker", "images", "-f", "dangling=true", "--format", "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}"],
        "Listing dangling images"
    )

    if success:
        lines = stdout.strip().split('\n')
        if len(lines) > 1:
            print(stdout)
            return len(lines) - 1
        else:
            print("No dangling images")
            return 0
    else:
        print(f"✗ Failed: {stderr}")
        return 0


def cleanup_stopped_containers():
    """Remove stopped containers"""
    print("\n🧹 Removing stopped containers...")

    success, stdout, stderr = run_command(
        ["docker", "container", "prune", "-f"],
        "Removing stopped containers"
    )

    if success:
        print("✓ Stopped containers removed")
        if stdout:
            print(stdout)
    else:
        print(f"✗ Failed: {stderr}")


def cleanup_dangling_images():
    """Remove dangling images"""
    print("\n🧹 Removing dangling images...")

    success, stdout, stderr = run_command(
        ["docker", "image", "prune", "-f"],
        "Removing dangling images"
    )

    if success:
        print("✓ Dangling images removed")
        if stdout:
            print(stdout)
    else:
        print(f"✗ Failed: {stderr}")


def cleanup_unused_volumes():
    """Remove unused volumes"""
    print("\n🧹 Removing unused volumes...")

    success, stdout, stderr = run_command(
        ["docker", "volume", "prune", "-f"],
        "Removing unused volumes"
    )

    if success:
        print("✓ Unused volumes removed")
        if stdout:
            print(stdout)
    else:
        print(f"✗ Failed: {stderr}")


def cleanup_build_cache():
    """Remove build cache"""
    print("\n🧹 Removing build cache...")

    success, stdout, stderr = run_command(
        ["docker", "builder", "prune", "-f"],
        "Removing build cache"
    )

    if success:
        print("✓ Build cache removed")
        if stdout:
            print(stdout)
    else:
        print(f"✗ Failed: {stderr}")


def full_cleanup(aggressive: bool = False):
    """Perform full cleanup"""
    print("🚀 Starting Docker cleanup...")
    print()

    # Basic cleanup
    cleanup_stopped_containers()
    cleanup_dangling_images()
    cleanup_unused_volumes()
    cleanup_build_cache()

    if aggressive:
        print("\n⚠️  Aggressive cleanup: Removing ALL unused images...")
        success, stdout, stderr = run_command(
            ["docker", "image", "prune", "-a", "-f"],
            "Removing all unused images"
        )

        if success:
            print("✓ All unused images removed")
            if stdout:
                print(stdout)
        else:
            print(f"✗ Failed: {stderr}")

    print("\n✓ Cleanup complete!")


def optimize_docker_desktop():
    """Provide optimization tips for Docker Desktop"""
    print("\n💡 Docker Desktop Optimization Tips:")
    print()
    print("1. Reduce Memory Allocation:")
    print("   Docker Desktop → Settings → Resources → Memory")
    print("   Recommended: 4GB (adjust based on your needs)")
    print()
    print("2. Reduce Disk Size:")
    print("   Docker Desktop → Settings → Resources → Disk image size")
    print("   Clean up regularly to reclaim space")
    print()
    print("3. Enable Resource Saver:")
    print("   Docker Desktop → Settings → General → Resource Saver")
    print("   Pauses Docker when not in use")
    print()
    print("4. Use .dockerignore:")
    print("   Prevents copying unnecessary files to images")
    print()
    print("5. Multi-stage Builds:")
    print("   Reduces final image size significantly")
    print()
    print("6. Regular Cleanup:")
    print("   Run: make prune (or python docker_cleanup.py --cleanup)")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Docker Desktop cleanup and optimization utility"
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show Docker disk usage information"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List resources that can be cleaned"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Perform cleanup (removes stopped containers, dangling images, etc.)"
    )
    parser.add_argument(
        "--aggressive",
        action="store_true",
        help="Aggressive cleanup (removes ALL unused images)"
    )
    parser.add_argument(
        "--optimize-tips",
        action="store_true",
        help="Show Docker Desktop optimization tips"
    )

    args = parser.parse_args()

    # If no arguments, show info and list
    if not any(vars(args).values()):
        get_docker_info()
        list_large_images()
        list_stopped_containers()
        list_dangling_images()
        print("\n💡 Tip: Use --cleanup to remove unused resources")
        print("        Use --optimize-tips for optimization guidance")
        return

    try:
        if args.info:
            get_docker_info()

        if args.list:
            list_large_images()
            stopped = list_stopped_containers()
            dangling = list_dangling_images()
            print(f"\n📊 Summary:")
            print(f"  Stopped containers: {stopped}")
            print(f"  Dangling images: {dangling}")

        if args.cleanup:
            full_cleanup(args.aggressive)
            print("\n📊 After cleanup:")
            get_docker_info()

        if args.optimize_tips:
            optimize_docker_desktop()

    except KeyboardInterrupt:
        print("\n\n⚠️  Cleanup interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
