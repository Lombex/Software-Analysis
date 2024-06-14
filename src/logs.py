import sqlite3
from datetime import datetime
from database import Database

class Logger:
    def __init__(self):
        self.db = Database()

    def log_activity(self, username, activity, additional_info="", suspicious=0):
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        with self.db.conn:
            self.db.conn.execute("""
            INSERT INTO logs (date, time, username, activity, additional_info, suspicious)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (date, time, username, activity, additional_info, suspicious))

    def fetch_logs(self):
        logs = self.db.conn.execute("SELECT * FROM logs").fetchall()
        return logs
