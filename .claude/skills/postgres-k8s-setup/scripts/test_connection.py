#!/usr/bin/env python3
"""
PostgreSQL Connection Test Script

Tests database connectivity and basic operations.
"""

import sys
import subprocess
import base64

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("✗ psycopg2 not installed")
    print("Install with: pip install psycopg2-binary")
    sys.exit(1)


def get_connection_details():
    """Retrieve connection details from Kubernetes"""
    try:
        # Get password from secret
        result = subprocess.run(
            ["kubectl", "get", "secret", "postgres-credentials", "-n", "postgres",
             "-o", "jsonpath={.data.password}"],
            capture_output=True,
            text=True,
            check=True
        )
        password = base64.b64decode(result.stdout.strip()).decode('utf-8')

        # Note: This assumes port-forwarding is active
        # kubectl port-forward -n postgres svc/postgres-postgresql 5432:5432
        return {
            'host': 'localhost',  # Change to service DNS if running in cluster
            'port': 5432,
            'database': 'learnflow',
            'user': 'learnflow_user',
            'password': password
        }
    except Exception as e:
        print(f"✗ Failed to get connection details: {e}")
        return None


def test_connection(conn_details):
    """Test basic connection"""
    print("🔗 Testing database connection...")

    try:
        conn = psycopg2.connect(
            host=conn_details['host'],
            port=conn_details['port'],
            database=conn_details['database'],
            user=conn_details['user'],
            password=conn_details['password'],
            connect_timeout=5
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

        print(f"  ✓ Connected successfully")
        print(f"  PostgreSQL version: {version.split(',')[0]}")

        cursor.close()
        conn.close()
        return True

    except psycopg2.OperationalError as e:
        print(f"  ✗ Connection failed: {e}")
        print("\n  Make sure port-forwarding is active:")
        print("    kubectl port-forward -n postgres svc/postgres-postgresql 5432:5432")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_tables(conn_details):
    """Test if tables exist"""
    print("\n📋 Checking database schema...")

    try:
        conn = psycopg2.connect(**conn_details)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # List all tables
        cursor.execute("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)

        tables = cursor.fetchall()

        if tables:
            print(f"  ✓ Found {len(tables)} tables:")
            for table in tables:
                print(f"    - {table['tablename']}")
        else:
            print("  ⚠ No tables found")
            print("    Run migrations: python scripts/migrate.py")

        cursor.close()
        conn.close()
        return len(tables) > 0

    except Exception as e:
        print(f"  ✗ Error checking tables: {e}")
        return False


def test_crud_operations(conn_details):
    """Test basic CRUD operations"""
    print("\n✏️  Testing CRUD operations...")

    try:
        conn = psycopg2.connect(**conn_details)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # CREATE - Insert test user
        print("  Testing INSERT...", end=" ")
        cursor.execute("""
            INSERT INTO users (email, username, hashed_password, full_name, role)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, ('test@example.com', 'testuser', 'hashed_pw', 'Test User', 'student'))

        user_id = cursor.fetchone()['id']
        conn.commit()
        print(f"✓ (ID: {user_id})")

        # READ - Select the user
        print("  Testing SELECT...", end=" ")
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        assert user['username'] == 'testuser'
        print("✓")

        # UPDATE - Modify the user
        print("  Testing UPDATE...", end=" ")
        cursor.execute("""
            UPDATE users
            SET full_name = %s
            WHERE id = %s
        """, ('Updated Name', user_id))
        conn.commit()
        print("✓")

        # DELETE - Remove the test user
        print("  Testing DELETE...", end=" ")
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        print("✓")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"\n  ✗ CRUD test failed: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False


def test_performance(conn_details):
    """Test basic performance"""
    print("\n⚡ Testing query performance...")

    try:
        import time

        conn = psycopg2.connect(**conn_details)
        cursor = conn.cursor()

        # Simple query
        start = time.time()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        elapsed = (time.time() - start) * 1000

        print(f"  ✓ Simple query: {elapsed:.2f}ms")

        # Count query
        start = time.time()
        cursor.execute("SELECT COUNT(*) FROM users;")
        count = cursor.fetchone()[0]
        elapsed = (time.time() - start) * 1000

        print(f"  ✓ Count query: {elapsed:.2f}ms ({count} rows)")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"  ✗ Performance test failed: {e}")
        return False


def main():
    """Main test function"""
    print("="*60)
    print("PostgreSQL Connection Test")
    print("="*60)
    print()

    # Get connection details
    conn_details = get_connection_details()
    if not conn_details:
        print("✗ Cannot get connection details")
        sys.exit(1)

    print(f"Connection details:")
    print(f"  Host: {conn_details['host']}")
    print(f"  Port: {conn_details['port']}")
    print(f"  Database: {conn_details['database']}")
    print(f"  User: {conn_details['user']}")
    print()

    # Run tests
    tests = [
        ("Connection", test_connection(conn_details)),
        ("Tables", test_tables(conn_details)),
        ("CRUD Operations", test_crud_operations(conn_details)),
        ("Performance", test_performance(conn_details))
    ]

    # Summary
    print("\n" + "="*60)
    print("Summary:")
    for test_name, result in tests:
        status = "✓" if result else "✗"
        print(f"  {status} {test_name}")

    all_passed = all(result for _, result in tests)

    if all_passed:
        print("\n✓ All tests passed!")
        print("\nDatabase is ready for use!")
    else:
        print("\n✗ Some tests failed")

    print("="*60)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
