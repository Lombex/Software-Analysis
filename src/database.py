import sqlite3
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Function to load RSA keys
def load_keys():
    # Load public key for encryption
    with open('src/public_key.pem', 'rb') as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    # Load private key for decryption
    with open('src/private_key.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

    return public_key, private_key

# Function to initialize the database schema
def initialize_db(db_name, sql_file):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        with open(sql_file, 'r') as f:
            sql = f.read()
        c.executescript(sql)
        conn.commit()
        print("Database schema initialized successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
    finally:
        conn.close()

# Function to add the default super_admin user to the database
def add_default_super_admin(db_name):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # Load keys for encryption
        public_key, _ = load_keys()

        # Super admin credentials
        username = "super_admin"
        password = "Admin_123?"
        role = "super_admin"

        # Encrypt the username
        encrypted_username = public_key.encrypt(
            username.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Insert the encrypted username, hashed password, and role into the database
        c.execute(
            "INSERT INTO users (username, password_hash, role, first_name, last_name) VALUES (?, ?, ?, 'Admin', 'User')",
            (encrypted_username, password_hash, role)
        )

        conn.commit()
        print("Default super admin added successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
    finally:
        conn.close()
