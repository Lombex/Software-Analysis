import sqlite3
from hashlib import sha256
import secrets
import string
from validationHelper import *
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

class Auth:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

        # Load private key for decryption
        try:
            with open('src/private_key.pem', 'rb') as key_file:
                self.private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
        except FileNotFoundError:
            print("Private key file not found.")
            self.private_key = None

    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Hash the password to compare
            password_hash = sha256(password.encode('utf-8')).hexdigest()

            # Retrieve all users with the matching password hash
            c.execute("SELECT id, username, role FROM users WHERE password_hash=?", (password_hash,))
            users = c.fetchall()

            # Loop through each user and attempt to decrypt the username
            for user in users:
                encrypted_username = user[1]

                # Decrypt the username
                try:
                    decrypted_username = self.private_key.decrypt(
                        encrypted_username,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    ).decode('utf-8')  # Decode the decrypted bytes to a string

                    # Check if the decrypted username matches the provided username
                    if decrypted_username == username:
                        print(f"Login successful!\nWelcome {decrypted_username}")
                        return user
                except Exception as e:
                    print(f"Decryption failed for user ID {user[0]}: {e}")

            # If no matches are found
            print("Login failed. No user found with matching username and password.")
            return None

        except sqlite3.Error as e:
            print(f"SQLite error during login: {e}")
            return None
        finally:
            conn.close()

    def change_password(self, username, current_password, new_password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Hash the current password
            current_password_hash = sha256(current_password.encode('utf-8')).hexdigest()

            # Check current password
            c.execute("SELECT * FROM users WHERE password_hash=?", (current_password_hash,))
            user = c.fetchone()

            if not user:
                print("Current password incorrect. Password change failed.")
                conn.close()
                return False

            # Hash the new password
            hashed_password = sha256(new_password.encode('utf-8')).hexdigest()
            c.execute("UPDATE users SET password_hash=? WHERE username=?", (hashed_password, user[1]))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error while updating password: {e}")
            conn.close()
            return False

    def reset_password(self, username, temporary_password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Hash the temporary password
            hashed_password = sha256(temporary_password.encode('utf-8')).hexdigest()
            c.execute("UPDATE users SET password_hash=? WHERE username=?", (hashed_password, username))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error while resetting password: {e}")
            conn.close()
            return False

    def create_temp_password(self, creator_role, username=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            if creator_role not in ['super_admin', 'system_admin', 'consultant']:
                print("You do not have permission to create temporary passwords.")
                return False

            temp_password = "TempPassword_1"
            
            if creator_role == 'consultant' and username:
                c.execute("UPDATE users SET temp_password=? WHERE username=?", (temp_password, username))
                conn.commit()
                print(f"Temporary password '{temp_password}' created for user '{username}'.")
            elif creator_role == 'super_admin' or creator_role == 'system_admin':
                c.execute("UPDATE users SET temp_password=?", (temp_password,))
                conn.commit()
                print(f"Temporary password '{temp_password}' created for all consultants.")
                
            return True
        except sqlite3.Error as e:
            print(f"SQLite error while creating temporary password: {e}")
            return False
        finally:
            conn.close()

    def verify_temp_password(self, username, temp_password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            c.execute("SELECT username FROM users WHERE username=? AND temp_password=?", (username, temp_password))
            user = c.fetchone()
            if user:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"SQLite error while verifying temporary password: {e}")
            return False
        finally:
            conn.close()
