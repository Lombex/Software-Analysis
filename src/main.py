from auth import Auth
from user import User
from member import Member
from logger import Logger
from backup import Backup
from database import initialize_db, add_default_super_admin
import os

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

    print("Welcome to Unique Meal Member Management System")

    while True:
        print("1. Login")
        print("2. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")  # Changed from getpass.getpass to input

            user = auth.login(username, password)
            if user:
                print(f"Welcome {username}")
                logger.log_activity(username, "Logged in")
                while True:
                    print("1. Add Member")
                    print("2. Add User")
                    print("3. Create Backup")
                    print("4. Restore Backup")
                    print("5. View Logs")
                    print("6. Logout")
                    choice = input("Enter choice: ")

                    if choice == '1':
                        first_name = input("First Name: ")
                        last_name = input("Last Name: ")
                        age = int(input("Age: "))
                        gender = input("Gender: ")
                        weight = float(input("Weight: "))
                        address = input("Address: ")
                        email = input("Email: ")
                        phone = input("Phone: ")

                        Member.add_member(first_name, last_name, age, gender, weight, address, email, phone, db_name)
                        logger.log_activity(username, "Added Member")
                    elif choice == '2':
                        if auth.is_super_admin(user):
                            username = input("Username: ")
                            password = input("Password: ")
                            role = input("Role: ")
                            first_name = input("First Name: ")
                            last_name = input("Last Name: ")

                            User.add_user(username, password, role, first_name, last_name, db_name)
                            logger.log_activity(username, "Added User")
                        else:
                            print("Unauthorized action.")
                    elif choice == '3':
                        if auth.is_super_admin(user):
                            backup.create_backup()
                            logger.log_activity(username, "Created Backup")
                        else:
                            print("Unauthorized action.")
                    elif choice == '4':
                        if auth.is_super_admin(user):
                            backup_name = input("Enter backup name: ")
                            backup.restore_backup(backup_name)
                            logger.log_activity(username, "Restored Backup")
                        else:
                            print("Unauthorized action.")
                    elif choice == '5':
                        if auth.is_super_admin(user):
                            logs = logger.fetch_logs()
                            for log in logs:
                                print(log)
                        else:
                            print("Unauthorized action.")
                    elif choice == '6':
                        logger.log_activity(username, "Logged out")
                        break
                    else:
                        print("Invalid choice")
            else:
                print("Invalid credentials")
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
