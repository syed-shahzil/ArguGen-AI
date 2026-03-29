import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    "dbname": "argugen_db",
    "user": "postgres",
    "password": "pas123",
    "host": "localhost",
    "port": "5432"
}

CREATE_TABLES_QUERY = """
-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DEBATES TABLE
CREATE TABLE IF NOT EXISTS debates (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    statement TEXT NOT NULL,
    debate_history JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, statement)
);

-- RESULTS TABLE
CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    debate_id INTEGER REFERENCES debates(id) ON DELETE CASCADE,
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
conn=None
cursor=None

def create_tables():
    global conn, cursor
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("✅ Connected to PostgreSQL")

        cursor.execute(CREATE_TABLES_QUERY)

        conn.commit()

        print("✅ Tables created successfully")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("🔌 Connection closed")

if __name__ == "__main__":
    create_tables()