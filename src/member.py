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
        
    @staticmethod
    def search_member(criteria, value, db_name='unique_meal.db'):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        
        # Define valid criteria that can be searched
        valid_criteria = ['first_name', 'last_name', 'age', 'gender', 'weight', 'address', 'email', 'phone']
        
        if criteria in valid_criteria:
            # Use parameterized query to prevent SQL injection
            query = f"SELECT * FROM members WHERE {criteria} LIKE ?"
            c.execute(query, ('%' + value + '%',))
            result = c.fetchall()
            conn.close()
            return result
        else:
            conn.close()
            raise ValueError("Invalid search criteria")

# Example usage:
# Searching by first name
results = Member.search_member('first_name', 'jurwin')
print("Search results for first name 'John':", results)