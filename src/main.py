from auth import Auth
from logger import Logger
from backup import Backup
from database import initialize_db, add_default_super_admin
import os

from member_manager import MemberManager
from user_manager import UserManager

def main():
    db_name = 'unique_meal.db'
    sql_file = 'src/schema.sql'
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
            if result is not None:
                user_id, username, role = result  # Unpack the tuple returned by login

                print(f"Attempting login with username: {username} and password: {'*'*len(password)}")
                print(f"Welcome {username}")  # Use username directly

                logger.log_activity(username, "Logged in")

                while True:
                    print("\nUser Menu:")
                    if role == 'consultant':
                        print("1. Member Management")
                        print("2. Logout")
                    elif role == 'system_admin' or role == 'super_admin':
                        print("1. Member Management")
                        print("2. User Management")
                        print("3. Create Backup")
                        print("4. Restore Backup")
                        print("5. View Logs")
                        print("6. Print Log")
                        print("7. Logout")

                    choice = input("Enter choice: ")

                    if choice == '1':
                        member_manager.run_member_management()

                    elif choice == '2' and role == 'consultant':
                        logger.log_activity(username, "Logged out")
                        break

                    elif choice == '2' and (role == 'system_admin' or role == 'super_admin'):
                        user_manager.run_user_management()
                        logger.log_activity(username, "Accessed User Management")

                    elif choice == '3' and (role == 'system_admin' or role == 'super_admin'):
                        backup.create_backup()
                        logger.log_activity(username, "Created Backup")

                    elif choice == '4' and (role == 'system_admin' or role == 'super_admin'):
                        backup_name = input("Enter backup name: ")
                        backup.restore_backup(backup_name)
                        logger.log_activity(username, "Restored Backup")

                    elif choice == '5' and (role == 'system_admin' or role == 'super_admin'):
                        logs = logger.fetch_logs()
                        for log in logs:
                            print(log)

                    elif choice == '6' and (role == 'system_admin' or role == 'super_admin'):
                        print_log(logger)

                    elif choice == '7':
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
