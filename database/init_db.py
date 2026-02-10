import sqlite3
import os

def init_db(db_path='anomalyguard.db', schema_path='database/schema.sql'):
    """Initializes the database using the schema file."""
    # Check if tables exist
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='monitored_transactions'")
        if cursor.fetchone():
            return

    print(f"Initializing database at {db_path}...")
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
    print("Database initialization complete.")

if __name__ == "__main__":
    # Ensure we are in the project root
    init_db()
