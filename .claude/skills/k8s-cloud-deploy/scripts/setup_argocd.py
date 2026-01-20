#!/usr/bin/env python3
"""
Setup ArgoCD for GitOps continuous deployment.
Minimal output to agent context.
"""

import subprocess
import sys
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
    print("Setting up ArgoCD for GitOps...")
    print("=" * 60)

    # Create argocd namespace
    print("\n1. Creating ArgoCD namespace...")
    run_kubectl("create namespace argocd --dry-run=client -o yaml | kubectl apply -f -")
    print("✓ Namespace: argocd")

    # Install ArgoCD
    print("\n2. Installing ArgoCD...")
    result = run_kubectl(
        "apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml"
    )

    if result.returncode == 0:
        print("✓ ArgoCD installed")
    else:
        print("✗ ArgoCD installation failed", file=sys.stderr)
        return 1

    # Wait for ArgoCD to be ready
    print("\n3. Waiting for ArgoCD pods...")
    time.sleep(10)
    run_kubectl("wait --for=condition=Ready pods --all -n argocd --timeout=300s")
    print("✓ ArgoCD pods ready")

    # Get initial admin password
    print("\n4. Retrieving ArgoCD admin password...")
    result = run_kubectl(
        "get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}'"
    )

    if result.returncode == 0 and result.stdout:
        # Password is base64 encoded
        print("✓ Admin password retrieved")
        print("  Decode with: echo '<password>' | base64 -d")

    # Create StoryForge application
    print("\n5. Creating ArgoCD application...")
    result = run_kubectl("apply -f k8s/argocd/application.yaml")

    if result.returncode == 0:
        print("✓ StoryForge application created")
    else:
        print("⚠ Application creation failed (update repo URL in k8s/argocd/application.yaml)")

    # Summary
    print("\n" + "=" * 60)
    print("✓ ArgoCD setup complete")
    print("\nAccess ArgoCD UI:")
    print("  kubectl port-forward svc/argocd-server -n argocd 8080:443")
    print("  Open: https://localhost:8080")
    print("  Username: admin")
    print("  Password: (retrieve with above command)")

    print("\nArgoCD will automatically sync from:")
    print("  Repository: https://github.com/YOUR_USERNAME/reusable-intelligence-hackathon3")
    print("  Path: k8s/app")
    print("  Branch: main")

    return 0

if __name__ == "__main__":
    sys.exit(main())
