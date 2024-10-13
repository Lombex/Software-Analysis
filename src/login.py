from logger import Logger
from auth import Auth
from validationHelper import InputValidationUtility
from member_manager import MemberManager
from user_manager import UserManager
from backup import Backup


class Login:
    @staticmethod
    def login(auth, logger):
        print("Welcome to Unique Meal Member Management System")
        login_attempt = 0
        validation_utility = InputValidationUtility()  # Create an instance of InputValidationUtility

        while True:
            # Validate username input
            username = validation_utility.validate_any_inputs(
                'Enter your username: ', 'username', 'current_username'  # Pass the current username
            )
            # Validate password input
            password = validation_utility.validate_any_inputs(
                'Enter your password: ', 'password', username  # Use the validated username
            )

            if login_attempt >= 3:
                logger.log_activity(username, "Login Attempt", "Too many login attempts", "Yes")
                print("Too many login attempts reached!")
                break

            # Attempt to log in
            user = auth.login(username, password)
            if user:
                user_id, username, role = user  # Unpack the tuple returned by login
                logger.log_activity(username, "Logged in")
                login_attempt = 0  # Reset the attempt count on successful login
                return user
            else:
                login_attempt += 1
                print("Login failed. Please check your credentials.")


    @staticmethod
    def consultant_menu(user, auth: Auth, logger: Logger):
        validation_utility = InputValidationUtility()
        username = user[1]  # Extract username
        while True:
            print("\nConsultant Menu:")
            print("1. Change Password")
            print("2. Member Management")
            print("3. Logout")

            choice = input("Enter choice: ")

            if choice == '1':
                current_password = input("Enter old password: ")
                new_password = validation_utility.validate_any_inputs('Enter new password: ', 'password', username )
                if auth.change_password(username,current_password, new_password):
                    print("Password changed successfully.")
                    logger.log_activity(username, "Changed their password")
                else:
                    print("Failed to change password. Please try again.")

            elif choice == '2':
                member_manager = MemberManager()  # Assuming member_manager is instantiated here
                member_manager.run_member_management(user)  # Pass the whole user object
                logger.log_activity(username, "Accessed Member Management")

            elif choice == '3':
                logger.log_activity(username, "Logged out")
                break

            else:
                print("Invalid choice")

    @staticmethod
    def admin_menu(user, auth: Auth, logger: Logger, backup : Backup):
        validation_utility = InputValidationUtility()
        username, role = user[1], user[2]  # Extract username and role from user object
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
                if user[2] == 'super_admin':
                    print('Not allowed to change password.')
                    return
                current_password = input("Enter old password: ")
                new_password = validation_utility.validate_any_inputs('Enter new password: ', 'password', username )
                if auth.change_password(username, current_password, new_password):
                    print("Password changed successfully.")
                    logger.log_activity(username, "Changed their password")
                else:
                    print("Failed to change password. Please try again.")

            elif choice == '2':
                member_manager = MemberManager()  # Assuming member_manager is instantiated here
                member_manager.run_member_management(user)  # Pass the whole user object
                logger.log_activity(username, "Accessed Member Management")

            elif choice == '3':
                if role in ['system_admin', 'super_admin']:
                    user_manager = UserManager()  # Assuming user_manager is instantiated here
                    user_manager.run_user_management(user)
                    logger.log_activity(username, "Accessed User Management")
                else:
                    print("You do not have permission to access this section.")

            elif choice == '4':
                if role in ['system_admin', 'super_admin']:
                    backup.create_backup()
                    logger.log_activity(username, "Created Backup")
                else:
                    print("You do not have permission to access this section.")

            elif choice == '5':
                if role in ['system_admin', 'super_admin']:
                    backup_name = input("Enter backup name: ")
                    backup.restore_backup(backup_name)
                    logger.log_activity(username, "Restored Backup")
                    logger.log_activity(username, "Logged out")
                    break
                else:
                    print("You do not have permission to access this section.")

            elif choice == '6':
                Login.print_log(logger)

            elif choice == '7':
                logger.log_activity(username, "Logged out")
                break

            else:
                print("Invalid choice")

    @staticmethod
    def print_log(logger: Logger):
        logs = logger.fetch_logs()
        for log in logs:
            print(log)
