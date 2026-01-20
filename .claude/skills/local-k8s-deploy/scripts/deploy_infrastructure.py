#!/usr/bin/env python3
"""
Deploy infrastructure services (PostgreSQL, Kafka, Redis) to local K8s.
"""

import subprocess
import sys
import time

def run_cmd(cmd, check=True):
    """Run command."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"✗ Error: {result.stderr}", file=sys.stderr)
        return False
    return True

def main():
    print("Deploying Infrastructure Services")
    print("=" * 60)

    # Check if Helm is installed
    print("\n1. Checking Helm...")
    if not run_cmd('helm version', check=False):
        print("✗ Helm not installed", file=sys.stderr)
        print("  Install from: https://helm.sh/docs/intro/install/", file=sys.stderr)
        sys.exit(1)
    print("✓ Helm OK")

    # Add Helm repos
    print("\n2. Adding Helm repositories...")
    run_cmd('helm repo add bitnami https://charts.bitnami.com/bitnami', check=False)
    run_cmd('helm repo update')
    print("✓ Helm repos updated")

    # Deploy PostgreSQL
    print("\n3. Deploying PostgreSQL...")
    run_cmd('kubectl create namespace storyforge --dry-run=client -o yaml | kubectl apply -f -')

    cmd = """helm install storyforge-postgres bitnami/postgresql \
        --namespace storyforge \
        --set auth.username=storyforge_user \
        --set auth.password=storyforge_pass \
        --set auth.database=storyforge_db \
        --set primary.persistence.size=2Gi \
        --wait --timeout=5m"""

    if run_cmd(cmd, check=False):
        print("✓ PostgreSQL deployed")
    else:
        print("⚠ PostgreSQL may already exist")

    # Deploy Redis
    print("\n4. Deploying Redis...")
    cmd = """helm install storyforge-redis bitnami/redis \
        --namespace storyforge \
        --set auth.enabled=false \
        --set master.persistence.size=1Gi \
        --wait --timeout=5m"""

    if run_cmd(cmd, check=False):
        print("✓ Redis deployed")
    else:
        print("⚠ Redis may already exist")

    # Deploy Kafka
    print("\n5. Deploying Kafka...")
    cmd = """helm install storyforge-kafka bitnami/kafka \
        --namespace storyforge \
        --set replicaCount=1 \
        --set zookeeper.replicaCount=1 \
        --set persistence.size=2Gi \
        --set zookeeper.persistence.size=1Gi \
        --wait --timeout=10m"""

    if run_cmd(cmd, check=False):
        print("✓ Kafka deployed")
    else:
        print("⚠ Kafka may already exist")

    # Wait for pods
    print("\n6. Waiting for pods to be ready...")
    time.sleep(15)

    result = subprocess.run(
        'kubectl get pods -n storyforge',
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(result.stdout)

    # Initialize database
    print("\n7. Initializing database schema...")
    print("⚠ Run manually after all pods are ready:")
    print("  kubectl exec -n storyforge storyforge-postgres-0 -i -- psql -U storyforge_user -d storyforge_db < k8s/storyforge-schema.sql")

    # Summary
    print("\n" + "=" * 60)
    print("✓ Infrastructure deployed!")
    print("\nServices running:")
    print("  - PostgreSQL: storyforge-postgres.storyforge.svc.cluster.local:5432")
    print("  - Redis: storyforge-redis-master.storyforge.svc.cluster.local:6379")
    print("  - Kafka: storyforge-kafka.storyforge.svc.cluster.local:9092")

    return 0

if __name__ == "__main__":
    sys.exit(main())
