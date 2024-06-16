import sqlite3
from user import User  # Assuming User class is implemented in user.py
from validation import validate_username, validate_password  # Validation functions from validation.py
from auth import Auth  # Import Auth class to handle temporary passwords

class UserManager:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.auth = Auth(db_name)  # Initialize Auth instance to handle temporary passwords

    def run_user_management(self):
        while True:
            print("\nUser Management Menu:")
            print("1. Add User")
            print("2. List Users")
            print("3. Update User")
            print("4. Delete User")
            print("5. Create Temporary Password")
            print("6. Back to Main Menu")
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.list_users()
            elif choice == '3':
                self.update_user()
            elif choice == '4':
                self.delete_user()
            elif choice == '5':
                self.create_temp_password()
            elif choice == '6':
                break
            else:
                print("Invalid choice")

    def add_user(self):
        try:
            # Input for username
            while True:
                username = input("Username (at least 8 characters, no longer than 10, start with letter or underscore, letters, numbers, underscores, apostrophes, periods): ").strip()
                if validate_username(username):
                    break
                else:
                    print("Invalid input. Username must adhere to the specified format.")

            # Input for password
            while True:
                password = input("Password (at least 12 characters, no longer than 30, combination of lowercase, uppercase, digit, special characters): ").strip()
                if validate_password(password):
                    break
                else:
                    print("Invalid input. Password must adhere to the specified format.")

            # Input for role
            while True:
                role = input("Role (consultant/system_admin/super_admin): ").strip().lower()
                if role in ['consultant', 'system_admin', 'super_admin']:
                    break
                else:
                    print("Invalid input. Role must be one of: consultant, system_admin, super_admin.")

            # Input for first_name
            while True:
                first_name = input("First Name (at least 2 letters): ").strip()
                if len(first_name) >= 2 and first_name.isalpha():
                    break
                else:
                    print("Invalid input. First name must be at least 2 letters and only contain alphabetic characters.")

            # Input for last_name
            while True:
                last_name = input("Last Name (at least 2 letters): ").strip()
                if len(last_name) >= 2 and last_name.isalpha():
                    break
                else:
                    print("Invalid input. Last name must be at least 2 letters and only contain alphabetic characters.")

            # Add user to database
            User.add_user(username, password, role, first_name, last_name, db_name=self.db_name)
            print("User added successfully.")

        except sqlite3.Error as e:
            print(f"SQLite error while inserting user: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def list_users(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT username, role, first_name, last_name FROM users")
            users = c.fetchall()
            conn.close()

            if users:
                for user in users:
                    print(f"Username: {user[0]}, Role: {user[1]}, Name: {user[2]} {user[3]}")
            else:
                print("No users found.")
        except sqlite3.Error as e:
            print(f"SQLite error while fetching users: {e}")

    def update_user(self):
        try:
            username = input("Enter username to update: ").strip()
            user = User.authenticate_user(username, '', db_name=self.db_name)  # Authenticated user to check role
            if user:
                print("Current User details:")
                print(f"Username: {user[0]}, Role: {user[3]}, Name: {user[4]} {user[5]}")

                # Input for password
                while True:
                    password = input("Enter new password (leave blank to keep current): ").strip()
                    if not password or validate_password(password):
                        break
                    else:
                        print("Invalid input. Password must adhere to the specified format.")

                # Input for role (only for system_admin)
                if User.is_system_admin(user):
                    while True:
                        new_role = input("Enter new role (consultant/system_admin/super_admin): ").strip().lower()
                        if new_role in ['consultant', 'system_admin', 'super_admin']:
                            break
                        else:
                            print("Invalid input. Role must be one of: consultant, system_admin, super_admin.")
                else:
                    new_role = None

                # Update user details, passing None for fields that were left blank
                User.update_user(username, password, new_role, db_name=self.db_name)
                print("User updated successfully.")
            else:
                print("User not found.")
        except sqlite3.Error as e:
            print(f"SQLite error while updating user: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_user(self):
        try:
            username = input("Enter username to delete: ").strip()
            User.delete_user(username, db_name=self.db_name)
            print("User deleted successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error while deleting user: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_temp_password(self):
        try:
            # Input for username
            username = input("Enter username to create temporary password: ").strip()
            
            # Validate if username exists
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT username FROM users WHERE username=?", (username,))
            user = c.fetchone()
            conn.close()
            
            if not user:
                print(f"User '{username}' not found.")
                return
            
            # Create temporary password
            temporary_password = input("Enter temporary password: ").strip()
            if self.auth.reset_password(username, temporary_password):
                print(f"Temporary password created successfully for user '{username}'.")
            else:
                print(f"Failed to create temporary password for user '{username}'.")

        except sqlite3.Error as e:
            print(f"SQLite error while checking user: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
