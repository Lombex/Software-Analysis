import sqlite3
from hashlib import sha256
from datetime import datetime
from logs import log_activity

def login(username, password):
    conn = sqlite3.connect('unique_meal.db')
    c = conn.cursor()
    
    password_hash = sha256(password.encode()).hexdigest()
    
    c.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    user = c.fetchone()
    
    conn.close()
    
    if user:
        return True, user
    else:
        return False, None

def check_permission(user_role, action):
    permissions = {
        'super_admin': ['create_user', 'delete_user', 'update_member', 'view_logs'],
        'system_admin': ['update_member', 'view_logs'],
        'consultant': ['update_member']
    }
    
    return action in permissions.get(user_role, [])

def handle_user_input():
    while True:
        print("Welcome to Unique Meal Membership Management System")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            is_authenticated, user_info = login(username, password)
            
            if is_authenticated:
                print(f"Welcome, {user_info[4]} {user_info[5]}!")
                # Additional menu for authenticated users based on role
                # Implement role-based actions here
                log_activity(username, 'login', 'User logged in successfully')
            else:
                print("Invalid username or password.")
                log_activity(username, 'login', 'Failed login attempt', 'Yes')
                
        elif choice == '2':
            # Registration logic
            print("Registration is not implemented in this example.")
            
        elif choice == '3':
            break
        
        else:
            print("Invalid choice. Please try again.")
