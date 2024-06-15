import sqlite3

def initialize_db(db_name, sql_file):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    with open(sql_file, 'r') as f:
        sql = f.read()
    c.executescript(sql)
    conn.commit()
    conn.close()

def add_default_super_admin(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    username = "admin"
    password = "adminpass"
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    role = "super_admin"
    c.execute("INSERT INTO users (username, password_hash, role, first_name, last_name) VALUES (?, ?, ?, 'Admin', 'User')", 
              (username, password_hash, role))
    conn.commit()
    conn.close()
