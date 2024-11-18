import sqlite3

DB_NAME = "database.db"

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS sensor_data (
    id TEXT PRIMARY KEY,
    sensor TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    location TEXT,
    status TEXT,
    valid BOOLEAN
);
"""

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()