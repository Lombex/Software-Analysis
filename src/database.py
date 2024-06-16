import sqlite3
import hashlib

def initialize_db(db_name, sql_file):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        with open(sql_file, 'r') as f:
            sql = f.read()
        c.executescript(sql)
        conn.commit()
        print("Database schema initialized successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
    finally:
        conn.close()

def add_default_super_admin(db_name):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        username = "super_admin"
        password = "Admin_123?"
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        role = "super_admin"
        c.execute("INSERT INTO users (username, password_hash, role, first_name, last_name) VALUES (?, ?, ?, 'Admin', 'User')", 
                  (username, password_hash, role))
        conn.commit()
        print("Default super admin added successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
    finally:
        conn.close()
