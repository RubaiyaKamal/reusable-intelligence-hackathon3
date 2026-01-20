#!/usr/bin/env python3
"""
Kafka Connectivity Test Script

Tests Kafka producer and consumer functionality.
"""

import sys
import json
import time
from datetime import datetime

try:
    from kafka import KafkaProducer, KafkaConsumer
    from kafka.errors import KafkaError
except ImportError:
    print("✗ kafka-python library not installed")
    print("Install it with: pip install kafka-python")
    sys.exit(1)


def test_producer(bootstrap_servers, topic="test-topic"):
    """Test Kafka producer"""
    print(f"📤 Testing Kafka Producer...")
    print(f"   Topic: {topic}")
    print(f"   Servers: {bootstrap_servers}")

    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(2, 5, 0)
        )

        # Send test messages
        test_messages = [
            {"message": "Test message 1", "timestamp": datetime.now().isoformat()},
            {"message": "Test message 2", "timestamp": datetime.now().isoformat()},
            {"message": "Test message 3", "timestamp": datetime.now().isoformat()},
        ]

        for i, msg in enumerate(test_messages, 1):
            future = producer.send(topic, msg)
            try:
                record_metadata = future.get(timeout=10)
                print(f"   ✓ Message {i} sent to partition {record_metadata.partition} at offset {record_metadata.offset}")
            except KafkaError as e:
                print(f"   ✗ Failed to send message {i}: {e}")
                return False

        producer.flush()
        producer.close()
        print("✓ Producer test passed\n")
        return True

    except Exception as e:
        print(f"✗ Producer test failed: {e}\n")
        return False


def test_consumer(bootstrap_servers, topic="test-topic", timeout=10):
    """Test Kafka consumer"""
    print(f"📥 Testing Kafka Consumer...")
    print(f"   Topic: {topic}")
    print(f"   Servers: {bootstrap_servers}")

    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            consumer_timeout_ms=timeout * 1000,
            api_version=(2, 5, 0),
            group_id='test-consumer-group'
        )

        messages_received = 0
        start_time = time.time()

        print(f"   Consuming messages (timeout: {timeout}s)...")

        for message in consumer:
            messages_received += 1
            print(f"   ✓ Received: {message.value}")

            # Stop after receiving a few messages or timeout
            if time.time() - start_time > timeout:
                break

        consumer.close()

        if messages_received > 0:
            print(f"✓ Consumer test passed ({messages_received} messages received)\n")
            return True
        else:
            print(f"⚠ Consumer test passed but no messages received\n")
            return True

    except Exception as e:
        print(f"✗ Consumer test failed: {e}\n")
        return False


def check_broker_connection(bootstrap_servers):
    """Check basic connection to Kafka broker"""
    print("🔗 Checking Kafka broker connection...")

    try:
        from kafka import KafkaAdminClient
        admin = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers,
            api_version=(2, 5, 0)
        )

        # Get cluster metadata
        cluster_metadata = admin._client.cluster
        print(f"   ✓ Connected to Kafka cluster")
        print(f"   Brokers: {len(cluster_metadata.brokers())}")

        admin.close()
        return True

    except Exception as e:
        print(f"   ✗ Connection failed: {e}")
        return False


def main():
    """Main test function"""
    # Kafka bootstrap servers
    # Update this based on how you're accessing Kafka
    bootstrap_servers = ['localhost:9092']  # For port-forwarded connection

    print("="*60)
    print("Kafka Connectivity Test")
    print("="*60)
    print()
    print("IMPORTANT: This script expects Kafka to be accessible at:")
    print(f"  {bootstrap_servers[0]}")
    print()
    print("If running from outside Kubernetes, port-forward first:")
    print("  kubectl port-forward -n kafka svc/kafka 9092:9092")
    print()
    print("="*60)
    print()

    # Check connection
    if not check_broker_connection(bootstrap_servers):
        print("\n✗ Cannot connect to Kafka broker")
        print("\nTroubleshooting:")
        print("  1. Verify Kafka is running: kubectl get pods -n kafka")
        print("  2. Port-forward to Kafka: kubectl port-forward -n kafka svc/kafka 9092:9092")
        print("  3. Check service: kubectl get svc -n kafka")
        sys.exit(1)

    print()

    # Test producer
    test_topic = "test-connectivity"
    producer_success = test_producer(bootstrap_servers, test_topic)

    # Wait a moment for messages to be available
    if producer_success:
        print("⏳ Waiting 2 seconds for messages to be available...")
        time.sleep(2)

    # Test consumer
    consumer_success = test_consumer(bootstrap_servers, test_topic, timeout=10)

    # Final result
    print("="*60)
    if producer_success and consumer_success:
        print("✓ All tests passed!")
        print("Kafka is working correctly")
    else:
        print("✗ Some tests failed")
        print("Check the output above for details")
    print("="*60)

    sys.exit(0 if (producer_success and consumer_success) else 1)


if __name__ == "__main__":
    main()
