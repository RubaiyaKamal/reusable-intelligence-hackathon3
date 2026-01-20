#!/bin/bash
# Create Kafka Topics for LearnFlow Application

set -e

echo "📝 Creating Kafka topics for LearnFlow..."

# Wait for Kafka to be ready
echo "⏳ Waiting for Kafka to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kafka -n kafka --timeout=300s

# Topic configuration
PARTITIONS=3
REPLICATION_FACTOR=1  # Use 1 for development, 2+ for production

# List of topics to create
declare -a topics=(
    "learning.query"
    "learning.response"
    "code.submission"
    "code.result"
    "exercise.generated"
    "struggle.alert"
)

# Create each topic
for topic in "${topics[@]}"
do
    echo "Creating topic: $topic"
    kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \
        --create \
        --if-not-exists \
        --topic "$topic" \
        --bootstrap-server localhost:9092 \
        --partitions $PARTITIONS \
        --replication-factor $REPLICATION_FACTOR \
        || echo "  (Topic may already exist)"
done

echo ""
echo "✓ Topics created successfully!"
echo ""
echo "List all topics:"
kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \
    --list \
    --bootstrap-server localhost:9092

echo ""
echo "Describe a topic (example):"
echo "kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \\"
echo "  --describe \\"
echo "  --topic learning.query \\"
echo "  --bootstrap-server localhost:9092"
