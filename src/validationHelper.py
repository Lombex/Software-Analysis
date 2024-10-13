import sqlite3
import datetime
from validation import validate_username, validate_password, validate_email, validate_age, validate_weight, validate_phone

class InputValidationUtility:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def detect_suspicious_activity(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        five_minutes_ago = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        c.execute("SELECT COUNT(*) FROM logs WHERE username = ? AND activity = 'Input Attempt' AND date || ' ' || time > ?", (username, five_minutes_ago))
        input_attempts = c.fetchone()[0]
        conn.close()
        return input_attempts > 5
    
    def detect_sql_injection(self, input_string):
        # List of SQL injection keywords
        sql_injection_keywords = [
            "#", ";",  # comment and semicolon
            "%28", "(", "%29", ")",  # Parentheses
            "%20", " ",  # Space
            "union select",  # Union select
            "select *",  # Select all
            "insert into",  # Insert statement
            "drop table",  # Drop table
            "update set",  # Update statement
            "delete from",  # Delete statement
            "or 1=1",  # OR condition
            "or '1'='1'",  # OR condition with quotes
            "--",  # Comment
            "xp_cmdshell",  # Command execution
            "exec(",  # Execution
            "exec ",  # Execution
            "union all select",  # Union all select
            "information_schema.tables",  # Information schema
            "load_file(",  # Load file
            "into outfile",  # Output file
            "benchmark(",  # Benchmark function
            "sleep(",  # Sleep function
            "' or 'x'='x",  # OR condition with quotes
            "' OR '1",  # OR condition with quotes
            '" OR "1',  # OR condition with quotes
            ") OR (1=1",  # OR condition with parentheses
        ]

        # Normalize the input string to lower case for case-insensitive comparison
        input_string = input_string.lower()

        # Check if any of the keywords are in the input string
        for keyword in sql_injection_keywords:
            if keyword == input_string:
                return True  # SQL injection detected

        return False  # No SQL injection detected

    def log_input_attempt(self, username, input_type, suspicious=False, value = None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        now = datetime.datetime.now()
        activity = f"Suspicious Activity Detected. User entered: {value}" if suspicious else f"Input Attempt: {input_type}"
        c.execute("INSERT INTO logs (username, activity, date, time) VALUES (?, ?, ?, ?)",
                  (username, activity, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")))
        conn.commit()
        conn.close()

    def validate_input(self, input_type, value):
        """
        Validate input based on the specified input type.
        
        :param input_type: Type of input to validate
        :param value: The input value to validate
        :return: (bool, str) A tuple containing a boolean indicating if the input is valid,
                 and a string containing an error message if invalid (or empty string if valid)
        """
        if input_type == 'username':
            is_valid, message = validate_username(value)
            return is_valid, message
        
        elif input_type == 'password':
            is_valid, message = validate_password(value)
            return is_valid, message
        
        elif input_type == 'email':
            is_valid, message = validate_email(value)
            return is_valid, message
        
        elif input_type == 'age':
            is_valid, message = validate_age(value)
            return is_valid, message
        
        elif input_type == 'weight':
            is_valid, message = validate_weight(value)
            return is_valid, message
        
        elif input_type == 'phone':
            is_valid, message = validate_phone(value)
            return is_valid, message
        
        elif input_type == 'name':
            if len(value.strip()) >= 2 and value.strip().isalpha():
                return True, ""
            return False, "Name must be at least 2 letters and contain only alphabetic characters."
        
        elif input_type == 'role':
            if value.lower() in ['consultant', 'system_admin']:
                return True, ""
            return False, "Role must be one of: consultant, system_admin"
        
        elif input_type == 'gender':
            if value.strip().lower() in ['male', 'female', 'other']:
                return True, ""
            return False, "Gender must be one of: male, female, other."
        
        elif input_type == 'address':
            if len(value.strip()) > 0:
                return True, ""
            return False, "Address cannot be empty."
        
        elif input_type == 'choice':
            if value.isdigit():
                return True, ""
            return False, "Choice must be a number."
        
        else:
            # For any other input type, we'll just check if it's not empty
            if len(value.strip()) > 0:
                return True, ""
            return False, f"{input_type.capitalize()} cannot be empty."

    def validate_any_inputs(self, prompt, input_type, username, skip=False):
        """
        Prompt the user for input, validate it based on the specified input type,
        and check for suspicious activity.
        
        :param prompt: The prompt to display to the user
        :param input_type: Type of input to validate
        :param username: The username of the current user (for logging and suspicious activity detection)
        :return: The validated input value
        """
        while True:
            value = prompt
            if not skip:
                value = input(prompt).strip()
            if self.detect_sql_injection(value):
                self.log_input_attempt(username, input_type, True, value)
                raise ValueError("Suspicious activity detected. Please try again later.")

            
            self.log_input_attempt(username, input_type)

            is_valid, error_message = self.validate_input(input_type, value)
            if is_valid:
                return value
            print(error_message)