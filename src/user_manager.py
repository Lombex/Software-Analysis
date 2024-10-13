import sqlite3
from user import User
from auth import Auth
from validationHelper import InputValidationUtility

class UserManager:
    def __init__(self, db_name='unique_meal.db'):
        self.auth = Auth(db_name)  # Initialize Auth directly with the database name
        self.user = User(db_name)  # Create an instance of the User class
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
            if self.current_user_role == 'super_admin':
                role = self.input_validator.validate_any_inputs("Role (consultant/system_admin): ", 'role', self.current_username).lower()
            if self.current_user_role == 'system_admin':
                print('Role: consultant')
                role = 'consultant'
            first_name = self.input_validator.validate_any_inputs("First Name: ", 'name', self.current_username)
            last_name = self.input_validator.validate_any_inputs("Last Name: ", 'name', self.current_username)

            self.user.add_user(username, password, role, first_name, last_name)
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
            users = self.user.list_users()

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
            # Validate the username input
            username = self.input_validator.validate_any_inputs("Enter username to update: ", 'username', self.current_username)
            user = self.user.get_user(username)
    
            if user:
                print('User found')
    
                # Restrict updating for certain roles based on permissions
                if self.current_user_role == 'system_admin' and user[1] in ['super_admin', 'system_admin']:
                    print("You don't have permission to update this user.")
                    return
                elif self.current_user_role == 'super_admin' and user[1] == 'super_admin':
                    print("You don't have permission to update this user.")
                    return
    
                # Show current user details
                print(f"Username: {user[0]}, Role: {user[1]}, First Name: {user[2]}, Last Name: {user[3]}")
    
                # Prompt for new values, allowing them to remain blank to keep current values
                password = input("Enter new password (leave blank to keep current): ").strip()
                if password:
                    password = self.input_validator.validate_any_inputs(password, 'password', self.current_username, skip=True)
    
                role = input("Enter new role (consultant/system_admin, leave blank to keep current): ").strip()
                if role:
                    role = self.input_validator.validate_any_inputs(role, 'role', self.current_username, skip=True)
    
                first_name = input("Enter new first name (leave blank to keep current): ").strip()
                if first_name:
                    first_name = self.input_validator.validate_any_inputs(first_name, 'name', self.current_username, skip=True)
    
                last_name = input("Enter new last name (leave blank to keep current): ").strip()
                if last_name:
                    last_name = self.input_validator.validate_any_inputs(last_name, 'name', self.current_username, skip=True)
    
                # Update user, passing `None` for fields left blank to keep current values
                self.user.update_user(
                    username,
                    password if password else None,
                    role if role else None,
                    first_name if first_name else None,
                    last_name if last_name else None
                )
    
                print("User updated successfully.")
            else:
                print("User not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_user(self):
        if self.current_user_role not in ['system_admin', 'super_admin']:
            print("You don't have permission to delete users.")
            return
        try:
            username = self.input_validator.validate_any_inputs("Enter username to delete: ", 'username', self.current_username)
            user = self.user.get_user(username)

            if user:
                if self.current_user_role == 'system_admin' and user[1] in ['super_admin', 'system_admin']:
                    print("You don't have permission to delete this user.")
                    return
                elif self.current_user_role == 'super_admin' and user[1] == 'super_admin':
                    print("You don't have permission to delete this user.")
                    return

                self.user.delete_user(username)
                print("User deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_temp_password(self):
        if self.current_user_role not in ['system_admin', 'super_admin']:
            print("You don't have permission to create temporary passwords.")
            return
        try:
            username = self.input_validator.validate_any_inputs("Enter username to create temporary password: ", 'username', self.current_username)
            user = self.user.get_user(username)
            if user:
                if self.current_user_role == 'system_admin' and user[1] in ['super_admin', 'system_admin']:
                    print("You don't have permission for this action.")
                    return
                elif self.current_user_role == 'super_admin' and user[1] == 'super_admin':
                    print("You don't have permission for this action.")
                    return

            temporary_password = self.input_validator.validate_any_inputs("Enter temporary password: ", 'password', self.current_username)
            if self.auth.reset_password(username, temporary_password):
                print(f"Temporary password created successfully for user '{username}'.")
            else:
                print(f"Failed to create temporary password for user '{username}'.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")