from auth import Auth
from user import User  # If needed
from member import*
from member_manager import*
from logger import Logger
from backup import Backup
from database import initialize_db, add_default_super_admin
import os

def print_main_menu():
    print("Main Menu")
    print("1. Member Management")
    print("2. User Management")
    print("3. Backup")
    print("4. Exit")
    print()

def print_member_menu():
    print("Member Management Menu")
    print("1. Add Member")
    print("2. View Member")
    print("3. Update Member")
    print("4. Delete Member")
    print("5. List All Members")
    print("6. Back to Main Menu")
    print()

def login(auth):
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = auth.login(username, password)
        if user:
            print(f"Login successful. Welcome, {username}!")
            return user
        else:
            print("Invalid username or password. Please try again.")
            retry = input("Do you want to retry? (y/n): ")
            if retry.lower() != 'y':
                return None

def main():
    db_name = 'unique_meal.db'
    sql_file = 'schema.sql'

    if not os.path.exists(db_name):
        print("Initializing database...")
        initialize_db(db_name, sql_file)
        add_default_super_admin(db_name)
        print("Database initialized and default super admin added.")

    auth = Auth(db_name)
    logger = Logger(db_name)
    backup = Backup(db_name)
    member_manager = MemberManager()

    print("Welcome to Unique Meal Member Management System")

    user = login(auth)
    if not user:
        print("Exiting...")
        return

    while True:
        print_main_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            member_manager.run_member_management()

        elif choice == '2':
            # Placeholder for User Management (to be implemented)
            print("User Management menu")
            input("Press Enter to continue...")

        elif choice == '3':
            # Placeholder for Backup (to be implemented)
            print("Backup menu")
            input("Press Enter to continue...")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
