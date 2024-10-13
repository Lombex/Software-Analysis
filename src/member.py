import sqlite3
import random
from datetime import datetime
from validation import validate_membership_id
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os

class Member:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        
        # Load public key for encryption
        with open('src/public_key.pem', 'rb') as key_file:  # Make sure the path is correct
            self.public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

        with open('src/private_key.pem', 'rb') as key_file:  # Make sure the path is correct
            self.private_key = serialization.load_pem_private_key(
            key_file.read(),
            password = None,  # Add a password if needed
            backend = default_backend())

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

        # Encrypt sensitive fields before inserting them into the database
        encrypted_first_name = self.public_key.encrypt(
            first_name.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        encrypted_last_name = self.public_key.encrypt(
            last_name.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        encrypted_address = self.public_key.encrypt(
            address.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        encrypted_phone = self.public_key.encrypt(
            phone.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        try:
            # Insert member into the database with encrypted data
            c.execute(
                "INSERT INTO members (membership_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (membership_id, encrypted_first_name, encrypted_last_name, age, gender, weight, encrypted_address, email, encrypted_phone, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
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
                encrypted_first_name = self.public_key.encrypt(
                    first_name.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                set_clause.append("first_name = ?")
                values.append(encrypted_first_name)

            if last_name is not None and last_name != "":
                encrypted_last_name = self.public_key.encrypt(
                    last_name.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                set_clause.append("last_name = ?")
                values.append(encrypted_last_name)

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
                encrypted_address = self.public_key.encrypt(
                    address.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                set_clause.append("address = ?")
                values.append(encrypted_address)

            if email is not None and email != "":
                set_clause.append("email = ?")
                values.append(email)

            if phone is not None and phone != "":
                encrypted_phone = self.public_key.encrypt(
                    phone.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                set_clause.append("phone = ?")
                values.append(encrypted_phone)

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
            # Execute SELECT query to fetch all members (including membership_id)
            c.execute("SELECT * FROM members")
            members = c.fetchall()

            decrypted_members = []
            
            for member in members:
                # Decrypt sensitive fields for each member
                decrypted_first_name = self.private_key.decrypt(
                    member[1],  # Assuming first_name is the second column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_last_name = self.private_key.decrypt(
                    member[2],  # Assuming last_name is the third column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_address = self.private_key.decrypt(
                    member[6],  # Assuming address is the seventh column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_phone = self.private_key.decrypt(
                    member[8],  # Assuming phone is the ninth column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                # Append decrypted member information to the list (including membership_id)
                decrypted_members.append((
                    member[0],  # member_id
                    decrypted_first_name,
                    decrypted_last_name,
                    member[3],  # age
                    member[4],  # gender
                    member[5],  # weight
                    decrypted_address,
                    member[7],  # email
                    decrypted_phone,
                    member[9],  # registration_date
                    member[10]  # membership_id (assuming it's the 11th column)
                ))
            
            return decrypted_members

        except sqlite3.Error as e:
            print(f"SQLite error while fetching members: {e}")
            return []
        finally:
            conn.close()

    def get_member(self, membership_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Retrieve member data
            c.execute("SELECT * FROM members WHERE membership_id=?", (membership_id,))
            member = c.fetchone()

            if member:
                # Decrypt sensitive fields after retrieving from the database
                decrypted_first_name = self.private_key.decrypt(
                    member[1],  # Assuming first_name is the second column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_last_name = self.private_key.decrypt(
                    member[2],  # Assuming last_name is the third column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_address = self.private_key.decrypt(
                    member[6],  # Assuming address is the seventh column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_phone = self.private_key.decrypt(
                    member[8],  # Assuming phone is the ninth column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                # Return the decrypted data along with other member info
                return (member[0], decrypted_first_name, decrypted_last_name, member[3], member[4], member[5], decrypted_address, member[7], decrypted_phone, member[9])

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
            # Execute SELECT query to fetch all members
            c.execute("SELECT * FROM members")
            members = c.fetchall()

            matching_members = []
            search_key_lower = search_key.lower()  # To perform case-insensitive search

            for member in members:
                # Decrypt sensitive fields
                decrypted_first_name = self.private_key.decrypt(
                    member[1],  # Assuming first_name is the second column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_last_name = self.private_key.decrypt(
                    member[2],  # Assuming last_name is the third column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_address = self.private_key.decrypt(
                    member[6],  # Assuming address is the seventh column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_phone = self.private_key.decrypt(
                    member[8],  # Assuming phone is the ninth column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                # Perform case-insensitive search in the decrypted data
                if (search_key_lower in decrypted_first_name.lower() or
                    search_key_lower in decrypted_last_name.lower() or
                    search_key_lower in decrypted_address.lower() or
                    search_key_lower in decrypted_phone or
                    search_key_lower in str(member[0]) or  # Search in member_id
                    search_key_lower in str(member[3]) or  # Search in age
                    search_key_lower in member[4].lower() or  # Search in gender
                    search_key_lower in str(member[5]) or  # Search in weight
                    search_key_lower in member[7].lower() or  # Search in email
                    search_key_lower in str(member[10])):  # Search in membership_id

                    # Append the decrypted member details to matching members
                    matching_members.append((
                        member[0],  # member_id
                        decrypted_first_name,
                        decrypted_last_name,
                        member[3],  # age
                        member[4],  # gender
                        member[5],  # weight
                        decrypted_address,
                        member[7],  # email
                        decrypted_phone,
                        member[9],  # registration_date
                        member[10]  # membership_id
                    ))

            return matching_members

        except sqlite3.Error as e:
            print(f"SQLite error while searching members: {e}")
            return []
        finally:
            conn.close()
