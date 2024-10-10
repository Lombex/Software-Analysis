import sqlite3
from user import User
from validation import validate_input, detect_suspicious_input
from auth import Auth

class UserManager:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.auth = Auth(db_name)

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

    def get_validated_input(self, prompt, input_type):
        while True:
            value = input(prompt).strip()
            if detect_suspicious_input(value):
                print("Suspicious input detected. Please try again.")
                continue
            if validate_input(input_type, value):
                return value
            print(f"Invalid {input_type}. Please try again.")

    def add_user(self):
        try:
            username = self.get_validated_input("Username: ", 'username')
            password = self.get_validated_input("Password: ", 'password')
            
            while True:
                role = input("Role (consultant/system_admin/super_admin): ").strip().lower()
                if role in ['consultant', 'system_admin', 'super_admin']:
                    break
                print("Invalid role. Please choose from: consultant, system_admin, super_admin.")

            first_name = self.get_validated_input("First Name: ", 'name')
            last_name = self.get_validated_input("Last Name: ", 'name')

            success, message = User.add_user(username, password, role, first_name, last_name, db_name=self.db_name)
            print(message)

        except Exception as e:
            print(f"An error occurred: {e}")

    def list_users(self):
        users, message = User.list_users(db_name=self.db_name)
        if users:
            print("\nList of Users:")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[2]}, Name: {user[3]} {user[4]}, Registered: {user[5]}")
        else:
            print(message)

    def update_user(self):
        try:
            username = self.get_validated_input("Enter username to update: ", 'username')
            user, message = User.get_user(username, db_name=self.db_name)
            if user:
                print("Current User details:")
                print(f"Username: {user[1]}, Role: {user[3]}, Name: {user[4]} {user[5]}")

                updates = {}

                new_password = input("Enter new password (leave blank to keep current): ").strip()
                if new_password and validate_input('password', new_password):
                    updates['password'] = new_password

                while True:
                    new_role = input("Enter new role (consultant/system_admin/super_admin, leave blank to keep current): ").strip().lower()
                    if not new_role:
                        break
                    if new_role in ['consultant', 'system_admin', 'super_admin']:
                        updates['role'] = new_role
                        break
                    print("Invalid role. Please choose from: consultant, system_admin, super_admin.")

                new_first_name = self.get_validated_input("Enter new first name (leave blank to keep current): ", 'name')
                if new_first_name:
                    updates['first_name'] = new_first_name

                new_last_name = self.get_validated_input("Enter new last name (leave blank to keep current): ", 'name')
                if new_last_name:
                    updates['last_name'] = new_last_name

                if updates:
                    success, message = User.update_user(username, **updates, db_name=self.db_name)
                    print(message)
                else:
                    print("No updates provided.")
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_user(self):
        try:
            username = self.get_validated_input("Enter username to delete: ", 'username')
            success, message = User.delete_user(username, db_name=self.db_name)
            print(message)
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_temp_password(self):
        try:
            username = self.get_validated_input("Enter username to create temporary password: ", 'username')
            
            user, message = User.get_user(username, db_name=self.db_name)
            if not user:
                print(message)
                return
            
            temporary_password = self.get_validated_input("Enter temporary password: ", 'password')
            success, message = self.auth.reset_password(username, temporary_password)
            print(message)

        except Exception as e:
            print(f"An error occurred: {e}")