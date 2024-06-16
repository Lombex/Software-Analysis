import sqlite3
from hashlib import sha256
import secrets
import string

class Auth:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute("SELECT id, username, role FROM users WHERE username=? AND password_hash=?", (username, sha256(password.encode('utf-8')).hexdigest()))
        user = c.fetchone()

        conn.close()
        return user

    def change_password(self, username, current_password, new_password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Validate new password
            if not self.is_valid_password(new_password):
                print("Invalid password. Please ensure your new password meets the requirements.")
                conn.close()
                return False

            # Check current password
            c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, sha256(current_password.encode('utf-8')).hexdigest()))
            user = c.fetchone()

            if not user:
                print("Current password incorrect. Password change failed.")
                conn.close()
                return False

            # Update password
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

    def create_temp_password(self, creator_role, username=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            if creator_role not in ['super_admin', 'system_admin', 'consultant']:
                print("You do not have permission to create temporary passwords.")
                return False

            temp_password = "TempPassword_1"
            
            if creator_role == 'consultant' and username:
                c.execute("UPDATE users SET temp_password=? WHERE username=?", (temp_password, username))
                conn.commit()
                print(f"Temporary password '{temp_password}' created for user '{username}'.")
            elif creator_role == 'super_admin' or creator_role == 'system_admin':
                c.execute("UPDATE users SET temp_password=?", (temp_password,))
                conn.commit()
                print(f"Temporary password '{temp_password}' created for all consultants.")
                
            return True
        except sqlite3.Error as e:
            print(f"SQLite error while creating temporary password: {e}")
            return False
        finally:
            conn.close()

    def verify_temp_password(self, username, temp_password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            c.execute("SELECT username FROM users WHERE username=? AND temp_password=?", (username, temp_password))
            user = c.fetchone()
            if user:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"SQLite error while verifying temporary password: {e}")
            return False
        finally:
            conn.close()

    def is_valid_password(self, password):
        # Implement your password validation logic here
        if len(password) < 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char.isdigit() for char in password):
            return False
        # Add more validation rules as needed

        return True
