#!/bin/bash
# StoryForge Kafka Topics Creation Script

set -e

echo "📝 Creating Kafka topics for StoryForge..."

NAMESPACE="storyforge"
KAFKA_POD=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=kafka -o jsonpath='{.items[0].metadata.name}')

if [ -z "$KAFKA_POD" ]; then
    echo "❌ Kafka pod not found in namespace $NAMESPACE"
    exit 1
fi

echo "Using Kafka pod: $KAFKA_POD"

# Function to create a topic
create_topic() {
    local TOPIC_NAME=$1
    local PARTITIONS=$2
    local REPLICATION_FACTOR=$3
    local DESCRIPTION=$4

    echo ""
    echo "Creating topic: $TOPIC_NAME"
    echo "  Description: $DESCRIPTION"
    echo "  Partitions: $PARTITIONS, Replication: $REPLICATION_FACTOR"

    kubectl exec -n $NAMESPACE $KAFKA_POD -- kafka-topics.sh \
        --create \
        --if-not-exists \
        --bootstrap-server localhost:9092 \
        --topic $TOPIC_NAME \
        --partitions $PARTITIONS \
        --replication-factor $REPLICATION_FACTOR \
        --config retention.ms=604800000

    echo "✓ Topic $TOPIC_NAME created"
}

# Create StoryForge topics
create_topic "story.generated" 3 1 "Stories created by Story Agent"
create_topic "vocabulary.lookup" 2 1 "Word definitions requested by students"
create_topic "comprehension.question" 2 1 "Comprehension questions and answers"
create_topic "student.progress" 2 1 "Student progress and metrics updates"
create_topic "router.events" 3 1 "Query routing decisions and engagement"
create_topic "agent.metrics" 1 1 "Agent performance metrics"
create_topic "reading.session" 2 1 "Reading session start/end events"
create_topic "engagement.alerts" 1 1 "Alerts for frustrated/confused students"

echo ""
echo "✓ All StoryForge topics created successfully!"
echo ""
echo "To list all topics:"
echo "  kubectl exec -n $NAMESPACE $KAFKA_POD -- kafka-topics.sh --list --bootstrap-server localhost:9092"
echo ""
echo "To describe a topic:"
echo "  kubectl exec -n $NAMESPACE $KAFKA_POD -- kafka-topics.sh --describe --topic story.generated --bootstrap-server localhost:9092"
echo ""
