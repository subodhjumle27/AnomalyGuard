import sqlite3
import os

def init_db(db_path='anomalyguard.db', schema_path='database/schema.sql'):
    """Initializes the database using the schema file."""
    if os.path.exists(db_path):
        print(f"Database already exists at {db_path}. Skipping initialization.")
        return

    print(f"Initializing database at {db_path}...")
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())
    print("Database initialization complete.")

if __name__ == "__main__":
    # Ensure we are in the project root
    init_db()
