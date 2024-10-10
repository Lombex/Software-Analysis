from member import Member
from validation import validate_input, detect_suspicious_input, validate_zip_code, validate_city

class MemberManager:
    def __init__(self, db_name='unique_meal.db'):
        self.member = Member(db_name)
        self.valid_cities = ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven", 
                             "Tilburg", "Groningen", "Almere", "Breda", "Nijmegen"]  # Example list

    def run_member_management(self):
        while True:
            print("\nMember Management Menu:")
            print("1. Add Member")
            print("2. List Members")
            print("3. Search Members")
            print("4. Update Member")
            print("5. Delete Member")
            print("6. Back to Main Menu")
            choice = input("Enter your choice (1-6): ")

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
                print("Invalid choice. Please try again.")

    def get_validated_input(self, prompt, input_type):
        while True:
            value = input(prompt).strip()
            if detect_suspicious_input(value):
                print("Suspicious input detected. Please try again.")
                continue
            if validate_input(input_type, value):
                return value
            print(f"Invalid {input_type}. Please try again.")

    def get_validated_zip_code(self, prompt):
        while True:
            value = input(prompt).strip()
            if detect_suspicious_input(value):
                print("Suspicious input detected. Please try again.")
                continue
            if validate_zip_code(value):
                return value
            print("Invalid zip code. Please enter a valid Dutch zip code (e.g., 1234AB).")

    def get_validated_city(self, prompt):
        while True:
            value = input(prompt).strip()
            if detect_suspicious_input(value):
                print("Suspicious input detected. Please try again.")
                continue
            if validate_city(value, self.valid_cities):
                return value
            print(f"Invalid city. Please choose from: {', '.join(self.valid_cities)}")

    def add_member(self):
        print("\nAdding a new member:")
        try:
            first_name = self.get_validated_input("First Name (at least 2 letters): ", 'name')
            last_name = self.get_validated_input("Last Name (at least 2 letters): ", 'name')
            age = self.get_validated_input("Age (must be a positive integer): ", 'age')
            gender = input("Gender: ").strip()
            if detect_suspicious_input(gender):
                print("Suspicious input detected. Member creation aborted.")
                return
            weight = self.get_validated_input("Weight (must be a positive number): ", 'weight')
            
            street = input("Street name: ").strip()
            if detect_suspicious_input(street):
                print("Suspicious input detected. Member creation aborted.")
                return
            
            house_number = input("House number: ").strip()
            if detect_suspicious_input(house_number):
                print("Suspicious input detected. Member creation aborted.")
                return
            
            zip_code = self.get_validated_zip_code("Zip Code (DDDDXX): ")
            city = self.get_validated_city("City: ")
            
            address = f"{street} {house_number}, {zip_code} {city}"
            email = self.get_validated_input("Email (must contain '@'): ", 'email')
            phone = self.get_validated_input("Phone (+31-6-DDDDDDDD): ", 'phone')

            membership_id, message = self.member.add_member(first_name, last_name, age, gender, weight, address, email, phone)
            if membership_id:
                print(f"Member added successfully. Membership ID: {membership_id}")
            else:
                print(f"Failed to add member: {message}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_members(self):
        members, message = self.member.list_members()
        if members:
            print("\nList of Members:")
            for member in members:
                print(f"ID: {member[0]}, Name: {member[1]} {member[2]}, Email: {member[7]}")
        else:
            print(f"No members found: {message}")

    def search_members(self):
        search_key = input("Enter search key: ").strip()
        if detect_suspicious_input(search_key):
            print("Suspicious input detected. Search aborted.")
            return
        members, message = self.member.search_members(search_key)
        if members:
            print("\nSearch Results:")
            for member in members:
                print(f"ID: {member[0]}, Name: {member[1]} {member[2]}, Email: {member[7]}")
        else:
            print(f"No members found: {message}")

    def update_member(self):
        member_id = input("Enter member ID to update: ").strip()
        if detect_suspicious_input(member_id):
            print("Suspicious input detected. Update aborted.")
            return
        member, message = self.member.get_member(member_id)
        if member:
            print("Current Member details:")
            print(f"ID: {member[0]}, Name: {member[1]} {member[2]}, Age: {member[3]}, Gender: {member[4]}, Weight: {member[5]}, Address: {member[6]}, Email: {member[7]}, Phone: {member[8]}")

            print("\nEnter new details (leave blank to keep current):")
            updates = {}
            
            new_first_name = self.get_validated_input("New first name: ", 'name')
            if new_first_name:
                updates['first_name'] = new_first_name

            new_last_name = self.get_validated_input("New last name: ", 'name')
            if new_last_name:
                updates['last_name'] = new_last_name

            new_age = self.get_validated_input("New age: ", 'age')
            if new_age:
                updates['age'] = new_age

            new_gender = input("New gender: ").strip()
            if new_gender:
                if detect_suspicious_input(new_gender):
                    print("Suspicious input detected. Update aborted.")
                    return
                updates['gender'] = new_gender

            new_weight = self.get_validated_input("New weight: ", 'weight')
            if new_weight:
                updates['weight'] = new_weight

            new_street = input("New street name: ").strip()
            new_house_number = input("New house number: ").strip()
            new_zip_code = self.get_validated_zip_code("New zip code: ")
            new_city = self.get_validated_city("New city: ")
            
            if any([new_street, new_house_number, new_zip_code, new_city]):
                if detect_suspicious_input(new_street) or detect_suspicious_input(new_house_number):
                    print("Suspicious input detected. Update aborted.")
                    return
                updates['address'] = f"{new_street} {new_house_number}, {new_zip_code} {new_city}"

            new_email = self.get_validated_input("New email: ", 'email')
            if new_email:
                updates['email'] = new_email

            new_phone = self.get_validated_input("New phone: ", 'phone')
            if new_phone:
                updates['phone'] = new_phone

            if updates:
                success, message = self.member.update_member(member_id, **updates)
                print(message)
            else:
                print("No updates provided.")
        else:
            print(f"Member not found: {message}")

    def delete_member(self):
        member_id = input("Enter member ID to delete: ").strip()
        if detect_suspicious_input(member_id):
            print("Suspicious input detected. Deletion aborted.")
            return
        success, message = self.member.delete_member(member_id)
        print(message)