import sqlite3
import hashlib

class Auth:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        print(f"Attempting login with username: {username} and password: {password}")
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            c.execute("SELECT username, password_hash, role, first_name, last_name FROM users WHERE username = ?", (username,))
            user = c.fetchone()  # Fetch single row
            
            if user and user[1] == password_hash:
                user_info = {
                    'username': user[0],
                    'password_hash': user[1],
                    'role': user[2],
                    'first_name': user[3],
                    'last_name': user[4]
                }
            else:
                user_info = None
            
            return user_info
        
        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            return None
        
        finally:
            conn.close()

    def is_super_admin(self, user):
        return user and user['role'] == 'super_admin'
