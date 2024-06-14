import hashlib
from database import Database

class Auth:
    def __init__(self):
        self.db = Database()

    def login(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = self.db.conn.execute("""
        SELECT * FROM users WHERE username = ? AND password_hash = ?
        """, (username, password_hash)).fetchone()
        return user

    def is_super_admin(self, user):
        return user and user[3] == 'super_admin'

    def is_system_admin(self, user):
        return user and user[3] == 'system_admin'

    def is_consultant(self, user):
        return user and user[3] == 'consultant'
