import sqlite3

class Member:
    @staticmethod
    def add_member(first_name, last_name, age, gender, weight, address, email, phone, db_name='unique_meal.db'):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("INSERT INTO members (first_name, last_name, age, gender, weight, address, email, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (first_name, last_name, age, gender, weight, address, email, phone))
        conn.commit()
        conn.close()
