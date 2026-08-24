import sqlite3
import os

# make sure database folder exists
os.makedirs("database", exist_ok=True)

DB_PATH = "database/qr_attendance.db"

# connect to database (it will be created if not exists)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# create teachers table
c.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# add a default teacher account (for testing)
c.execute("INSERT OR IGNORE INTO teachers (id, name, email, password) VALUES (1, ?, ?, ?)",
          ("Admin", "admin@example.com", "admin123"))

conn.commit()
conn.close()

print("✅ Database created with default login (email=admin@example.com, password=admin123)")
