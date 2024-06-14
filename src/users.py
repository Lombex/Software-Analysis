import hashlib
import re
from database import Database

class User:
    def __init__(self, username, password, role, first_name, last_name):
        self.username = username
        self.password_hash = self.hash_password(password)
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.registration_date = "2024-06-14"

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def validate_username(username):
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_'.]{7,9}$", username):
            return False
        return True

    @staticmethod
    def validate_password(password):
        if (len(password) < 12 or len(password) > 30 or
            not re.search(r"[a-z]", password) or
            not re.search(r"[A-Z]", password) or
            not re.search(r"\d", password) or
            not re.search(r"[~!@#$%&_-+=`|\(){}[\]:;'<>,.?/]", password)):
            return False
        return True
    
    @staticmethod
    def add_user(username, password, role, first_name, last_name):
        db = Database()
        user = User(username, password, role, first_name, last_name)
        with db.conn:
            db.conn.execute("""
            INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (user.username, user.password_hash, user.role, user.first_name, user.last_name, user.registration_date))
        db.close()
