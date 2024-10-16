from member import Member
from validationHelper import InputValidationUtility
import sqlite3

class MemberManager:
    def __init__(self, db_name = "unique_meal.db"):
        self.member = Member(db_name)  # Initialize the Member class directly with the database name
        self.current_user_role = None
        self.current_username = None
        self.input_validator = InputValidationUtility()  # Initialize the validation utility directly

    def set_current_user(self, username, role):
        self.current_username = username
        self.current_user_role = role

    def run_member_management(self, user):
        self.set_current_user(user[1], user[2])  # Set username and role
        while True:
            print("\n1. Add Member")
            print("2. List Members")
            print("3. Search Members")
            print("4. Update Member")
            print("5. Delete Member")
            print("6. Back to Main Menu")
            choice = self.input_validator.validate_any_inputs("Enter your choice (1-6): ", 'choice', self.current_username)

            if choice == '1':
                self.add_member()
            elif choice == '2':
                self.list_members()
            elif choice == '3':
                self.search_members()
            elif choice == '4':
                self.update_member()
            elif choice == '5':
                self.delete_member()
            elif choice == '6':
                break
            else:
                print("Invalid choice")

    def add_member(self):
        if self.current_user_role not in ['consultant', 'system_admin', 'super_admin']:
            print("You don't have permission to add members.")
            return
        # Predefined list of cities
        cities = [
            "Amsterdam", "Rotterdam", "The Hague", "Utrecht", 
            "Eindhoven", "Tilburg", "Groningen", "Breda", 
            "Nijmegen", "Enschede"]
        try:
            first_name = self.input_validator.validate_any_inputs("First Name: ", 'name', self.current_username)
            last_name = self.input_validator.validate_any_inputs("Last Name: ", 'name', self.current_username)
            age = self.input_validator.validate_any_inputs("Age: ", 'age', self.current_username)
            gender = self.input_validator.validate_any_inputs("Gender (male/female/other): ", 'gender', self.current_username)
            weight = self.input_validator.validate_any_inputs("Weight: ", 'weight', self.current_username)
            # Collect address details step by step
            street_name = self.input_validator.get_validated_input("Street Name: ", 'address', self.current_username)
            house_number = self.input_validator.get_validated_input("House Number: ", 'number', self.current_username)
            zip_code = self.input_validator.get_validated_input("Zip Code (DDDDXX): ", 'zipcode', self.current_username)
            
            # Display predefined list of cities and ask user to choose
            print("Choose a city from the following list:")
            for index, city in enumerate(cities, 1):
                print(f"{index}. {city}")
            
            # City selection validation loop
            while True:
                try:
                    city_choice = int(self.input_validator.get_validated_input("Enter the number corresponding to your city: ", 'number', self.current_username))
                    
                    if 1 <= city_choice <= len(cities):
                        city = cities[city_choice - 1]  # Adjust for zero-based index
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(cities)}.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            
            # Combine address parts into a single string
            address = f"{street_name} {house_number}, {zip_code}, {city}"
            email = self.input_validator.validate_any_inputs("Email: ", 'email', self.current_username)
            phone = self.input_validator.get_validated_input("Phone +31-6-", 'phone', self.current_username)

            membership_id = self.member.add_member(first_name, last_name, int(age), gender, float(weight), address, email, phone)
            print(f"Member added with Membership ID: {membership_id}")

        except ValueError as e:
            print(f"Error: {e}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_members(self):
        if self.current_user_role not in ['consultant', 'system_admin', 'super_admin']:
            print("You don't have permission to list members.")
            return
        try:
            members = self.member.list_members()
            print(f"Fetched {len(members)} members.")  # Debug print

            if members:
                for member in members:
                    member_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date, membership_id = member
                    
                    formatted_phone = f"+31-6-{phone}"
                    print(f"ID: {member_id}, Name: {first_name} {last_name}, Age: {age}, Gender: {gender}, Weight: {weight}kg, Address: {address}")
                    print(f"Email: {email}, Phone: {formatted_phone}, Registered: {registration_date}, Membership ID: {membership_id}")
                    print("-" * 80)
            else:
                print("No members found.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def search_members(self):
        if self.current_user_role not in ['consultant', 'system_admin', 'super_admin']:
            print("You don't have permission to search members.")
            return
        try:
            search_key = self.input_validator.validate_any_inputs("Enter search key: ", 'search', self.current_username)
            members = self.member.search_members(search_key)
            print(f"Fetched {len(members)} matching members.")  # Debug print

            if members:
                for member in members:
                    member_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date, membership_id = member
                    
                    formatted_phone = f"+31-6-{phone}"
                    print(f"ID: {member_id}, Name: {first_name} {last_name}, Age: {age}, Gender: {gender}, Weight: {weight}kg, Address: {address}")
                    print(f"Email: {email}, Phone: {formatted_phone}, Registered: {registration_date}, Membership ID: {membership_id}")
                    print("-" * 80)
            else:
                print("No members found.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def update_member(self):
        if self.current_user_role not in ['system_admin', 'super_admin']:
            print("You don't have permission to update members.")
            return
        
        # Predefined list of cities
        cities = [
            "Amsterdam", "Rotterdam", "The Hague", "Utrecht", 
            "Eindhoven", "Tilburg", "Groningen", "Breda", 
            "Nijmegen", "Enschede"
        ]
        
        try:
            member_id = self.input_validator.validate_any_inputs("Enter member ID to update: ", 'member_id', self.current_username)
            member = self.member.get_member(member_id)
            if member:
                print("Current Member details:")
                print(f"ID: {member[0]}, First Name: {member[1]}, Last Name: {member[2]}, Age: {member[3]}, Gender: {member[4]}, Weight: {member[5]}, Address: {member[6]}, Email: {member[7]}, Phone: {member[8]}")

                first_name = self.input_validator.validate_any_inputs("Enter new first name (leave blank to keep current): ", 'name', self.current_username)
                last_name = self.input_validator.validate_any_inputs("Enter new last name (leave blank to keep current): ", 'name', self.current_username)
                age = self.input_validator.validate_any_inputs("Enter new age (leave blank to keep current): ", 'age', self.current_username)
                gender = self.input_validator.validate_any_inputs("Enter new gender (male/female/other, leave blank to keep current): ", 'gender', self.current_username)
                weight = self.input_validator.validate_any_inputs("Enter new weight (leave blank to keep current): ", 'weight', self.current_username)
                # Prompt for address updates (step by step)
                street_name = self.input_validator.get_validated_input("Enter new Street Name (leave blank to keep current): ", 'address', self.current_username)
                house_number = self.input_validator.get_validated_input("Enter new House Number (leave blank to keep current): ", 'number', self.current_username)
                zip_code = self.input_validator.get_validated_input("Enter new Zip Code (DDDDXX, leave blank to keep current): ", 'zipcode', self.current_username)

                # City selection with validation
                print("Choose a city from the following list (leave blank to keep current):")
                for index, city in enumerate(cities, 1):
                    print(f"{index}. {city}")

                while True:
                    city_choice = self.input_validator.get_validated_input("Enter the number corresponding to your city (leave blank to keep current): ", 'number', self.current_username)
                    
                    if not city_choice:
                        city = member[6].split(",")[-1].strip()  # Use the current city from the member's address
                        break
                    elif 1 <= int(city_choice) <= len(cities):
                        city = cities[int(city_choice) - 1]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(cities)}.")

                # If any part of the address is skipped, keep the current values
                street_name = street_name or member[6].split(",")[0].strip()
                house_number = house_number or member[6].split(",")[1].strip()
                zip_code = zip_code or member[6].split(",")[2].strip().split()[0]

                # Reconstruct the address
                address = f"{street_name} {house_number}, {zip_code}, {city}"

                # Collect email and phone number with the option to skip (keep current values)
                email = self.input_validator.validate_any_inputs("Enter new email (leave blank to keep current): ", 'email', self.current_username)
                phone = self.input_validator.validate_any_inputs("Enter new phone (leave blank to keep current): ", 'phone', self.current_username)

                # Update member details, keeping current values if fields are blank
                self.member.update_member(
                    member_id,
                    first_name or None,
                    last_name or None,
                    int(age) if age else None,
                    gender or None,
                    float(weight) if weight else None,
                    address or None,
                    email or None,
                    phone or None
                )
                print("Member updated successfully.")
            else:
                print("Member not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_member(self):
        if self.current_user_role != 'super_admin':
            print("You don't have permission to delete members.")
            return
        try:
            member_id = self.input_validator.validate_any_inputs("Enter member ID to delete: ", 'member_id', self.current_username)
            self.member.delete_member(member_id)
            print("Member deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
