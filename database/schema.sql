import sqlite3
from cryptography.fernet import Fernet

class Database:
    def __init__(self, db_name="unique_meal.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                role TEXT,
                first_name TEXT,
                last_name TEXT,
                registration_date TEXT
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                gender TEXT,
                weight REAL,
                address TEXT,
                email TEXT,
                phone TEXT,
                registration_date TEXT,
                membership_id TEXT UNIQUE
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                username TEXT,
                activity TEXT,
                additional_info TEXT,
                suspicious INTEGER
            )
            """)
    def close(self):
        self.conn.close()
