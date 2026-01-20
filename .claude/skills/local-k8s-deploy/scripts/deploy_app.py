#!/usr/bin/env python3
"""
Deploy StoryForge application to local Kubernetes.
"""

import subprocess
import sys
import argparse
import time

def run_kubectl(cmd):
    """Run kubectl command."""
    result = subprocess.run(
        f"kubectl {cmd}",
        shell=True,
        capture_output=True,
        text=True
    )
    return result

def main():
    parser = argparse.ArgumentParser(description='Deploy app to local K8s')
    parser.add_argument('--namespace', default='storyforge', help='Namespace')
    args = parser.parse_args()

    print(f"Deploying StoryForge to {args.namespace}")
    print("=" * 60)

    # Create namespace
    print("\n1. Creating namespace...")
    run_kubectl(f"create namespace {args.namespace} --dry-run=client -o yaml | kubectl apply -f -")
    print(f"✓ Namespace: {args.namespace}")

    # Create secrets
    print("\n2. Creating secrets...")
    import os
    openai_key = os.getenv('OPENAI_API_KEY', 'your-key-here')

    result = run_kubectl(f"get secret storyforge-secrets -n {args.namespace}")
    if result.returncode != 0:
        # Create secret
        cmd = f"""create secret generic storyforge-secrets \
            --from-literal=openai-api-key={openai_key} \
            --from-literal=database-url=postgresql://storyforge_user:storyforge_pass@storyforge-postgres.{args.namespace}.svc.cluster.local:5432/storyforge_db \
            --from-literal=postgres-password=storyforge_pass \
            -n {args.namespace}"""
        run_kubectl(cmd)
        print("✓ Secrets created")
    else:
        print("✓ Secrets already exist")

    # Apply ConfigMap
    print("\n3. Applying configuration...")
    run_kubectl(f"apply -f k8s/app/configmap.yaml -n {args.namespace}")
    print("✓ ConfigMap applied")

    # Update image registry for local
    print("\n4. Preparing manifests for local deployment...")
    # For local, we'll use the images we already built
    import re

    for manifest in ['backend-deployment.yaml', 'frontend-deployment.yaml']:
        with open(f'k8s/app/{manifest}', 'r') as f:
            content = f.read()

        # Replace registry placeholder with local images
        content = re.sub(
            r'\${DOCKER_REGISTRY}/storyforge-(\w+):\${IMAGE_TAG}',
            r'reusable-intelligence-hackathon3-\1:latest',
            content
        )

        # Write temporary file
        with open(f'k8s/app/{manifest}.local', 'w') as f:
            f.write(content)

    # Deploy backend
    print("\n5. Deploying backend...")
    run_kubectl(f"apply -f k8s/app/backend-deployment.yaml.local -n {args.namespace}")
    print("✓ Backend deployment created")

    # Deploy frontend
    print("\n6. Deploying frontend...")
    run_kubectl(f"apply -f k8s/app/frontend-deployment.yaml.local -n {args.namespace}")
    print("✓ Frontend deployment created")

    # Wait for pods
    print("\n7. Waiting for pods to start...")
    time.sleep(10)

    result = run_kubectl(f"get pods -n {args.namespace}")
    if result.returncode == 0:
        print(result.stdout)

    # Summary
    print("\n" + "=" * 60)
    print("✓ Application deployed!")
    print(f"\nCheck status:")
    print(f"  kubectl get pods -n {args.namespace}")
    print(f"  kubectl get svc -n {args.namespace}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
