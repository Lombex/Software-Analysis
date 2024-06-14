import sqlite3
from hashlib import sha256
from datetime import datetime

def register_user(username, password, role, first_name, last_name):
    conn = sqlite3.connect('unique_meal.db')
    c = conn.cursor()
    
    password_hash = sha256(password.encode()).hexdigest()
    
    c.execute("INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, ?)",
              (username, password_hash, role, first_name, last_name, datetime.now().strftime("%Y-%m-%d")))
    
    conn.commit()
    conn.close()
