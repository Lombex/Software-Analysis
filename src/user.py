# user.py

import sqlite3
import hashlib
from datetime import datetime
from validation import validate_username, validate_password

class User:
    @staticmethod
    def add_user(username, password, role, first_name, last_name, db_name='unique_meal.db'):
        # Validate inputs
        if not (validate_username(username) and validate_password(password)):
            print("Invalid input. Username or password does not meet criteria.")
            return

        # Function to add a new user
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, ?)",
                      (username, password_hash, role, first_name, last_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            print("User added successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error while inserting user: {e}")
        finally:
            conn.close()

    @staticmethod
    def authenticate_user(username, password, db_name='unique_meal.db'):
        # Function to authenticate a user
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, password_hash))
        user = c.fetchone()
        conn.close()
        return user  # Returns None if no user found, otherwise returns user details tuple

    @staticmethod
    def update_user(username, password=None, role=None, first_name=None, last_name=None, db_name='unique_meal.db'):
        # Validate password if provided
        if password and not validate_password(password):
            print("Invalid input. Password must adhere to the specified format.")
            return
    
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            update_fields = []
            values = []
    
            if password:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                update_fields.append("password_hash = ?")
                values.append(password_hash)
            if role:
                update_fields.append("role = ?")
                values.append(role)
            if first_name:
                update_fields.append("first_name = ?")
                values.append(first_name)
            if last_name:
                update_fields.append("last_name = ?")
                values.append(last_name)
    
            values.append(username)
            set_clause = ", ".join(update_fields)
            print(f"Updating user {username} with set clause: {set_clause} and values: {values}")  # Debug statement
            c.execute(f"UPDATE users SET {set_clause} WHERE username = ?", values)
            conn.commit()
            print("User updated successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error while updating user: {e}")
        finally:
            conn.close()

    @staticmethod
    def delete_user(username, db_name='unique_meal.db'):
        # Function to delete a user
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            print("User deleted successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error while deleting user: {e}")
        finally:
            conn.close()

    @staticmethod
    def is_consultant(user):
        # Check if user is a consultant
        return user and user[3] == 'consultant'

    @staticmethod
    def is_system_admin(user):
        # Check if user is a system administrator
        return user and user[3] == 'system_admin'

    @staticmethod
    def is_super_admin(user):
        # Check if user is a super administrator
        return user and user[3] == 'super_admin'

    @staticmethod
    def can_add_member(user):
        # Check if user can add a new member
        return User.is_consultant(user) or User.is_system_admin(user) or User.is_super_admin(user)

    @staticmethod
    def can_update_member(user):
        # Check if user can update member information
        return User.is_consultant(user) or User.is_system_admin(user) or User.is_super_admin(user)

    @staticmethod
    def can_delete_member(user):
        # Check if user can delete a member
        return User.is_system_admin(user) or User.is_super_admin(user)

    @staticmethod
    def can_view_logs(user):
        # Check if user can view system logs
        return User.is_system_admin(user) or User.is_super_admin(user)

    @staticmethod
    def can_make_backup(user):
        # Check if user can make a backup of the system
        return User.is_system_admin(user) or User.is_super_admin(user)
