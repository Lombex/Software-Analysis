import sqlite3
from datetime import datetime
import random

def register_member(first_name, last_name, age, gender, weight, address, email, phone):
    conn = sqlite3.connect('unique_meal.db')
    c = conn.cursor()
    
    membership_id = generate_membership_id()
    
    c.execute("INSERT INTO members (first_name, last_name, age, gender, weight, address, email, phone, registration_date, membership_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (first_name, last_name, age, gender, weight, address, email, phone, datetime.now().strftime("%Y-%m-%d"), membership_id))
    
    conn.commit()
    conn.close()

def generate_membership_id():
    year = datetime.now().year % 100
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    checksum = (sum(int(digit) for digit in str(year) + random_digits) % 10)
    return f"{year}{random_digits}{checksum}"
