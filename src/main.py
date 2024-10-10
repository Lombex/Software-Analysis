from auth import Auth
from logger import Logger
from backup import Backup
from database import initialize_db, add_default_super_admin
from member_manager import MemberManager
from user_manager import UserManager
import os
import getpass
from validation import validate_input, detect_suspicious_input

class Main:
    def __init__(self):
        self.db_name = 'unique_meal.db'
        self.sql_file = 'src/schema.sql'
        self.auth = Auth(self.db_name)
        self.logger = Logger(self.db_name)
        self.backup = Backup(self.db_name)
        self.member_manager = MemberManager(self.db_name)
        self.user_manager = UserManager(self.db_name)

    def initialize_system(self):
        if not os.path.exists(self.db_name):
            print("Initializing database...")
            initialize_db(self.db_name, self.sql_file)
            add_default_super_admin(self.db_name)
            print("Database initialized and default super admin added.")

    def get_validated_input(self, prompt, input_type):
        while True:
            value = input(prompt).strip()
            if detect_suspicious_input(value):
                print("Suspicious input detected. Please try again.")
                continue
            if validate_input(input_type, value):
                return value
            print(f"Invalid {input_type}. Please try again.")
    def login(self):
        login_attempts = 0
        while login_attempts < 3:
            username = self.get_validated_input("Username: ", 'username')
    
            # Temporary replacement of getpass for testing
            # Replace this with getpass.getpass() in production
            password = self.get_validated_input("Password: ", 'password')  # Ensure this line correctly calls the method
    
            user, message = self.auth.login(username, password)
            if user:
                print(f"Welcome, {username}!")
                self.logger.log_activity(username, "Logged in")
                return user
            else:
                print(message)
                login_attempts += 1
    
        print("Too many login attempts. Please try again later.")
        self.logger.log_activity("SYSTEM", "Login attempt", "High login frequency", "Yes")
        return None

    

    def consultant_menu(self, username):
        while True:
            print("\nConsultant Menu:")
            print("1. Change Password")
            print("2. Member Management")
            print("3. Logout")

            choice = input("Enter choice: ")

            if choice == '1':
                self.change_password(username)
            elif choice == '2':
                self.member_manager.run_member_management()
                self.logger.log_activity(username, "Accessed Member Management")
            elif choice == '3':
                self.logger.log_activity(username, "Logged out")
                break
            else:
                print("Invalid choice")

    def admin_menu(self, username):
        while True:
            print("\nAdministrator Menu:")
            print("1. Change Password")
            print("2. Member Management")
            print("3. User Management")
            print("4. Create Backup")
            print("5. Restore Backup")
            print("6. View Logs")
            print("7. Logout")

            choice = input("Enter choice: ")

            if choice == '1':
                self.change_password(username)
            elif choice == '2':
                self.member_manager.run_member_management()
                self.logger.log_activity(username, "Accessed Member Management")
            elif choice == '3':
                self.user_manager.run_user_management()
                self.logger.log_activity(username, "Accessed User Management")
            elif choice == '4':
                if self.backup.create_backup():
                    self.logger.log_activity(username, "Created Backup")
            elif choice == '5':
                backup_name = input("Enter backup name: ")
                if self.backup.restore_backup(backup_name):
                    self.logger.log_activity(username, "Restored Backup")
                    print("Backup restored. You will be logged out for security reasons.")
                    return
            elif choice == '6':
                logs = self.logger.fetch_logs()
                for log in logs:
                    print(log)
            elif choice == '7':
                self.logger.log_activity(username, "Logged out")
                break
            else:
                print("Invalid choice")

    def super_admin_menu(self, username):
        self.admin_menu(username)  # Super admin has all privileges of admin

    def change_password(self, username):
        current_password = getpass.getpass("Enter current password: ")
        new_password = self.get_validated_input("Enter new password: ", 'password')
        success, message = self.auth.change_password(username, current_password, new_password)
        if success:
            print("Password changed successfully.")
            self.logger.log_activity(username, "Changed their password")
        else:
            print(f"Failed to change password: {message}")

    def run(self):
        self.initialize_system()

        print("Welcome to Unique Meal Member Management System")
        while True:
            print("\nMain Menu:")
            print("1. Login")
            print("2. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                user = self.login()
                if user:
                    user_id, username, role = user
                    if role == 'consultant':
                        self.consultant_menu(username)
                    elif role == 'system_admin':
                        self.admin_menu(username)
                    elif role == 'super_admin':
                        self.super_admin_menu(username)
            elif choice == '2':
                print("Goodbye!")
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    try:
        main = Main()
        main.run()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logger = Logger('unique_meal.db')
        logger.log_activity("SYSTEM", "Error", str(e), "Yes")