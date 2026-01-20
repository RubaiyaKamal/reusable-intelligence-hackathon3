# PostgreSQL Kubernetes Setup - Reference Documentation

## PostgreSQL Overview

PostgreSQL is a powerful, open-source relational database with ACID compliance, advanced features like JSON support, full-text search, and extensive indexing capabilities.

## Architecture on Kubernetes

```
┌─────────────────────────────────────────────────┐
│           Kubernetes Cluster                    │
│  ┌────────────────────────────────────────────┐ │
│  │  Namespace: postgres                       │ │
│  │                                            │ │
│  │  ┌──────────────────────────────────────┐ │ │
│  │  │  PostgreSQL StatefulSet              │ │ │
│  │  │  ┌────────────┐                      │ │ │
│  │  │  │ PostgreSQL │                      │ │ │
│  │  │  │   Pod-0    │                      │ │ │
│  │  │  └─────┬──────┘                      │ │ │
│  │  │        │                             │ │ │
│  │  │  ┌─────▼──────┐                      │ │ │
│  │  │  │ PVC (10Gi) │                      │ │ │
│  │  │  └────────────┘                      │ │ │
│  │  └──────────────────────────────────────┘ │ │
│  │                                            │ │
│  │  ┌──────────────────────────────────────┐ │ │
│  │  │  Service: postgres                   │ │ │
│  │  │  ClusterIP: 10.x.x.x:5432           │ │ │
│  │  └──────────────────────────────────────┘ │ │
│  │                                            │ │
│  │  ┌──────────────────────────────────────┐ │ │
│  │  │  Secret: postgres-credentials        │ │ │
│  │  │  - POSTGRES_PASSWORD                 │ │ │
│  │  │  - POSTGRES_USER                     │ │ │
│  │  └──────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

## LearnFlow Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

### Learning Progress Table
```sql
CREATE TABLE learning_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    module_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    mastery_score DECIMAL(5,2) DEFAULT 0.00 CHECK (mastery_score BETWEEN 0 AND 100),
    exercises_completed INTEGER DEFAULT 0,
    quiz_score DECIMAL(5,2),
    code_quality_rating DECIMAL(3,2),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    streak_days INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, module_id, topic_id)
);

CREATE INDEX idx_progress_user ON learning_progress(user_id);
CREATE INDEX idx_progress_module ON learning_progress(module_id, topic_id);
CREATE INDEX idx_progress_mastery ON learning_progress(mastery_score);
```

### Code Submissions Table
```sql
CREATE TABLE code_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    exercise_id UUID NOT NULL,
    code TEXT NOT NULL,
    language VARCHAR(20) DEFAULT 'python',
    status VARCHAR(20) CHECK (status IN ('pending', 'running', 'passed', 'failed', 'error')),
    output TEXT,
    error_message TEXT,
    execution_time_ms INTEGER,
    test_results JSONB,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submissions_user ON code_submissions(user_id);
CREATE INDEX idx_submissions_exercise ON code_submissions(exercise_id);
CREATE INDEX idx_submissions_status ON code_submissions(status);
CREATE INDEX idx_submissions_date ON code_submissions(submitted_at DESC);
```

### Conversations Table
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    agent_type VARCHAR(50) NOT NULL,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    context JSONB,
    helpful BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_date ON conversations(created_at DESC);
CREATE INDEX idx_conversations_agent ON conversations(agent_type);
```

### Struggle Events Table
```sql
CREATE TABLE struggle_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    description TEXT,
    context JSONB,
    resolved BOOLEAN DEFAULT FALSE,
    teacher_notified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_struggle_user ON struggle_events(user_id);
CREATE INDEX idx_struggle_resolved ON struggle_events(resolved);
CREATE INDEX idx_struggle_date ON struggle_events(created_at DESC);
```

## Bitnami PostgreSQL Helm Chart

### Development Configuration
```yaml
auth:
  postgresPassword: "dev-password"
  username: "learnflow_user"
  password: "learnflow-dev-pass"
  database: "learnflow"

primary:
  persistence:
    enabled: true
    size: 10Gi
  resources:
    requests:
      memory: 256Mi
      cpu: 250m
    limits:
      memory: 1Gi
      cpu: 1000m

readReplicas:
  replicaCount: 0
```

### Production Configuration
```yaml
auth:
  existingSecret: "postgres-credentials"

primary:
  persistence:
    enabled: true
    size: 100Gi
    storageClass: "fast-ssd"
  resources:
    requests:
      memory: 2Gi
      cpu: 1000m
    limits:
      memory: 4Gi
      cpu: 2000m

readReplicas:
  replicaCount: 2
  persistence:
    enabled: true
    size: 100Gi
  resources:
    requests:
      memory: 2Gi
      cpu: 1000m

metrics:
  enabled: true
  serviceMonitor:
    enabled: true

backup:
  enabled: true
  schedule: "0 2 * * *"
  retention: 7
```

## Connection Details

### From Within Kubernetes
```bash
# Service DNS
postgres-postgresql.postgres.svc.cluster.local:5432

# From same namespace
postgres-postgresql:5432

# Connection string
postgresql://learnflow_user:password@postgres-postgresql:5432/learnflow
```

### From External (Development)
```bash
# Port forward
kubectl port-forward -n postgres svc/postgres-postgresql 5432:5432

# Connect
psql -h localhost -U learnflow_user -d learnflow
```

## Database Management

### Create Database
```bash
kubectl exec -it postgres-postgresql-0 -n postgres -- psql -U postgres -c "CREATE DATABASE learnflow;"
```

### Create User
```bash
kubectl exec -it postgres-postgresql-0 -n postgres -- psql -U postgres -c "CREATE USER learnflow_user WITH PASSWORD 'secure-password';"
kubectl exec -it postgres-postgresql-0 -n postgres -- psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE learnflow TO learnflow_user;"
```

### Run SQL File
```bash
kubectl cp schema.sql postgres/postgres-postgresql-0:/tmp/schema.sql
kubectl exec -it postgres-postgresql-0 -n postgres -- psql -U learnflow_user -d learnflow -f /tmp/schema.sql
```

## Python Connection Example

### Using psycopg2
```python
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host="postgres-postgresql.postgres.svc.cluster.local",
    port=5432,
    database="learnflow",
    user="learnflow_user",
    password="password"
)

cursor = conn.cursor(cursor_factory=RealDictCursor)
cursor.execute("SELECT * FROM users WHERE role = %s", ('student',))
users = cursor.fetchall()

cursor.close()
conn.close()
```

### Using SQLAlchemy
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://learnflow_user:password@postgres-postgresql:5432/learnflow"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use session
db = SessionLocal()
try:
    users = db.query(User).filter(User.role == 'student').all()
finally:
    db.close()
```

## Backup and Restore

### Manual Backup
```bash
kubectl exec postgres-postgresql-0 -n postgres -- pg_dump -U learnflow_user learnflow > backup.sql
```

### Restore from Backup
```bash
kubectl cp backup.sql postgres/postgres-postgresql-0:/tmp/backup.sql
kubectl exec -it postgres-postgresql-0 -n postgres -- psql -U learnflow_user -d learnflow -f /tmp/backup.sql
```

### Automated Backups with CronJob
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: postgres
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15
            command:
            - /bin/sh
            - -c
            - pg_dump -h postgres-postgresql -U learnflow_user learnflow | gzip > /backup/learnflow-$(date +\%Y\%m\%d).sql.gz
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
            volumeMounts:
            - name: backup-volume
              mountPath: /backup
          volumes:
          - name: backup-volume
            persistentVolumeClaim:
              claimName: postgres-backup-pvc
          restartPolicy: OnFailure
```

## Performance Tuning

### Key Settings
```sql
-- Connection pooling
ALTER SYSTEM SET max_connections = 100;

-- Memory
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';

-- Write performance
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';

-- Query performance
ALTER SYSTEM SET random_page_cost = 1.1;  -- For SSD storage
ALTER SYSTEM SET effective_io_concurrency = 200;
```

### Create Indexes
```sql
-- Index on frequently queried columns
CREATE INDEX CONCURRENTLY idx_progress_user_module
ON learning_progress(user_id, module_id);

-- Partial index for active users
CREATE INDEX idx_users_active
ON users(last_login)
WHERE last_login > CURRENT_DATE - INTERVAL '30 days';

-- BRIN index for time-series data
CREATE INDEX idx_submissions_time_brin
ON code_submissions USING BRIN(submitted_at);
```

## Monitoring

### Check Connection Count
```sql
SELECT count(*) FROM pg_stat_activity;
```

### Find Slow Queries
```sql
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### Database Size
```sql
SELECT pg_size_pretty(pg_database_size('learnflow'));
```

### Table Sizes
```sql
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Integration with Dapr

Dapr State Store Component:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "host=postgres-postgresql.postgres.svc.cluster.local user=learnflow_user password=password dbname=learnflow port=5432 sslmode=disable"
```

## Best Practices

1. **Use connection pooling** (PgBouncer) for high-traffic applications
2. **Enable SSL/TLS** for production environments
3. **Regular VACUUM** to maintain performance
4. **Monitor replication lag** in read replica setups
5. **Set resource limits** to prevent OOM kills
6. **Use prepared statements** to prevent SQL injection
7. **Implement database migrations** with tools like Alembic
8. **Regular backups** with point-in-time recovery capability

## Troubleshooting

### Pod Won't Start
```bash
kubectl describe pod postgres-postgresql-0 -n postgres
kubectl logs postgres-postgresql-0 -n postgres
# Check PVC status
kubectl get pvc -n postgres
```

### Connection Refused
```bash
# Check service
kubectl get svc -n postgres
kubectl describe svc postgres-postgresql -n postgres

# Check if pod is ready
kubectl get pods -n postgres

# Test from another pod
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- psql -h postgres-postgresql.postgres.svc.cluster.local -U learnflow_user
```

### High CPU/Memory
```sql
-- Find expensive queries
SELECT * FROM pg_stat_activity WHERE state = 'active';

-- Kill long-running query
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid = <pid>;
```

## Resources
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Bitnami PostgreSQL Helm Chart](https://github.com/bitnami/charts/tree/main/bitnami/postgresql)
- [PostgreSQL on Kubernetes Best Practices](https://www.postgresql.org/docs/current/high-availability.html)
