#!/usr/bin/env python3
"""
Local Kubernetes deployment script using MCP Code Execution pattern.
Supports Kind, k3s, and Minikube.
"""

import subprocess
import sys
import argparse
import time

PLATFORMS = {
    'kind': {
        'check_cmd': 'kind version',
        'install_url': 'https://kind.sigs.k8s.io/docs/user/quick-start/#installation',
        'description': 'Kubernetes in Docker'
    },
    'k3s': {
        'check_cmd': 'k3s --version',
        'install_url': 'https://k3s.io/',
        'description': 'Lightweight Kubernetes'
    },
    'minikube': {
        'check_cmd': 'minikube version',
        'install_url': 'https://minikube.sigs.k8s.io/docs/start/',
        'description': 'Full Kubernetes locally'
    }
}

def run_cmd(cmd, check=True):
    """Run command and return result."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"[ERROR] {result.stderr}", file=sys.stderr)
        return None
    return result

def check_prerequisites(platform):
    """Check if platform is installed."""
    platform_config = PLATFORMS[platform]

    # Check Docker for Kind
    if platform == 'kind':
        result = run_cmd('docker --version', check=False)
        if result.returncode != 0:
            print("[ERROR] Docker not running", file=sys.stderr)
            print("  Start Docker Desktop first", file=sys.stderr)
            return False

    # Check platform
    result = run_cmd(platform_config['check_cmd'], check=False)
    if result.returncode != 0:
        print(f"[ERROR] {platform} not installed", file=sys.stderr)
        print(f"  Install from: {platform_config['install_url']}", file=sys.stderr)
        return False

    # Check kubectl
    result = run_cmd('kubectl version --client', check=False)
    if result.returncode != 0:
        print("[ERROR] kubectl not installed", file=sys.stderr)
        return False

    print(f"[OK] Prerequisites OK for {platform}")
    return True

def deploy_kind(cluster_name):
    """Deploy Kind cluster."""
    print(f"\nDeploying Kind cluster: {cluster_name}")

    # Create config file
    config = f"""
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: {cluster_name}
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 8080
    protocol: TCP
  - containerPort: 443
    hostPort: 8443
    protocol: TCP
"""

    with open('kind-config.yaml', 'w') as f:
        f.write(config)

    # Create cluster
    result = run_cmd(f'kind create cluster --name {cluster_name} --config kind-config.yaml')
    if result is None:
        return False

    print(f"[OK] Kind cluster created: {cluster_name}")

    # Wait for cluster to be ready
    print("Waiting for cluster to be ready...")
    time.sleep(10)

    return True

def deploy_k3s(cluster_name):
    """Deploy k3s cluster."""
    print(f"\nDeploying k3s cluster: {cluster_name}")

    # Install k3s
    if sys.platform.startswith('linux'):
        cmd = "curl -sfL https://get.k3s.io | sh -"
        result = run_cmd(cmd)
        if result is None:
            return False

        # Configure kubectl
        run_cmd('sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config', check=False)
        run_cmd('sudo chown $USER ~/.kube/config', check=False)

        print(f"[OK] k3s cluster created: {cluster_name}")
        return True
    else:
        print("[WARNING] k3s is primarily for Linux", file=sys.stderr)
        print("  On Windows/Mac, use Kind or Minikube instead", file=sys.stderr)
        return False

def deploy_minikube(cluster_name, memory, cpus):
    """Deploy Minikube cluster."""
    print(f"\nDeploying Minikube cluster: {cluster_name}")

    # Delete existing cluster if any
    run_cmd('minikube delete', check=False)

    # Create cluster
    cmd = f'minikube start --profile {cluster_name} --memory={memory} --cpus={cpus} --driver=docker'
    result = run_cmd(cmd)
    if result is None:
        return False

    print(f"[OK] Minikube cluster created: {cluster_name}")

    # Enable addons
    print("Enabling addons...")
    run_cmd(f'minikube addons enable ingress --profile {cluster_name}')
    run_cmd(f'minikube addons enable metrics-server --profile {cluster_name}')

    return True

def main():
    parser = argparse.ArgumentParser(description='Deploy local Kubernetes')
    parser.add_argument('--platform', required=True, choices=PLATFORMS.keys(),
                       help='Platform to use')
    parser.add_argument('--cluster-name', default='storyforge-local',
                       help='Cluster name')
    parser.add_argument('--memory', type=int, default=3072,
                       help='Memory in MB (Minikube only)')
    parser.add_argument('--cpus', type=int, default=2,
                       help='Number of CPUs (Minikube only)')

    args = parser.parse_args()

    print(f"\n{PLATFORMS[args.platform]['description']}")
    print("=" * 60)

    # Check prerequisites
    if not check_prerequisites(args.platform):
        sys.exit(1)

    # Deploy based on platform
    success = False
    if args.platform == 'kind':
        success = deploy_kind(args.cluster_name)
    elif args.platform == 'k3s':
        success = deploy_k3s(args.cluster_name)
    elif args.platform == 'minikube':
        success = deploy_minikube(args.cluster_name, args.memory, args.cpus)

    if success:
        # Verify kubectl
        print("\nVerifying kubectl configuration...")
        result = run_cmd('kubectl cluster-info')

        print("\n" + "=" * 60)
        print(f"[OK] {args.platform} cluster ready!")
        print("\nNext steps:")
        print("1. python scripts/deploy_infrastructure.py")
        print("2. python scripts/deploy_app.py")
        print("3. python scripts/verify.py")
        sys.exit(0)
    else:
        print("\n[ERROR] Deployment failed", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
