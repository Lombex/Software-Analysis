import sqlite3
from datetime import datetime
from validation import validate_input
import base64
import os

class Member:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.salt = self.load_or_generate_salt()

    def load_or_generate_salt(self):
        salt_file = 'member_salt.bin'
        if os.path.exists(salt_file):
            with open(salt_file, 'rb') as file:
                return file.read()
        else:
            salt = os.urandom(16)
            with open(salt_file, 'wb') as file:
                file.write(salt)
            return salt

    def encrypt(self, data):
        return base64.b64encode(bytes([b ^ self.salt[i % len(self.salt)] for i, b in enumerate(data.encode())])).decode()

    def decrypt(self, data):
        decoded = base64.b64decode(data.encode())
        return bytes([b ^ self.salt[i % len(self.salt)] for i, b in enumerate(decoded)]).decode()

    def generate_membership_id(self):
        current_year = datetime.now().year
        base_id = f"{current_year % 100:02d}{datetime.now().strftime('%m%d%H%M%S')}"
        checksum = sum(int(digit) for digit in base_id) % 10
        return f"{base_id}{checksum}"

    def add_member(self, first_name, last_name, age, gender, weight, address, email, phone):
        if not all([
            validate_input('name', first_name),
            validate_input('name', last_name),
            validate_input('age', age),
            validate_input('weight', weight),
            validate_input('email', email),
            validate_input('phone', phone)
        ]):
            return None, "Invalid input. Please check your entries."

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        membership_id = self.generate_membership_id()

        try:
            c.execute("""
                INSERT INTO members 
                (membership_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                membership_id, 
                self.encrypt(first_name), 
                self.encrypt(last_name), 
                age, 
                gender, 
                weight, 
                self.encrypt(address), 
                self.encrypt(email), 
                self.encrypt(phone), 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            conn.commit()
            return membership_id, "Member added successfully."
        except sqlite3.Error as e:
            return None, f"Database error: {e}"
        finally:
            conn.close()

    def update_member(self, membership_id, **kwargs):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            current_data, _ = self.get_member(membership_id)
            if not current_data:
                return False, "Member not found."

            update_fields = []
            values = []

            for key, value in kwargs.items():
                if value is not None:
                    if key in ['first_name', 'last_name', 'address', 'email', 'phone']:
                        if validate_input(key, value):
                            update_fields.append(f"{key} = ?")
                            values.append(self.encrypt(value))
                    elif key in ['age', 'gender', 'weight']:
                        if validate_input(key, value):
                            update_fields.append(f"{key} = ?")
                            values.append(value)

            if not update_fields:
                return False, "No valid fields to update."

            values.append(membership_id)
            query = f"UPDATE members SET {', '.join(update_fields)} WHERE membership_id = ?"
            c.execute(query, values)
            conn.commit()
            return True, "Member updated successfully."
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            conn.close()

    def delete_member(self, membership_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            c.execute("DELETE FROM members WHERE membership_id=?", (membership_id,))
            if c.rowcount == 0:
                return False, "Member not found."
            conn.commit()
            return True, "Member deleted successfully."
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            conn.close()

    def list_members(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            c.execute("SELECT * FROM members")
            members = c.fetchall()
            decrypted_members = []
            for member in members:
                decrypted_member = list(member)
                for i in [1, 2, 6, 7, 8]:  # indexes of encrypted fields
                    decrypted_member[i] = self.decrypt(decrypted_member[i])
                decrypted_members.append(tuple(decrypted_member))
            return decrypted_members, "Members retrieved successfully."
        except sqlite3.Error as e:
            return [], f"Database error: {e}"
        finally:
            conn.close()

    def get_member(self, membership_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            c.execute("SELECT * FROM members WHERE membership_id=?", (membership_id,))
            member = c.fetchone()
            if member:
                decrypted_member = list(member)
                for i in [1, 2, 6, 7, 8]:  # indexes of encrypted fields
                    decrypted_member[i] = self.decrypt(decrypted_member[i])
                return tuple(decrypted_member), "Member retrieved successfully."
            else:
                return None, "Member not found."
        except sqlite3.Error as e:
            return None, f"Database error: {e}"
        finally:
            conn.close()

    def search_members(self, search_key):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            c.execute("""
                SELECT * FROM members WHERE 
                membership_id LIKE ? OR 
                first_name LIKE ? OR 
                last_name LIKE ? OR 
                address LIKE ? OR 
                email LIKE ? OR 
                phone LIKE ?
            """, ('%' + search_key + '%',) * 6)
            members = c.fetchall()
            decrypted_members = []
            for member in members:
                decrypted_member = list(member)
                for i in [1, 2, 6, 7, 8]:  # indexes of encrypted fields
                    decrypted_member[i] = self.decrypt(decrypted_member[i])
                decrypted_members.append(tuple(decrypted_member))
            return decrypted_members, "Search completed successfully."
        except sqlite3.Error as e:
            return [], f"Database error: {e}"
        finally:
            conn.close()