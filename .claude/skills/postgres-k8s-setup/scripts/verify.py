#!/usr/bin/env python3
"""
PostgreSQL Deployment Verification Script
"""

import subprocess
import json
import sys
import time


def run_kubectl(args):
    """Run kubectl command"""
    try:
        result = subprocess.run(
            ["kubectl"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout) if result.stdout else None
    except subprocess.CalledProcessError as e:
        print(f"✗ kubectl error: {e.stderr}", file=sys.stderr)
        return None


def verify_namespace():
    """Check if postgres namespace exists"""
    print("🔍 Checking postgres namespace...")
    result = run_kubectl(["get", "namespace", "postgres", "-o", "json"])
    if result:
        print("  ✓ Namespace exists")
        return True
    print("  ✗ Namespace not found")
    return False


def verify_pod():
    """Check PostgreSQL pod status"""
    print("\n🔍 Checking PostgreSQL pod...")
    pods = run_kubectl(["get", "pods", "-n", "postgres", "-o", "json"])

    if not pods or not pods.get("items"):
        print("  ✗ No pods found")
        return False

    postgres_pod = None
    for pod in pods["items"]:
        if "postgresql" in pod["metadata"]["name"]:
            postgres_pod = pod
            break

    if not postgres_pod:
        print("  ✗ PostgreSQL pod not found")
        return False

    name = postgres_pod["metadata"]["name"]
    phase = postgres_pod["status"]["phase"]

    if phase == "Running":
        # Check if ready
        conditions = postgres_pod["status"].get("conditions", [])
        ready = any(c["type"] == "Ready" and c["status"] == "True" for c in conditions)

        if ready:
            print(f"  ✓ Pod {name} is Running and Ready")
            return True
        else:
            print(f"  ⚠ Pod {name} is Running but not Ready")
            return False
    else:
        print(f"  ✗ Pod {name} is {phase}")
        return False


def verify_pvc():
    """Check PersistentVolumeClaim status"""
    print("\n🔍 Checking PersistentVolumeClaim...")
    pvcs = run_kubectl(["get", "pvc", "-n", "postgres", "-o", "json"])

    if not pvcs or not pvcs.get("items"):
        print("  ✗ No PVCs found")
        return False

    for pvc in pvcs["items"]:
        name = pvc["metadata"]["name"]
        phase = pvc["status"]["phase"]

        if phase == "Bound":
            size = pvc["spec"]["resources"]["requests"]["storage"]
            print(f"  ✓ PVC {name} is Bound ({size})")
            return True
        else:
            print(f"  ✗ PVC {name} is {phase}")
            return False

    return False


def verify_service():
    """Check PostgreSQL service"""
    print("\n🔍 Checking PostgreSQL service...")
    svc = run_kubectl(["get", "service", "postgres-postgresql", "-n", "postgres", "-o", "json"])

    if not svc:
        print("  ✗ Service not found")
        return False

    cluster_ip = svc["spec"].get("clusterIP", "None")
    ports = svc["spec"].get("ports", [])

    if ports:
        port = ports[0]["port"]
        print(f"  ✓ Service exists: {cluster_ip}:{port}")
        return True

    print("  ✗ Service has no ports")
    return False


def verify_secret():
    """Check if credentials secret exists"""
    print("\n🔍 Checking credentials secret...")
    secret = run_kubectl(["get", "secret", "postgres-credentials", "-n", "postgres", "-o", "json"])

    if secret:
        print("  ✓ Credentials secret exists")
        return True

    print("  ✗ Credentials secret not found")
    return False


def main():
    """Main verification"""
    print("="*60)
    print("PostgreSQL Deployment Verification")
    print("="*60)

    checks = [
        ("Namespace", verify_namespace()),
        ("Pod", verify_pod()),
        ("PersistentVolumeClaim", verify_pvc()),
        ("Service", verify_service()),
        ("Secret", verify_secret())
    ]

    print("\n" + "="*60)
    print("Summary:")
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")

    all_passed = all(result for _, result in checks)

    if all_passed:
        print("\n✓ All checks passed!")
        print("\nPostgreSQL is accessible at:")
        print("  postgres-postgresql.postgres.svc.cluster.local:5432")
        print("\nDatabase: learnflow")
        print("Username: learnflow_user")
        print("\nGet password:")
        print("  kubectl get secret postgres-credentials -n postgres -o jsonpath='{.data.password}' | base64 --decode")
        sys.exit(0)
    else:
        print("\n✗ Some checks failed")
        print("\nTroubleshooting:")
        print("  kubectl describe pod <pod-name> -n postgres")
        print("  kubectl logs <pod-name> -n postgres")
        print("  kubectl get events -n postgres")
        sys.exit(1)


if __name__ == "__main__":
    main()
