from auth import Auth
from logger import Logger
from backup import Backup
from database import initialize_db, add_default_super_admin
from member_manager import MemberManager
from user_manager import UserManager
from login import Login
import os

def main():
    db_name = 'unique_meal.db'
    sql_file = 'src/schema.sql'

    # Initialize database if it does not exist
    if not os.path.exists(db_name):
        print("Initializing database...")
        initialize_db(db_name, sql_file)
        add_default_super_admin(db_name)
        print("Database initialized and default super admin added.")

    # Initialize necessary components
    auth = Auth(db_name)
    logger = Logger(db_name)
    backup = Backup(db_name)
    member_manager = MemberManager(db_name)
    user_manager = UserManager(db_name)

    print("Welcome to Unique Meal Member Management System")
    try:
        while True:
            print("\nMain Menu:")
            print("1. Login")
            print("2. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                user = Login.login(auth, logger)  # Pass auth and logger to login
                if user:
                    user_id, username, role = user  # Unpack the tuple returned by login
                    print(f"Welcome {username}")  # Print welcome message with username
                    logger.log_activity(username, "Logged in")

                    # Call menu based on user role (add this part based on your requirements)
                    if role == 'consultant':
                        Login.consultant_menu(user, auth, logger)  # Use user info to access member management
                    elif role in ['system_admin', 'super_admin']:
                        # Add appropriate method calls for admin roles
                        Login.admin_menu(user, auth, logger)  # For example, run user management

            elif choice == '2':
                print("Exiting the application.")
                break

            else:
                print("Invalid choice, please try again.")
    except Exception as e:
        print(f"An error occurred, returning to Main Menu")
        main()

if __name__ == "__main__":
    main()
