from auth import Auth
from logger import Logger
from backup import Backup
from database import initialize_db, add_default_super_admin
from member_manager import MemberManager
from user_manager import UserManager
import os

def main():
    db_name = 'unique_meal.db'
    sql_file = 'src/schema.sql'

    # Initialize database if not exists
    if not os.path.exists(db_name):
        print("Initializing database...")
        initialize_db(db_name, sql_file)
        add_default_super_admin(db_name)
        print("Database initialized and default super admin added.")

    auth = Auth(db_name)
    logger = Logger(db_name)
    backup = Backup(db_name)
    member_manager = MemberManager(db_name)
    user_manager = UserManager(db_name)

    print("Welcome to Unique Meal Member Management System")

    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")

            result = auth.login(username, password)
            if result:
                user_id, username, role = result  # Unpack the tuple returned by login

                print(f"Attempting login with username: {username} and password: {'*'*len(password)}")
                print(f"Welcome {username}")  # Print welcome message with username
                logger.log_activity(username, "Logged in")

                if role == 'consultant':
                    while True:
                        print("\nConsultant Menu:")
                        print("1. Change Password")
                        print("2. Member Management")
                        print("3. Logout")

                        choice = input("Enter choice: ")

                        if choice == '1':
                            new_password = input("Enter new password: ")
                            if auth.change_password(username, password, new_password):
                                print("Password changed successfully.")
                                logger.log_activity(username, "Changed their password")
                            else:
                                print("Failed to change password. Please try again.")

                        elif choice == '2':
                            member_manager.run_member_management()
                            logger.log_activity(username, "Accessed Member Management")

                        elif choice == '3':
                            logger.log_activity(username, "Logged out")
                            break

                        else:
                            print("Invalid choice")

                elif role == 'system_admin' or role == 'super_admin':
                    while True:
                        print("\nAdministrator Menu:")
                        print("1. Change Password")
                        print("2. Member Management")
                        print("3. User Management")
                        print("4. Create Backup")
                        print("5. Restore Backup")
                        print("6. View Logs")
                        print("7. Print Log")
                        print("8. Logout")

                        choice = input("Enter choice: ")

                        if choice == '1':
                            new_password = input("Enter new password: ")
                            if auth.change_password(username, password, new_password):
                                print("Password changed successfully.")
                                logger.log_activity(username, "Changed their password")
                            else:
                                print("Failed to change password. Please try again.")

                        elif choice == '2':
                            member_manager.run_member_management()
                            logger.log_activity(username, "Accessed Member Management")

                        elif choice == '3':
                            user_manager.run_user_management()
                            logger.log_activity(username, "Accessed User Management")

                        elif choice == '4':
                            backup.create_backup()
                            logger.log_activity(username, "Created Backup")

                        elif choice == '5':
                            backup_name = input("Enter backup name: ")
                            backup.restore_backup(backup_name)
                            logger.log_activity(username, "Restored Backup")

                        elif choice == '6':
                            logs = logger.fetch_logs()
                            for log in logs:
                                print(log)

                        elif choice == '7':
                            print_log(logger)

                        elif choice == '8':
                            logger.log_activity(username, "Logged out")
                            break

                        else:
                            print("Invalid choice")

            else:
                print("Login failed. Please check your credentials.")

        elif choice == '2':
            print("Goodbye!")
            break

        else:
            print("Invalid choice")

def print_log(logger):
    logs = logger.fetch_logs()
    for log in logs:
        print(log)

if __name__ == "__main__":
    main()
