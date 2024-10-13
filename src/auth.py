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

            # Fetch all users with the same password hash
            c.execute("SELECT id, username FROM users WHERE password_hash=?", (current_password_hash,))
            users = c.fetchall()

            if not users:
                print("Current password incorrect. Password change failed.")
                return False

            # Loop through each user and attempt to decrypt the username
            for user in users:
                if username == user[1]:
                    try:
                        decrypted_username = self.private_key.decrypt(
                            username,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        ).decode('utf-8')

                        # If the decrypted username matches, reset the password
                    
                    except Exception as e:
                        print(f"Decryption failed for user ID {user[0]}: {e}")

                    # Hash the new password
                    hashed_password = sha256(new_password.encode('utf-8')).hexdigest()
                    # Update the password in the database for the matching username
                    c.execute("UPDATE users SET password_hash=? WHERE username=?", (hashed_password, user[1]))
                    conn.commit()
                    print(f"Password updated successfully for {decrypted_username}.")
                    return True


            print("Username does not match any users with the given password.")
            return False

        except sqlite3.Error as e:
            print(f"SQLite error while updating password: {e}")
            return False
        finally:
            conn.close()


    def reset_password(self, username, temporary_password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            # Fetch all users (since usernames are encrypted)
            c.execute("SELECT id, username FROM users")
            users = c.fetchall()

            # Decrypt the usernames and match with the provided username
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
                    ).decode('utf-8')

                    # If the decrypted username matches, reset the password
                    if decrypted_username == username:
                        hashed_password = sha256(temporary_password.encode('utf-8')).hexdigest()
                        c.execute("UPDATE users SET password_hash=? WHERE username=?", (hashed_password, encrypted_username))
                        conn.commit()
                        print(f"Password reset successfully for {decrypted_username}.")
                        return True
                except Exception as e:
                    print(f"Decryption failed for user ID {user[0]}: {e}")

            print("Reset failed. No user found with matching username.")
            return False

        except sqlite3.Error as e:
            print(f"SQLite error while resetting password: {e}")
            return False
        finally:
            conn.close()


    def create_temp_password(self, creator_role, username=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
    
        try:
            if creator_role not in ['super_admin', 'system_admin', 'consultant']:
                print("You do not have permission to create temporary passwords.")
                return False
    
            temp_password = "TempPassword_1"
    
            # If username is provided (for consultants)
            if creator_role == 'consultant' and username:
                c.execute("SELECT id, username FROM users")
                users = c.fetchall()
    
                # Decrypt usernames to find the matching user
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
                        ).decode('utf-8')
    
                        # If the decrypted username matches the provided username
                        if decrypted_username == username:
                            c.execute("UPDATE users SET temp_password=? WHERE username=?", (temp_password, encrypted_username))
                            conn.commit()
                            print(f"Temporary password '{temp_password}' created for user '{decrypted_username}'.")
                            return True
                    except Exception as e:
                        print(f"Decryption failed for user ID {user[0]}: {e}")
    
                print(f"User '{username}' not found.")
                return False
    
            # For system_admin or super_admin, apply to all consultants
            elif creator_role in ['super_admin', 'system_admin']:
                c.execute("UPDATE users SET temp_password=?", (temp_password,))
                conn.commit()
                print(f"Temporary password '{temp_password}' created for all consultants.")
                return True
    
        except sqlite3.Error as e:
            print(f"SQLite error while creating temporary password: {e}")
            return False
    
        finally:
            conn.close()