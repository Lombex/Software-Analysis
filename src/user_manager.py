import sqlite3
from user import User
from auth import Auth
from validationHelper import InputValidationUtility

class UserManager:
    def __init__(self, db_name='unique_meal.db'):
        self.auth = Auth(db_name)  # Initialize Auth directly with the database name
        self.current_user_role = None
        self.current_username = None
        self.input_validator = InputValidationUtility()  # Initialize InputValidationUtility directly

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
            choice = self.input_validator.validate_any_inputs("Enter your choice (1-6): ", 'choice', self.current_username)

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
            username = self.input_validator.validate_any_inputs("Username: ", 'username', self.current_username)
            password = self.input_validator.validate_any_inputs("Password: ", 'password', self.current_username)
            role = self.input_validator.validate_any_inputs("Role (consultant/system_admin): ", 'role', self.current_username)
            first_name = self.input_validator.validate_any_inputs("First Name: ", 'name', self.current_username)
            last_name = self.input_validator.validate_any_inputs("Last Name: ", 'name', self.current_username)

            User.add_user(username, password, role, first_name, last_name)  # Pass the necessary arguments directly
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
            users = User.list_users()  # Call list_users method from User directly

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
            username = self.input_validator.validate_any_inputs("Enter username to update: ", 'username', self.current_username)
            user = User.get_user(username)  # Fetch user details from User directly
            if user:
                print("Current User details:")
                print(f"Username: {user[0]}, Role: {user[1]}, Name: {user[2]} {user[3]}")

                password = self.input_validator.validate_any_inputs("Enter new password (leave blank to keep current): ", 'password', self.current_username)
                role = self.input_validator.validate_any_inputs("Enter new role (consultant/system_admin leave blank to keep current): ", 'role', self.current_username)
                first_name = self.input_validator.validate_any_inputs("Enter new first name (leave blank to keep current): ", 'name', self.current_username)
                last_name = self.input_validator.validate_any_inputs("Enter new last name (leave blank to keep current): ", 'name', self.current_username)

                User.update_user(username, password or None, role or None, first_name or None, last_name or None)  # Call update_user from User directly
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
            username = self.input_validator.validate_any_inputs("Enter username to delete: ", 'username', self.current_username)
            User.delete_user(username)  # Call delete_user from User directly
            print("User deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_temp_password(self):
        if self.current_user_role not in ['system_admin', 'super_admin']:
            print("You don't have permission to create temporary passwords.")
            return
        try:
            username = self.input_validator.validate_any_inputs("Enter username to create temporary password: ", 'username', self.current_username)
            
            # Validate if username exists
            user = User.get_user(username)  # Call get_user from User directly
            if not user:
                print(f"User '{username}' not found.")
                return
            
            # Create temporary password
            temporary_password = self.input_validator.validate_any_inputs("Enter temporary password: ", 'password', self.current_username)
            if self.auth.reset_password(username, temporary_password):
                print(f"Temporary password created successfully for user '{username}'.")
            else:
                print(f"Failed to create temporary password for user '{username}'.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
