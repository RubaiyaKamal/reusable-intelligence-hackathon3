#!/usr/bin/env python3
"""
Expose services for local access.
"""

import subprocess
import sys
import argparse

def run_cmd(cmd):
    """Run command."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result

def main():
    parser = argparse.ArgumentParser(description='Expose services')
    parser.add_argument('--namespace', default='storyforge', help='Namespace')
    parser.add_argument('--platform', default='kind', choices=['kind', 'k3s', 'minikube'])
    args = parser.parse_args()

    print(f"Exposing services on {args.platform}")
    print("=" * 60)

    if args.platform == 'minikube':
        # Minikube has built-in service exposure
        print("\nMinikube service URLs:")
        result = run_cmd(f'minikube service list -n {args.namespace}')
        if result.returncode == 0:
            print(result.stdout)

        print("\nTo access a service:")
        print(f"  minikube service storyforge-frontend -n {args.namespace}")
        print(f"  minikube service storyforge-backend -n {args.namespace}")

    elif args.platform == 'kind':
        # Kind uses port forwarding
        print("\nKind requires port forwarding:")
        print("\nFrontend:")
        print(f"  kubectl port-forward -n {args.namespace} svc/storyforge-frontend 3000:3000")
        print("  Access: http://localhost:3000")

        print("\nBackend:")
        print(f"  kubectl port-forward -n {args.namespace} svc/storyforge-backend 8000:8000")
        print("  Access: http://localhost:8000/docs")

        print("\nOr use kubectl proxy:")
        print("  kubectl proxy")
        print(f"  http://localhost:8001/api/v1/namespaces/{args.namespace}/services/storyforge-frontend:3000/proxy/")

    elif args.platform == 'k3s':
        # k3s uses NodePort or LoadBalancer
        print("\nk3s service access:")
        result = run_cmd(f'kubectl get svc -n {args.namespace}')
        if result.returncode == 0:
            print(result.stdout)

        print("\nAccess via NodePort or use port forwarding:")
        print(f"  kubectl port-forward -n {args.namespace} svc/storyforge-frontend 3000:3000")

    return 0

if __name__ == "__main__":
    sys.exit(main())
