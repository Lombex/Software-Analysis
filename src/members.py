import sqlite3
import random
from datetime import datetime
from database import Database

class Member:
    def __init__(self, first_name, last_name, age, gender, weight, address, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.weight = weight
        self.address = address
        self.email = email
        self.phone = phone
        self.registration_date = datetime.now().strftime("%Y-%m-%d")
        self.membership_id = self.generate_membership_id()

    def generate_membership_id(self):
        id_base = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        checksum = sum(int(digit) for digit in id_base) % 10
        return id_base + str(checksum)

    @staticmethod
    def add_member(first_name, last_name, age, gender, weight, address, email, phone):
        db = Database()
        member = Member(first_name, last_name, age, gender, weight, address, email, phone)
        with db.conn:
            db.conn.execute("""
            INSERT INTO members (first_name, last_name, age, gender, weight, address, email, phone, registration_date, membership_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (member.first_name, member.last_name, member.age, member.gender, member.weight, member.address, member.email, member.phone, member.registration_date, member.membership_id))
        db.close()
