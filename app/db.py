import sqlite3
from pathlib import Path


DB_FILE = Path(__file__).resolve().parent / "app.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn