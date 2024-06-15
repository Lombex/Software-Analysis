from member import Member  # Importing the Member class from member.py

class MemberManager:
    def __init__(self):
        self.member = Member()  # Initialize an instance of the Member class

    def print_member_menu(self):
        print("Member Management Menu")
        print("1. Add Member")
        print("2. View Member")
        print("3. Update Member")
        print("4. Delete Member")
        print("5. List All Members")
        print("6. Back to Main Menu")
        print()

    def run_member_management(self):
        while True:
            self.print_member_menu()
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.add_member()
            elif choice == '2':
                self.view_member()
            elif choice == '3':
                self.update_member()
            elif choice == '4':
                self.delete_member()
            elif choice == '5':
                self.list_members()
            elif choice == '6':
                print("Returning to Main Menu...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                input("Press Enter to continue...")

    def add_member(self):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        age = int(input("Enter age: "))
        gender = input("Enter gender: ")
        weight = float(input("Enter weight: "))
        address = input("Enter address: ")
        email = input("Enter email: ")
        phone = input("Enter phone: ")
        self.member.add_member(first_name, last_name, age, gender, weight, address, email, phone)
        print("Member added successfully.")
        input("Press Enter to continue...")

    def view_member(self):
        member_id = int(input("Enter member ID to view: "))
        member = self.member.get_member(member_id)
        if member:
            print("Member details:")
            print(f"ID: {member[0]}")
            print(f"First Name: {member[1]}")
            print(f"Last Name: {member[2]}")
            print(f"Age: {member[3]}")
            print(f"Gender: {member[4]}")
            print(f"Weight: {member[5]}")
            print(f"Address: {member[6]}")
            print(f"Email: {member[7]}")
            print(f"Phone: {member[8]}")
        else:
            print(f"Member with ID {member_id} not found.")
        input("Press Enter to continue...")

    def update_member(self):
        member_id = int(input("Enter member ID to update: "))
        member = self.member.get_member(member_id)
        if member:
            print("Current Member details:")
            print(f"ID: {member[0]}, First Name: {member[1]}, Last Name: {member[2]}, Age: {member[3]}, Gender: {member[4]}, Weight: {member[5]}, Address: {member[6]}, Email: {member[7]}, Phone: {member[8]}")
            first_name = input("Enter new first name (leave blank to keep current): ") or member[1]
            last_name = input("Enter new last name (leave blank to keep current): ") or member[2]
            age = int(input("Enter new age (leave blank to keep current): ")) or member[3]
            gender = input("Enter new gender (leave blank to keep current): ") or member[4]
            weight = float(input("Enter new weight (leave blank to keep current): ")) or member[5]
            address = input("Enter new address (leave blank to keep current): ") or member[6]
            email = input("Enter new email (leave blank to keep current): ") or member[7]
            phone = input("Enter new phone (leave blank to keep current): ") or member[8]
            self.member.update_member(member_id, first_name, last_name, age, gender, weight, address, email, phone)
            print("Member updated successfully.")
        else:
            print(f"Member with ID {member_id} not found.")
        input("Press Enter to continue...")

    def delete_member(self):
        member_id = int(input("Enter member ID to delete: "))
        member = self.member.get_member(member_id)
        if member:
            confirm = input(f"Are you sure you want to delete member {member[1]} {member[2]} (ID: {member_id})? (y/n): ")
            if confirm.lower() == 'y':
                self.member.delete_member(member_id)
                print("Member deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print(f"Member with ID {member_id} not found.")
        input("Press Enter to continue...")

    def list_members(self):
        members = self.member.list_members()
        if members:
            print("List of Members:")
            for member in members:
                print(f"ID: {member[0]}, Name: {member[1]} {member[2]}, Age: {member[3]}, Gender: {member[4]}, Weight: {member[5]}, Address: {member[6]}, Email: {member[7]}, Phone: {member[8]}")
        else:
            print("No members found.")
        input("Press Enter to continue...")
