# Kafka Kubernetes Setup - Reference Documentation

## Apache Kafka Overview

Apache Kafka is a distributed event streaming platform designed for high-throughput, fault-tolerant publish-subscribe messaging. It's ideal for building real-time data pipelines and event-driven microservices.

## Architecture on Kubernetes

```
┌─────────────────────────────────────────────────┐
│           Kubernetes Cluster                    │
│  ┌────────────────────────────────────────────┐ │
│  │  Namespace: kafka                          │ │
│  │                                            │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │ │
│  │  │  Kafka   │  │  Kafka   │  │  Kafka   │ │ │
│  │  │ Broker 0 │  │ Broker 1 │  │ Broker 2 │ │ │
│  │  └─────┬────┘  └─────┬────┘  └─────┬────┘ │ │
│  │        │             │             │       │ │
│  │        └─────────────┼─────────────┘       │ │
│  │                      │                     │ │
│  │  ┌──────────┐  ┌─────┴────┐  ┌──────────┐ │ │
│  │  │ZooKeeper │  │ZooKeeper │  │ZooKeeper │ │ │
│  │  │    0     │  │    1     │  │    2     │ │ │
│  │  └──────────┘  └──────────┘  └──────────┘ │ │
│  │                                            │ │
│  │  ┌──────────────────────────────────────┐ │ │
│  │  │  Persistent Volumes (8Gi each)       │ │ │
│  │  └──────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

## Bitnami Helm Chart

The Bitnami Kafka Helm chart provides:
- **Production-ready defaults**: Optimized for reliability
- **StatefulSets**: For stable pod identities and persistent storage
- **ZooKeeper bundled**: Coordination service included
- **Easy configuration**: Values-based customization
- **Security features**: SASL, TLS support

## Deployment Parameters

### Development Configuration (Single Node)
```yaml
replicaCount: 1
zookeeper:
  replicaCount: 1
persistence:
  size: 8Gi
resources:
  requests:
    memory: 2Gi
    cpu: 500m
  limits:
    memory: 4Gi
    cpu: 2000m
```

### Production Configuration (Multi-Node)
```yaml
replicaCount: 3
zookeeper:
  replicaCount: 3
persistence:
  size: 100Gi
  storageClass: fast-ssd
resources:
  requests:
    memory: 8Gi
    cpu: 2000m
  limits:
    memory: 16Gi
    cpu: 4000m
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - topologyKey: kubernetes.io/hostname
```

## Kafka Topics for LearnFlow

The LearnFlow application uses these Kafka topics:

| Topic | Purpose | Producers | Consumers |
|-------|---------|-----------|-----------|
| `learning.query` | Student questions | Frontend | Triage Service |
| `learning.response` | AI tutor responses | Tutor Services | Frontend |
| `code.submission` | Code submissions | Frontend | Code Review Agent |
| `code.result` | Execution results | Sandbox | Frontend |
| `exercise.generated` | New exercises | Exercise Agent | Frontend |
| `struggle.alert` | Student difficulties | Progress Agent | Teacher Dashboard |

## Connection Details

### From Within Kubernetes
```bash
# Service DNS name
kafka.kafka.svc.cluster.local:9092

# From same namespace
kafka:9092
```

### From External (Development Only)
```bash
# Port forward to localhost
kubectl port-forward -n kafka svc/kafka 9092:9092

# Connect via localhost
localhost:9092
```

## Topic Management

### Create Topic
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \
  --create \
  --topic learning.query \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 2
```

### List Topics
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092
```

### Describe Topic
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \
  --describe \
  --topic learning.query \
  --bootstrap-server localhost:9092
```

## Producer/Consumer Testing

### Console Producer
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-console-producer.sh \
  --topic test-topic \
  --bootstrap-server localhost:9092
```

### Console Consumer
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-console-consumer.sh \
  --topic test-topic \
  --from-beginning \
  --bootstrap-server localhost:9092
```

## Python Client Example

```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer
producer = KafkaProducer(
    bootstrap_servers=['kafka.kafka.svc.cluster.local:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send('learning.query', {
    'student_id': '123',
    'query': 'How do for loops work?'
})
producer.flush()

# Consumer
consumer = KafkaConsumer(
    'learning.response',
    bootstrap_servers=['kafka.kafka.svc.cluster.local:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='frontend-service'
)

for message in consumer:
    print(f"Received: {message.value}")
```

## Monitoring

### Check Pod Status
```bash
kubectl get pods -n kafka
kubectl logs kafka-0 -n kafka
kubectl describe pod kafka-0 -n kafka
```

### Check Broker Health
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-broker-api-versions.sh \
  --bootstrap-server localhost:9092
```

### View Logs
```bash
# Kafka logs
kubectl logs -f kafka-0 -n kafka

# ZooKeeper logs
kubectl logs -f kafka-zookeeper-0 -n kafka
```

## Performance Tuning

### Increase Throughput
```yaml
# In values.yaml
logFlushIntervalMs: 1000
numIoThreads: 8
numNetworkThreads: 3
socketReceiveBufferBytes: 102400
socketSendBufferBytes: 102400
```

### Optimize Retention
```yaml
logRetentionHours: 168  # 7 days
logRetentionBytes: 1073741824  # 1GB per partition
```

## Security Configuration

### Enable SASL/PLAIN Authentication
```yaml
auth:
  clientProtocol: sasl
  interBrokerProtocol: sasl
  sasl:
    mechanism: plain
    users:
      - user1
    passwords:
      - password1
```

### Enable TLS
```yaml
auth:
  tls:
    type: jks
    jksPassword: changeit
```

## Backup and Recovery

### Backup Topics List
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092 > topics-backup.txt
```

### Export Topic Configuration
```bash
kubectl exec -it kafka-0 -n kafka -- kafka-configs.sh \
  --describe \
  --entity-type topics \
  --entity-name learning.query \
  --bootstrap-server localhost:9092
```

## Scaling

### Scale Kafka Brokers
```bash
helm upgrade kafka bitnami/kafka \
  --namespace kafka \
  --set replicaCount=5
```

### Scale ZooKeeper
```bash
helm upgrade kafka bitnami/kafka \
  --namespace kafka \
  --set zookeeper.replicaCount=5
```

## Troubleshooting Guide

### Issue: Pods Stuck in Pending
**Cause**: Insufficient resources or PVC not bound
**Solution**:
```bash
kubectl describe pvc -n kafka
kubectl get storageclass
# Increase cluster resources or use different storage class
```

### Issue: Connection Refused
**Cause**: Service not exposed or incorrect hostname
**Solution**:
```bash
kubectl get svc -n kafka
kubectl describe svc kafka -n kafka
# Verify service endpoints exist
```

### Issue: Under-Replicated Partitions
**Cause**: Broker failure or network issues
**Solution**:
```bash
# Check broker status
kubectl exec -it kafka-0 -n kafka -- kafka-topics.sh \
  --describe \
  --under-replicated-partitions \
  --bootstrap-server localhost:9092
```

### Issue: High Memory Usage
**Cause**: Large message sizes or retention
**Solution**:
- Reduce retention period
- Increase heap size
- Enable compression

## Best Practices

1. **Use multiple replicas** for production (minimum 3)
2. **Set replication factor** to at least 2 for critical topics
3. **Configure resource limits** to prevent OOM kills
4. **Enable monitoring** with Prometheus/Grafana
5. **Use persistent volumes** for data durability
6. **Implement consumer groups** for parallel processing
7. **Set appropriate retention policies** to manage storage
8. **Test failover** by killing pods and observing recovery

## Integration with Dapr

Dapr provides Kafka pub/sub component:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka.kafka.svc.cluster.local:9092"
  - name: authType
    value: "none"
  - name: consumerGroup
    value: "learnflow-services"
```

## Resources
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Bitnami Kafka Helm Chart](https://github.com/bitnami/charts/tree/main/bitnami/kafka)
- [Kafka on Kubernetes Best Practices](https://strimzi.io/docs/operators/latest/overview.html)
