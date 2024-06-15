import sqlite3
import hashlib

class User:
    @staticmethod
    def add_user(username, password, role, first_name, last_name, db_name='unique_meal.db'):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password_hash, role, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
                  (username, password_hash, role, first_name, last_name))
        conn.commit()
        conn.close()
