#!/usr/bin/env python3
"""
PostgreSQL Migration Script for LearnFlow
Creates the database schema for the LearnFlow application.
"""

import subprocess
import sys
import base64


def get_password():
    """Retrieve password from Kubernetes secret"""
    try:
        result = subprocess.run(
            ["kubectl", "get", "secret", "postgres-credentials", "-n", "postgres",
             "-o", "jsonpath={.data.password}"],
            capture_output=True,
            text=True,
            check=True
        )
        password_b64 = result.stdout.strip()
        password = base64.b64decode(password_b64).decode('utf-8')
        return password
    except Exception as e:
        print(f"✗ Failed to get password: {e}", file=sys.stderr)
        return None


def run_sql_in_pod(sql_command):
    """Execute SQL command in PostgreSQL pod"""
    try:
        # Find the pod name
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", "postgres", "-l", "app.kubernetes.io/name=postgresql",
             "-o", "jsonpath={.items[0].metadata.name}"],
            capture_output=True,
            text=True,
            check=True
        )
        pod_name = result.stdout.strip()

        if not pod_name:
            print("✗ PostgreSQL pod not found")
            return False

        # Execute SQL
        result = subprocess.run(
            ["kubectl", "exec", "-it", pod_name, "-n", "postgres", "--",
             "psql", "-U", "learnflow_user", "-d", "learnflow", "-c", sql_command],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return True
        else:
            print(f"✗ SQL execution failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"✗ Error executing SQL: {e}", file=sys.stderr)
        return False


def create_schema():
    """Create database schema"""
    print("📝 Creating database schema...")

    migrations = [
        {
            "name": "users table",
            "sql": """
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    email VARCHAR(255) UNIQUE NOT NULL,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    full_name VARCHAR(255),
                    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher', 'admin')),
                    last_login TIMESTAMP WITH TIME ZONE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
            """
        },
        {
            "name": "learning_progress table",
            "sql": """
                CREATE TABLE IF NOT EXISTS learning_progress (
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
                CREATE INDEX IF NOT EXISTS idx_progress_user ON learning_progress(user_id);
                CREATE INDEX IF NOT EXISTS idx_progress_module ON learning_progress(module_id, topic_id);
            """
        },
        {
            "name": "code_submissions table",
            "sql": """
                CREATE TABLE IF NOT EXISTS code_submissions (
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
                CREATE INDEX IF NOT EXISTS idx_submissions_user ON code_submissions(user_id);
                CREATE INDEX IF NOT EXISTS idx_submissions_exercise ON code_submissions(exercise_id);
            """
        },
        {
            "name": "conversations table",
            "sql": """
                CREATE TABLE IF NOT EXISTS conversations (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                    agent_type VARCHAR(50) NOT NULL,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    context JSONB,
                    helpful BOOLEAN,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id);
                CREATE INDEX IF NOT EXISTS idx_conversations_date ON conversations(created_at DESC);
            """
        },
        {
            "name": "struggle_events table",
            "sql": """
                CREATE TABLE IF NOT EXISTS struggle_events (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                    event_type VARCHAR(50) NOT NULL,
                    description TEXT,
                    context JSONB,
                    resolved BOOLEAN DEFAULT FALSE,
                    teacher_notified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_struggle_user ON struggle_events(user_id);
                CREATE INDEX IF NOT EXISTS idx_struggle_resolved ON struggle_events(resolved);
            """
        }
    ]

    success_count = 0
    for migration in migrations:
        print(f"  Creating {migration['name']}...", end=" ")
        if run_sql_in_pod(migration['sql']):
            print("✓")
            success_count += 1
        else:
            print("✗")

    return success_count == len(migrations)


def verify_schema():
    """Verify tables were created"""
    print("\n🔍 Verifying schema...")

    tables = ['users', 'learning_progress', 'code_submissions', 'conversations', 'struggle_events']

    for table in tables:
        sql = f"SELECT to_regclass('public.{table}');"
        print(f"  Checking {table}...", end=" ")
        if run_sql_in_pod(sql):
            print("✓")
        else:
            print("✗")


def main():
    """Main migration function"""
    print("="*60)
    print("PostgreSQL Database Migration for LearnFlow")
    print("="*60)
    print()

    # Check if we can access the database
    password = get_password()
    if not password:
        print("✗ Cannot retrieve database password")
        print("Make sure PostgreSQL is deployed: ./scripts/deploy.sh")
        sys.exit(1)

    # Run migrations
    if create_schema():
        print("\n✓ Schema created successfully!")
    else:
        print("\n✗ Schema creation failed")
        sys.exit(1)

    # Verify
    verify_schema()

    print("\n" + "="*60)
    print("✓ Migration completed successfully!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Test connection: python scripts/test_connection.py")
    print("  2. Insert test data if needed")
    print("  3. Configure application to use database")


if __name__ == "__main__":
    main()
