import sqlite3
import random
from datetime import datetime
from validation import validate_membership_id

class Member:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def add_member(self, first_name, last_name, age, gender, weight, address, email, phone):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Generate membership ID
        current_year = datetime.now().year % 100
        id_digits = [int(digit) for digit in str(current_year)]
        for _ in range(7):
            id_digits.append(random.randint(0, 9))
        checksum = sum(id_digits) % 10
        id_digits.append(checksum)
        membership_id = ''.join(map(str, id_digits))
        print("Generated ID:", membership_id)

        # Calculate checksum
        is_valid, message = validate_membership_id(membership_id)
        print(f"Validation result: {is_valid}, {message}")

        try:
            # Insert member into database
            c.execute("INSERT INTO members (membership_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (membership_id, first_name, last_name, age, gender, weight, address, email, phone, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error while inserting member: {e}")
            membership_id = None  # Return None if insertion fails
        finally:
            conn.close()
        
        return membership_id

    def update_member(self, membership_id, first_name=None, last_name=None, age=None, gender=None, weight=None, address=None, email=None, phone=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Check if all fields are None or empty
        if all(value is None or value == "" for value in (first_name, last_name, age, gender, weight, address, email, phone)):
            conn.close()
            print("No fields provided for update.")
            return

        try:
            # Create SET clause based on provided fields
            set_clause = []
            values = []

            if first_name is not None and first_name != "":
                set_clause.append("first_name = ?")
                values.append(first_name)
            if last_name is not None and last_name != "":
                set_clause.append("last_name = ?")
                values.append(last_name)
            if age is not None and age != "":
                set_clause.append("age = ?")
                values.append(int(age))
            if gender is not None and gender != "":
                set_clause.append("gender = ?")
                values.append(gender)
            if weight is not None and weight != "":
                set_clause.append("weight = ?")
                values.append(float(weight))
            if address is not None and address != "":
                set_clause.append("address = ?")
                values.append(address)
            if email is not None and email != "":
                set_clause.append("email = ?")
                values.append(email)
            if phone is not None and phone != "":
                set_clause.append("phone = ?")
                values.append(phone)

            # Add membership_id to values
            values.append(membership_id)

            # Construct and execute the UPDATE query
            set_clause = ", ".join(set_clause)
            query = f"UPDATE members SET {set_clause} WHERE membership_id = ?"
            c.execute(query, values)
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error while updating member: {e}")
        finally:
            conn.close()

    def delete_member(self, membership_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Execute DELETE query
            c.execute("DELETE FROM members WHERE membership_id=?", (membership_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error while deleting member: {e}")
        finally:
            conn.close()

    def list_members(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Execute SELECT query
            c.execute("SELECT * FROM members")
            members = c.fetchall()
        except sqlite3.Error as e:
            print(f"SQLite error while fetching members: {e}")
            members = []
        finally:
            conn.close()

        return members

    def get_member(self, membership_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Execute SELECT query
            c.execute("SELECT * FROM members WHERE membership_id=?", (membership_id,))
            member = c.fetchone()
        except sqlite3.Error as e:
            print(f"SQLite error while fetching member: {e}")
            member = None
        finally:
            conn.close()

        return member

    def search_members(self, search_key):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Execute SELECT query with LIKE clause for each field
            c.execute("SELECT * FROM members WHERE "
                      "membership_id LIKE ? OR "
                      "LOWER(first_name) LIKE ? OR "
                      "LOWER(last_name) LIKE ? OR "
                      "LOWER(address) LIKE ? OR "
                      "LOWER(email) LIKE ? OR "
                      "phone LIKE ? OR "
                      "LOWER(gender) LIKE ? OR "
                      "weight LIKE ?",
                      (f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%"))

            members = c.fetchall()
        except sqlite3.Error as e:
            print(f"SQLite error while searching members: {e}")
            members = []
        finally:
            conn.close()

        return members
