import sqlite3
import hashlib
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from validation import validate_username, validate_password

class User:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        
        # Load public key for encryption
        with open('src/public_key.pem', 'rb') as key_file:
            self.public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

        # Load private key for decryption
        with open('src/private_key.pem', 'rb') as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

    def add_user(self, username, password, role, first_name, last_name):
        # Validate inputs
        if not (validate_username(username) and validate_password(password)):
            print("Invalid input. Username or password does not meet criteria.")
            return

        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Encrypt sensitive fields
        encrypted_username = self.public_key.encrypt(
            username.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

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

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            # Insert encrypted data into the database
            c.execute("INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, ?)",
                      (encrypted_username, password_hash, role, encrypted_first_name, encrypted_last_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            print("User added successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error while inserting user: {e}")
        finally:
            conn.close()

    def authenticate_user(self, username, password):
        # Hash the password to compare with stored hash
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            # Encrypt the provided username
            encrypted_username = self.public_key.encrypt(
                username.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Query the database with the encrypted username and password hash
            c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (encrypted_username, password_hash))
            user = c.fetchone()
            return user  # Returns None if no user found, otherwise returns user details tuple
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return None
        finally:
            conn.close()

    def update_user(self, username, password=None, role=None, first_name=None, last_name=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # First, retrieve the encrypted username by decrypting it
            c.execute("SELECT username FROM users")
            users = c.fetchall()
            encrypted_username = None

            # Loop through all users and decrypt their usernames to find the matching one
            for user in users:
                decrypted_username = self.private_key.decrypt(
                    user[0],  # Assuming username is in the first column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode('utf-8')

                # Check if the decrypted username matches the input
                if decrypted_username == username:
                    encrypted_username = user[0]  # Save the encrypted username for later use
                    break

            if not encrypted_username:
                print("User not found.")
                return

            # Now proceed to update the fields as necessary
            update_fields = []
            values = []

            if password:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                update_fields.append("password_hash = ?")
                values.append(password_hash)

            if role:
                update_fields.append("role = ?")
                values.append(role)

            if first_name:
                encrypted_first_name = self.public_key.encrypt(
                    first_name.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                update_fields.append("first_name = ?")
                values.append(encrypted_first_name)

            if last_name:
                encrypted_last_name = self.public_key.encrypt(
                    last_name.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                update_fields.append("last_name = ?")
                values.append(encrypted_last_name)

            if not update_fields:
                print("Nothing to update.")
                return

            # Use the encrypted username to identify the record to update
            values.append(encrypted_username)
            set_clause = ", ".join(update_fields)
            c.execute(f"UPDATE users SET {set_clause} WHERE username = ?", values)
            conn.commit()
            print("User updated successfully.")
        except sqlite3.Error as e:
            print(f"SQLite error while updating user: {e}")
        finally:
            conn.close()



    def delete_user(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            # Retrieve all users from the database to find the correct encrypted username
            c.execute("SELECT username FROM users")
            users = c.fetchall()
            encrypted_username = None

            # Loop through all users and decrypt each username
            for user in users:
                decrypted_username = self.private_key.decrypt(
                    user[0],  # Assuming username is the first column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode('utf-8')

                # If decrypted username matches the input username, store the encrypted version
                if decrypted_username == username:
                    encrypted_username = user[0]
                    break

            # If no matching user is found, exit
            if not encrypted_username:
                print("User not found.")
                return

            # Now delete the user based on the encrypted username
            c.execute("DELETE FROM users WHERE username=?", (encrypted_username,))
            conn.commit()
            print("User deleted successfully.")
            
        except sqlite3.Error as e:
            print(f"SQLite error while deleting user: {e}")
        finally:
            conn.close()

    def get_user(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Retrieve all users and decrypt each user's username for comparison
            c.execute("SELECT username, role, first_name, last_name FROM users")
            users = c.fetchall()

            for user in users:
                # Decrypt the username
                decrypted_username = self.private_key.decrypt(
                    user[0],  # Assuming username is the first column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                # Check if the decrypted username matches the provided username
                if decrypted_username == username:
                    # Decrypt first name and last name if the username matches
                    decrypted_first_name = self.private_key.decrypt(
                        user[2],  # Assuming first_name is the third column
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    ).decode()

                    decrypted_last_name = self.private_key.decrypt(
                        user[3],  # Assuming last_name is the fourth column
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    ).decode()

                    return (decrypted_username, user[1], decrypted_first_name, decrypted_last_name)  # Return the decrypted values

            print("User not found.")
            return None
        except sqlite3.Error as e:
            print(f"SQLite error while retrieving user: {e}")
            return None
        finally:
            conn.close()


    def list_users(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT username, role, first_name, last_name FROM users")
            users = c.fetchall()

            decrypted_users = []
            for user in users:
                decrypted_username = self.private_key.decrypt(
                    user[0],  # Assuming username is the first column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_first_name = self.private_key.decrypt(
                    user[2],  # Assuming first_name is the third column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_last_name = self.private_key.decrypt(
                    user[3],  # Assuming last_name is the fourth column
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode()

                decrypted_users.append((
                    decrypted_username,
                    user[1],  # Role is not encrypted
                    decrypted_first_name,
                    decrypted_last_name
                ))

            return decrypted_users
        except sqlite3.Error as e:
            print(f"SQLite error while fetching users: {e}")
            return []
        finally:
            conn.close()
