import sqlite3
import hashlib
import base64
import os

def load_or_generate_salt():
    salt_file = 'db_salt.bin'
    if os.path.exists(salt_file):
        with open(salt_file, 'rb') as file:
            return file.read()
    else:
        salt = os.urandom(16)
        with open(salt_file, 'wb') as file:
            file.write(salt)
        return salt

def encrypt(data, salt):
    return base64.b64encode(bytes([b ^ salt[i % len(salt)] for i, b in enumerate(data.encode())]))

def hash_password(password, salt):
    return hashlib.sha256(password.encode() + salt).hexdigest()

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

def add_default_super_admin(db_name):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        username = "super_admin"
        password = "Admin_123?"
        role = "super_admin"
        first_name = "Admin"
        last_name = "User"

        salt = load_or_generate_salt()
        hashed_password = encrypt(hash_password(password, salt), salt)
        encrypted_first_name = encrypt(first_name, salt)
        encrypted_last_name = encrypt(last_name, salt)

        c.execute("""
            INSERT INTO users (username, password_hash, role, first_name, last_name, salt) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, hashed_password, role, encrypted_first_name, encrypted_last_name, salt))
        
        conn.commit()
        print("Default super admin added successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
    finally:
        conn.close()

def update_db_schema(db_name, update_sql_file):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        with open(update_sql_file, 'r') as f:
            sql = f.read()
        c.executescript(sql)
        conn.commit()
        print("Database schema updated successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error occurred while updating schema: {e}")
    finally:
        conn.close()

# Usage example
if __name__ == "__main__":
    db_name = 'unique_meal.db'
    schema_file = 'schema.sql'
    
    # Initialize the database
    initialize_db(db_name, schema_file)
    
    # Add default super admin
    add_default_super_admin(db_name)
