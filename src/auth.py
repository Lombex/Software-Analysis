import sqlite3
import hashlib

class Auth:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        password_hash = self.hash_password(password)
        c.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
        user = c.fetchone()
        conn.close()
        return user

    def is_super_admin(self, user):
        return user and user[3] == 'super_admin'
