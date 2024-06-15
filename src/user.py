import sqlite3
import hashlib
from auth import Auth
from logger import Logger
from datetime import datetime

class User:
    @staticmethod
    def add_user(username, password, role, first_name, last_name, db_name='unique_meal.db'):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, ?)",
                      (username, password_hash, role, first_name, last_name, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            print("User added successfully.")
        except sqlite3.IntegrityError:
            print("Username already exists. Please choose a different username.")
        finally:
            conn.close()

    @staticmethod
    def remove_user(username, db_name='unique_meal.db'):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username = ?", (username,))
        if c.rowcount == 0:
            print("User not found.")
        else:
            conn.commit()
            print(f"User '{username}' removed successfully.")
        conn.close()

    @staticmethod
    def update_user(username, password=None, role=None, first_name=None, last_name=None, db_name='unique_meal.db'):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        updates = []
        values = []

        if password:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            updates.append("password_hash = ?")
            values.append(password_hash)
        if role:
            updates.append("role = ?")
            values.append(role)
        if first_name:
            updates.append("first_name = ?")
            values.append(first_name)
        if last_name:
            updates.append("last_name = ?")
            values.append(last_name)

        if not updates:
            print("No updates provided.")
            return

        values.append(username)
        query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"
        c.execute(query, values)

        if c.rowcount == 0:
            print("User not found.")
        else:
            conn.commit()
            print(f"User '{username}' updated successfully.")
        conn.close()

    @staticmethod
    def get_user(username, db_name='unique_meal.db'):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user:
            return user
        else:
            print("User not found.")
            return None

    @staticmethod
    def user_exists(username, db_name='unique_meal.db'):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        exists = c.fetchone() is not None
        conn.close()
        return exists

    @staticmethod
    def list_users(db_name='unique_meal.db'):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()
        return users
    
    @staticmethod
    def handle_user_input():
        db_name = 'unique_meal.db'
        while True:
            print("Welcome to Unique Meal Membership Management System")
            print("1. Register")
            print("2. Update User")
            print("3. Remove User")
            print("4. List Users")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                username = input("Username: ")
                password = input("Password: ")
                role = input("Role (super_admin/system_admin/consultant): ")
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                User.add_user(username, password, role, first_name, last_name)
            elif choice == '2':
                username = input("Username: ")
                password = input("New Password (leave blank if unchanged): ")
                role = input("New Role (leave blank if unchanged): ")
                first_name = input("New First Name (leave blank if unchanged): ")
                last_name = input("New Last Name (leave blank if unchanged): ")
                User.update_user(username, password, role, first_name, last_name)
            elif choice == '3':
                username = input("Username: ")
                User.remove_user(username)
            elif choice == '4':
                users = User.list_users()
                for user in users:
                    print(user)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")