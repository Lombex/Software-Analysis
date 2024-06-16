from member import Member
from datetime import datetime
import sqlite3

class MemberManager:
    def __init__(self, db_name='unique_meal.db'):
        self.member = Member(db_name)

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
                print("Invalid choice")

    def add_member(self):
        while True:
            try:
                # Input for member details (first_name, last_name, age, gender, weight, address, email, phone)
                # ... (same as before)

                # Generate membership ID and add member
                membership_id = self.member.add_member(first_name, last_name, age, gender, weight, address, email, phone)
                if membership_id:
                    print(f"Member added with Membership ID: {membership_id}")
                break  # Break out of the loop if member is successfully added

            except ValueError as e:
                print(f"Error: {e}")
                print("Please try again.")

            except sqlite3.Error as e:
                print(f"Database error: {e}")
                break  # Break out of the loop on database error

            except Exception as e:
                print(f"An error occurred: {e}")
                break  # Break out of the loop on any other unexpected error

    def list_members(self):
        members = self.member.list_members()
        if members:
            print("\nList of Members:")
            for member in members:
                print(f"Membership ID: {member[0]}, Name: {member[1]} {member[2]}, Age: {member[3]}, Gender: {member[4]}, Weight: {member[5]}, Address: {member[6]}, Email: {member[7]}, Phone: {member[8]}")
        else:
            print("No members found.")

    def search_members(self):
        search_key = input("Enter search key: ").strip().lower()  # Convert search key to lowercase for case-insensitive search
        members = self.member.search_members(search_key)
        if members:
            print("\nSearch Results:")
            for member in members:
                print(f"Membership ID: {member[0]}, Name: {member[1]} {member[2]}, Age: {member[3]}, Gender: {member[4]}, Weight: {member[5]}, Address: {member[6]}, Email: {member[7]}, Phone: {member[8]}")
        else:
            print("No members found.")

    def update_member(self):
        try:
            member_id = input("Enter member ID to update: ").strip()
            member = self.member.get_member(member_id)
            if member:
                print("\nCurrent Member details:")
                print(f"ID: {member[0]}, First Name: {member[1]}, Last Name: {member[2]}, Age: {member[3]}, Gender: {member[4]}, Weight: {member[5]}, Address: {member[6]}, Email: {member[7]}, Phone: {member[8]}")

                first_name = input("Enter new first name (leave blank to keep current): ").strip()
                last_name = input("Enter new last name (leave blank to keep current): ").strip()
                age = input("Enter new age (leave blank to keep current): ").strip()
                gender = input("Enter new gender (leave blank to keep current): ").strip()
                weight = input("Enter new weight (leave blank to keep current): ").strip()
                address = input("Enter new address (leave blank to keep current): ").strip()
                email = input("Enter new email (leave blank to keep current): ").strip()
                phone = input("Enter new phone (leave blank to keep current): ").strip()

                # Update member details, passing None for fields that were left blank
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
        try:
            member_id = input("Enter member ID to delete: ").strip()
            self.member.delete_member(member_id)
            print("Member deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
