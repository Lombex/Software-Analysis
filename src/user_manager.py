import sqlite3
from user import User
from auth import Auth
from validationHelper import InputValidationUtility

class UserManager:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.auth = Auth(db_name)
        self.current_user_role = None
        self.current_username = None
        self.input_validator = InputValidationUtility(db_name)

    def set_current_user(self, username, role):
        self.current_username = username
        self.current_user_role = role

    def run_user_management(self, user):
        self.set_current_user(user[1], user[2])  # Set username and role
        while True:
            print("\nUser Management Menu:")
            print("1. Add User")
            print("2. List Users")
            print("3. Update User")
            print("4. Delete User")
            print("5. Create Temporary Password")
            print("6. Back to Main Menu")
            choice = self.input_validator.get_validated_input("Enter your choice (1-6): ", 'choice', self.current_username)

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
        if self.current_user_role not in ['system_admin', 'super_admin']:
            print("You don't have permission to add users.")
            return
        try:
            username = self.input_validator.get_validated_input("Username: ", 'username', self.current_username)
            password = self.input_validator.get_validated_input("Password: ", 'password', self.current_username)
            role = self.input_validator.get_validated_input("Role (consultant/system_admin): ", 'role', self.current_username)
            first_name = self.input_validator.get_validated_input("First Name: ", 'name', self.current_username)
            last_name = self.input_validator.get_validated_input("Last Name: ", 'name', self.current_username)

            User.add_user(username, password, role, first_name, last_name, db_name=self.db_name)
            print("User added successfully.")

        except ValueError as e:
            print(f"Error: {e}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_users(self):
        if self.current_user_role not in ['system_admin', 'super_admin']:
            print("You don't have permission to list users.")
            return
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
            print(f"Database error: {e}")

    def update_user(self):
        if self.current_user_role not in ['system_admin', 'super_admin']:
            print("You don't have permission to update users.")
            return
        try:
            username = self.input_validator.get_validated_input("Enter username to update: ", 'username', self.current_username)
            user = User.get_user(username, db_name=self.db_name)
            if user:
                print("Current User details:")
                print(f"Username: {user[0]}, Role: {user[1]}, Name: {user[2]} {user[3]}")

                password = self.input_validator.get_validated_input("Enter new password (leave blank to keep current): ", 'password', self.current_username)
                role = self.input_validator.get_validated_input("Enter new role (consultant/system_admin/super_admin, leave blank to keep current): ", 'role', self.current_username)
                first_name = self.input_validator.get_validated_input("Enter new first name (leave blank to keep current): ", 'name', self.current_username)
                last_name = self.input_validator.get_validated_input("Enter new last name (leave blank to keep current): ", 'name', self.current_username)

                User.update_user(username, password or None, role or None, first_name or None, last_name or None, db_name=self.db_name)
                print("User updated successfully.")
            else:
                print("User not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_user(self):
        if self.current_user_role != 'super_admin':
            print("You don't have permission to delete users.")
            return
        try:
            username = self.input_validator.get_validated_input("Enter username to delete: ", 'username', self.current_username)
            User.delete_user(username, db_name=self.db_name)
            print("User deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_temp_password(self):
        if self.current_user_role not in ['system_admin', 'super_admin']:
            print("You don't have permission to create temporary passwords.")
            return
        try:
            username = self.input_validator.get_validated_input("Enter username to create temporary password: ", 'username', self.current_username)
            
            # Validate if username exists
            user = User.get_user(username, db_name=self.db_name)
            if not user:
                print(f"User '{username}' not found.")
                return
            
            # Create temporary password
            temporary_password = self.input_validator.get_validated_input("Enter temporary password: ", 'password', self.current_username)
            if self.auth.reset_password(username, temporary_password):
                print(f"Temporary password created successfully for user '{username}'.")
            else:
                print(f"Failed to create temporary password for user '{username}'.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")