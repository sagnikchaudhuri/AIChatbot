import sqlite3
from datetime import datetime

DB = "leads.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        message TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_lead(name, phone, message):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO leads (name, phone, message, created_at)
    VALUES (?, ?, ?, ?)
    """, (name, phone, message, datetime.now()))

    conn.commit()
    conn.close()