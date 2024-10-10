import sqlite3
import hashlib
import os
import time
from validation import validate_input, detect_suspicious_input
from enum import Enum

# Assuming Role Enum is defined in a separate file
class Role(Enum):
    SUPER_ADMIN = 1
    SYSTEM_ADMIN = 2
    CONSULTANT = 3

class Auth:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.max_attempts = 3
        self.lockout_time = 300  # 5 minutes in seconds
        self.attempts = {}

    def generate_salt(self):
        """Generate a new salt for password hashing."""
        return os.urandom(16)  # 16 bytes of random data

    def hash_password(self, password, salt):
        """Hash the password using SHA-256 with a specific salt."""
        return hashlib.sha256(password.encode() + salt).hexdigest()

    def store_user(self, username, password, role):
        """Add a new user with a hashed password and salt."""
        salt = self.generate_salt()
        hashed_password = self.hash_password(password, salt)

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            c.execute("""
                INSERT INTO users (username, password_hash, salt, role) 
                VALUES (?, ?, ?, ?)
            """, (username, hashed_password, salt, role.value))  # Use role.value
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error while adding user: {e}")
        finally:
            conn.close()
    
    def login(self, username, password):
        """Authenticate user by validating input and checking credentials."""
        # Validate input
        if not all([validate_input('username', username), validate_input('password', password)]):
            return None, "Invalid input. Please check your credentials."
    
        # Check for suspicious inputs
        if detect_suspicious_input(username) or detect_suspicious_input(password):
            return None, "Suspicious input detected. Authentication aborted."
    
        # Check if the account is locked due to too many failed attempts
        if self.is_account_locked(username):
            return None, "Account is temporarily locked. Please try again later."
    
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
    
        try:
            # Query to retrieve user credentials from the database
            c.execute("SELECT id, username, role, password_hash, salt FROM users WHERE username=?", (username,))
            user = c.fetchone()
    
            # If user is found
            if user:
                user_id, username, role_value, stored_password_hash, salt = user
    
                # Convert string to Role Enum
                role = Role.from_string(role_value)  # Use the from_string method
    
                # Hash the entered password with the stored salt
                hashed_password = self.hash_password(password, salt)
    
                # If hashed passwords match, login successful
                if hashed_password == stored_password_hash:
                    self.reset_attempts(username)
                    return (user_id, username, role), "Login successful."
                else:
                    self.increment_attempts(username)
                    return None, "Invalid username or password."
            else:
                self.increment_attempts(username)
                return None, "Invalid username or password."
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # Logging error for debugging
            return None, "Database error occurred. Please try again."
        finally:
            conn.close()


    def is_account_locked(self, username):
        """Check if a user's account is locked due to too many failed login attempts."""
        if username in self.attempts:
            attempts_data = self.attempts[username]
            if attempts_data['count'] >= self.max_attempts:
                if time.time() - attempts_data['time'] < self.lockout_time:
                    return True
                else:
                    del self.attempts[username]  # Remove lock after time passes
        return False

    def increment_attempts(self, username):
        """Increment failed login attempts for a given username."""
        if username not in self.attempts:
            self.attempts[username] = {'count': 1, 'time': time.time()}
        else:
            self.attempts[username]['count'] += 1
            self.attempts[username]['time'] = time.time()

    def reset_attempts(self, username):
        """Reset login attempts after a successful login."""
        if username in self.attempts:
            del self.attempts[username]

    def change_password(self, username, current_password, new_password):
        """Allow the user to change their password after validating the current one."""
        if not all([
            validate_input('username', username),
            validate_input('password', current_password),
            validate_input('password', new_password)
        ]):
            return False, "Invalid input. Please check your entries."

        if detect_suspicious_input(username) or detect_suspicious_input(current_password) or detect_suspicious_input(new_password):
            return False, "Suspicious input detected. Password change aborted."

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Fetch the current password hash and salt from the database
            c.execute("SELECT password_hash, salt FROM users WHERE username=?", (username,))
            user = c.fetchone()

            if not user:
                return False, "User not found."

            stored_password_hash, salt = user

            # Check if the current password matches the stored hash
            if stored_password_hash != self.hash_password(current_password, salt):
                return False, "Current password is incorrect."

            # Update the password with a new hashed password
            new_salt = self.generate_salt()
            new_password_hash = self.hash_password(new_password, new_salt)
            c.execute("UPDATE users SET password_hash=?, salt=? WHERE username=?", (new_password_hash, new_salt, username))
            conn.commit()
            return True, "Password changed successfully."
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            conn.close()