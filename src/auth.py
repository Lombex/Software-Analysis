import sqlite3
from hashlib import sha256

class Auth:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        hashed_password = sha256(password.encode('utf-8')).hexdigest()
        c.execute("SELECT id, username, role FROM users WHERE username=? AND password_hash=?", (username, hashed_password))
        user = c.fetchone()

        conn.close()
        return user

    def change_password(self, username, new_password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            hashed_password = sha256(new_password.encode('utf-8')).hexdigest()
            c.execute("UPDATE users SET password_hash=? WHERE username=?", (hashed_password, username))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error while updating password: {e}")
            conn.close()
            return False

    def reset_password(self, username, temporary_password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            hashed_password = sha256(temporary_password.encode('utf-8')).hexdigest()
            c.execute("UPDATE users SET password_hash=? WHERE username=?", (hashed_password, username))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error while resetting password: {e}")
            conn.close()
            return False
