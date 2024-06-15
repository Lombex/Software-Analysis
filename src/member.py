import sqlite3
from datetime import datetime

class Member:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def generate_membership_id(self):
        current_year = datetime.now().year
        return f"{current_year % 100:02d}{datetime.now().strftime('%m%d%H%M%S')}"

    def add_member(self, first_name, last_name, age, gender, weight, address, email, phone):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Generate membership ID
        membership_id = self.generate_membership_id()

        # Calculate checksum
        checksum = sum(int(digit) for digit in membership_id[:9]) % 10
        membership_id += str(checksum)

        # Insert member into database
        c.execute("INSERT INTO members (membership_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (membership_id, first_name, last_name, age, gender, weight, address, email, phone, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        
        return membership_id

    def get_member(self, member_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM members WHERE id=?", (member_id,))
        member = c.fetchone()
        conn.close()
        return member

    def update_member(self, member_id, first_name=None, last_name=None, age=None, gender=None, weight=None, address=None, email=None, phone=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Create SET clause based on provided fields
        set_clause = []
        if first_name:
            set_clause.append(f"first_name='{first_name}'")
        if last_name:
            set_clause.append(f"last_name='{last_name}'")
        if age:
            set_clause.append(f"age={age}")
        if gender:
            set_clause.append(f"gender='{gender}'")
        if weight:
            set_clause.append(f"weight={weight}")
        if address:
            set_clause.append(f"address='{address}'")
        if email:
            set_clause.append(f"email='{email}'")
        if phone:
            set_clause.append(f"phone='{phone}'")

        set_clause = ', '.join(set_clause)
        query = f"UPDATE members SET {set_clause} WHERE id=?"
        c.execute(query, (member_id,))
        conn.commit()
        conn.close()

    def delete_member(self, member_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM members WHERE id=?", (member_id,))
        conn.commit()
        conn.close()

    def list_members(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM members")
        members = c.fetchall()
        conn.close()
        return members
