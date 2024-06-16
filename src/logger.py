import sqlite3
import datetime
import re

class Logger:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def log_activity(self, username, activity, additional_info='', suspicious='No'):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        c.execute("INSERT INTO logs (date, time, username, activity, additional_info, suspicious) VALUES (?, ?, ?, ?, ?, ?)", (date, time, username, activity, additional_info, suspicious))
        conn.commit()
        conn.close()

    def fetch_logs(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM logs")
        logs = c.fetchall()
        conn.close()
        return logs
    
    def detect_suspicious_activity(self, username):
        # Added: Method to detect suspicious activity
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        five_minutes_ago = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        c.execute("SELECT COUNT(*) FROM logs WHERE username = ? AND activity = 'Login Attempt' AND date || ' ' || time > ?", (username, five_minutes_ago))
        login_attempts = c.fetchone()[0]
        conn.close()
        return login_attempts > 5

    def detect_sql_injection(self, input_string):
        # Added: Method to detect SQL injection
        sql_injection_patterns = [
            r"(\%27)|(\')|(\-\-)|(\%23)|(#)",  # Single quote, comment
            r"(\%22)|(\")|(\%3B)|(;)",  # Double quote, semicolon
            r"(\%28)|(\()|(\%29)|(\))",  # Parentheses
            r"(\%20)|(\s)",  # Space
            r"union\s+select",  # UNION SELECT
            r"select\s+\*",  # SELECT *
            r"insert\s+into",  # INSERT INTO
            r"drop\s+table",  # DROP TABLE
            r"update\s+set",  # UPDATE SET
            r"delete\s+from",  # DELETE FROM
            r"or\s+1=1",  # OR 1=1
            r"or\s+'1'='1'",  # OR '1'='1'
            r"--",  # Comment
            r"xp_cmdshell",  # xp_cmdshell (SQL Server)
            r"exec\s+\(",  # EXEC(
            r"exec\s+",  # EXEC
            r"union\s+all\s+select",  # UNION ALL SELECT
            r"information_schema.tables",  # INFORMATION_SCHEMA
            r"load_file\(",  # LOAD_FILE
            r"into\s+outfile",  # INTO OUTFILE
            r"benchmark\(",  # BENCHMARK
            r"sleep\(",  # SLEEP
            r"' or 'x'='x",  # ' OR 'x'='x
            r"' OR '1",  # ' OR '1
            r'" OR "1',  # " OR "1
            r") OR (1=1",  # ) OR (1=1
        ]
        for pattern in sql_injection_patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                return True
        return False