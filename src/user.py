import sqlite3
import hashlib
import base64
import os
from datetime import datetime
from validation import validate_input, detect_suspicious_input

class User:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.salt = self.load_or_generate_salt()

    def load_or_generate_salt(self):
        salt_file = 'user_salt.bin'
        if os.path.exists(salt_file):
            with open(salt_file, 'rb') as file:
                return file.read()
        else:
            salt = os.urandom(16)
            with open(salt_file, 'wb') as file:
                file.write(salt)
            return salt

    def encrypt(self, data):
        return base64.b64encode(bytes([b ^ self.salt[i % len(self.salt)] for i, b in enumerate(data.encode())]))

    def decrypt(self, data):
        decoded = base64.b64decode(data)
        return bytes([b ^ self.salt[i % len(self.salt)] for i, b in enumerate(decoded)]).decode()

    def hash_password(self, password):
        return hashlib.sha256(password.encode() + self.salt).hexdigest()

    @staticmethod
    def add_user(username, password, role, first_name, last_name, db_name='unique_meal.db'):
        if not all([
            validate_input('username', username),
            validate_input('password', password),
            validate_input('name', first_name),
            validate_input('name', last_name)
        ]):
            return False, "Invalid input. Please check your entries."

        if any(detect_suspicious_input(i) for i in [username, password, first_name, last_name]):
            return False, "Suspicious input detected. User creation aborted."

        user = User(db_name)
        hashed_password = user.encrypt(user.hash_password(password))
        
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute("""
                INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                username, 
                hashed_password, 
                role, 
                user.encrypt(first_name).decode(), 
                user.encrypt(last_name).decode(), 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            conn.commit()
            return True, "User added successfully."
        except sqlite3.Error as e:
            return False, f"SQLite error while inserting user: {e}"
        finally:
            conn.close()

    @staticmethod
    def authenticate_user(username, password, db_name='unique_meal.db'):
        if detect_suspicious_input(username) or detect_suspicious_input(password):
            return None, "Suspicious input detected. Authentication aborted."

        user = User(db_name)
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            db_user = c.fetchone()
            if db_user:
                stored_hash = user.decrypt(db_user[2])
                if user.hash_password(password) == stored_hash:
                    return db_user, "Authentication successful."
                else:
                    return None, "Invalid username or password."
            else:
                return None, "User not found."
        except sqlite3.Error as e:
            return None, f"Database error: {e}"
        finally:
            conn.close()

    @staticmethod
    def update_user(username, password=None, role=None, first_name=None, last_name=None, db_name='unique_meal.db'):
        user = User(db_name)
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            update_fields = []
            values = []

            if password and validate_input('password', password):
                if detect_suspicious_input(password):
                    return False, "Suspicious input detected in password. Update aborted."
                hashed_password = user.encrypt(user.hash_password(password))
                update_fields.append("password_hash = ?")
                values.append(hashed_password)
            if role:
                if detect_suspicious_input(role):
                    return False, "Suspicious input detected in role. Update aborted."
                update_fields.append("role = ?")
                values.append(role)
            if first_name and validate_input('name', first_name):
                if detect_suspicious_input(first_name):
                    return False, "Suspicious input detected in first name. Update aborted."
                update_fields.append("first_name = ?")
                values.append(user.encrypt(first_name).decode())
            if last_name and validate_input('name', last_name):
                if detect_suspicious_input(last_name):
                    return False, "Suspicious input detected in last name. Update aborted."
                update_fields.append("last_name = ?")
                values.append(user.encrypt(last_name).decode())

            if not update_fields:
                return False, "No valid fields to update."

            values.append(username)
            set_clause = ", ".join(update_fields)
            c.execute(f"UPDATE users SET {set_clause} WHERE username = ?", values)
            conn.commit()
            return True, "User updated successfully."
        except sqlite3.Error as e:
            return False, f"SQLite error while updating user: {e}"
        finally:
            conn.close()

    @staticmethod
    def delete_user(username, db_name='unique_meal.db'):
        if detect_suspicious_input(username):
            return False, "Suspicious input detected. Deletion aborted."

        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute("DELETE FROM users WHERE username=?", (username,))
            if c.rowcount == 0:
                return False, "User not found."
            conn.commit()
            return True, "User deleted successfully."
        except sqlite3.Error as e:
            return False, f"SQLite error while deleting user: {e}"
        finally:
            conn.close()

    @staticmethod
    def get_user(username, db_name='unique_meal.db'):
        if detect_suspicious_input(username):
            return None, "Suspicious input detected. Retrieval aborted."

        user = User(db_name)
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            db_user = c.fetchone()
            if db_user:
                decrypted_user = list(db_user)
                decrypted_user[4] = user.decrypt(decrypted_user[4])  # Decrypt first_name
                decrypted_user[5] = user.decrypt(decrypted_user[5])  # Decrypt last_name
                return tuple(decrypted_user), "User retrieved successfully."
            else:
                return None, "User not found."
        except sqlite3.Error as e:
            return None, f"Database error: {e}"
        finally:
            conn.close()

    @staticmethod
    def list_users(db_name='unique_meal.db'):
        user = User(db_name)
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT id, username, role, first_name, last_name, registration_date FROM users")
            users = c.fetchall()
            decrypted_users = []
            for db_user in users:
                decrypted_user = list(db_user)
                decrypted_user[3] = user.decrypt(decrypted_user[3])  # Decrypt first_name
                decrypted_user[4] = user.decrypt(decrypted_user[4])  # Decrypt last_name
                decrypted_users.append(tuple(decrypted_user))
            return decrypted_users, "Users retrieved successfully."
        except sqlite3.Error as e:
            return [], f"Database error: {e}"
        finally:
            conn.close()

    @staticmethod
    def is_consultant(user):
        return user and user[3] == 'consultant'

    @staticmethod
    def is_system_admin(user):
        return user and user[3] == 'system_admin'

    @staticmethod
    def is_super_admin(user):
        return user and user[3] == 'super_admin'