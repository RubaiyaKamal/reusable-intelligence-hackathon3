#!/usr/bin/env python3
"""
Kafka Deployment Verification Script

Verifies that Kafka and ZooKeeper pods are running and healthy.
"""

import subprocess
import json
import sys
import time


def run_kubectl_command(args):
    """Run kubectl command and return parsed JSON output"""
    try:
        result = subprocess.run(
            ["kubectl"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"✗ kubectl command failed: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Failed to parse kubectl output: {e}", file=sys.stderr)
        sys.exit(1)


def get_pods(namespace="kafka"):
    """Get all pods in the kafka namespace"""
    return run_kubectl_command(["get", "pods", "-n", namespace, "-o", "json"])


def check_pod_status(pod):
    """Check if a pod is running and ready"""
    phase = pod["status"]["phase"]
    conditions = pod["status"].get("conditions", [])

    ready = False
    for condition in conditions:
        if condition["type"] == "Ready" and condition["status"] == "True":
            ready = True
            break

    return phase == "Running" and ready


def verify_kafka_deployment():
    """Verify Kafka deployment status"""
    print("🔍 Verifying Kafka deployment...\n")

    # Get all pods
    pods_data = get_pods()
    pods = pods_data["items"]

    if not pods:
        print("✗ No pods found in kafka namespace")
        return False

    # Categorize pods
    kafka_pods = [p for p in pods if "kafka-" in p["metadata"]["name"] and "zookeeper" not in p["metadata"]["name"]]
    zookeeper_pods = [p for p in pods if "zookeeper" in p["metadata"]["name"]]

    # Check Kafka pods
    kafka_running = 0
    kafka_total = len(kafka_pods)

    print(f"Kafka Brokers ({kafka_total} pods):")
    for pod in kafka_pods:
        name = pod["metadata"]["name"]
        is_ready = check_pod_status(pod)

        if is_ready:
            kafka_running += 1
            print(f"  ✓ {name}: Running")
        else:
            phase = pod["status"]["phase"]
            print(f"  ✗ {name}: {phase}")

    # Check ZooKeeper pods
    zk_running = 0
    zk_total = len(zookeeper_pods)

    print(f"\nZooKeeper ({zk_total} pods):")
    for pod in zookeeper_pods:
        name = pod["metadata"]["name"]
        is_ready = check_pod_status(pod)

        if is_ready:
            zk_running += 1
            print(f"  ✓ {name}: Running")
        else:
            phase = pod["status"]["phase"]
            print(f"  ✗ {name}: {phase}")

    # Summary
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Kafka:     {kafka_running}/{kafka_total} running")
    print(f"  ZooKeeper: {zk_running}/{zk_total} running")
    print(f"{'='*50}\n")

    # Check if all pods are ready
    all_ready = (kafka_running == kafka_total) and (zk_running == zk_total)

    if all_ready:
        print("✓ All pods are running and ready!")
        print("\nKafka is accessible at:")
        print("  kafka.kafka.svc.cluster.local:9092")
        return True
    else:
        print("✗ Some pods are not ready yet")
        print("\nTroubleshooting:")
        print("  1. Check pod logs: kubectl logs <pod-name> -n kafka")
        print("  2. Describe pod: kubectl describe pod <pod-name> -n kafka")
        print("  3. Check events: kubectl get events -n kafka --sort-by='.lastTimestamp'")
        return False


def check_kafka_service():
    """Verify Kafka service exists and has endpoints"""
    try:
        service = run_kubectl_command(["get", "service", "kafka", "-n", "kafka", "-o", "json"])
        endpoints = run_kubectl_command(["get", "endpoints", "kafka", "-n", "kafka", "-o", "json"])

        service_type = service["spec"]["type"]
        cluster_ip = service["spec"].get("clusterIP", "None")

        print(f"\nKafka Service:")
        print(f"  Type: {service_type}")
        print(f"  ClusterIP: {cluster_ip}")

        # Check if endpoints exist
        subsets = endpoints.get("subsets", [])
        if subsets and subsets[0].get("addresses"):
            endpoint_count = len(subsets[0]["addresses"])
            print(f"  Endpoints: {endpoint_count} ready")
            return True
        else:
            print(f"  Endpoints: None ready")
            return False

    except subprocess.CalledProcessError:
        print("✗ Kafka service not found")
        return False


def main():
    """Main verification function"""
    try:
        # Check namespace exists
        try:
            run_kubectl_command(["get", "namespace", "kafka", "-o", "json"])
        except subprocess.CalledProcessError:
            print("✗ Namespace 'kafka' not found")
            print("Run deployment first: ./scripts/deploy.sh")
            sys.exit(1)

        # Verify pods
        pods_ready = verify_kafka_deployment()

        # Verify service
        service_ready = check_kafka_service()

        # Final status
        if pods_ready and service_ready:
            print("\n" + "="*50)
            print("✓ Kafka deployment verified successfully!")
            print("="*50)
            sys.exit(0)
        else:
            print("\n" + "="*50)
            print("✗ Kafka deployment verification failed")
            print("="*50)
            sys.exit(1)

    except Exception as e:
        print(f"✗ Verification error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
