import sqlite3
import hashlib

def initialize_db(db_name, sql_file):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    with open(sql_file, 'r') as f:
        sql_script = f.read()
        c.executescript(sql_script)
    conn.commit()
    conn.close()
    print("Database initialized with schema.")

def add_default_super_admin(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    super_admin_username = 'admin'
    super_admin_password = 'adminpass'
    super_admin_password_hash = hashlib.sha256(super_admin_password.encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO users (username, password_hash, role, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
              (super_admin_username, super_admin_password_hash, 'super_admin', 'Super', 'Admin'))
    conn.commit()
    conn.close()
    print("Default super admin added.")
