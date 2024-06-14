from auth import Auth
from user import User
from member import Member
from logger import Logger
from backup.py import Backup
import getpass

def main():
    auth = Auth()
    logger = Logger()
    backup = Backup()

    print("Welcome to Unique Meal Member Management System")

    while True:
        print("1. Login")
        print("2. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            username = input("Username: ")
            password = getpass.getpass("Password: ")

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

                        Member.add_member(first_name, last_name, age, gender, weight, address, email, phone)
                        logger.log_activity(username, "Added Member")
                    elif choice == '2':
                        if auth.is_super_admin(user):
                            username = input("Username: ")
                            password = getpass.getpass("Password: ")
                            role = input("Role: ")
                            first_name = input("First Name: ")
                            last_name = input("Last Name: ")

                            User.add_user(username, password, role, first_name, last_name)
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
