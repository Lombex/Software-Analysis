import sqlite3
from datetime import datetime

class Logger:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def log_activity(self, username, activity, additional_info="", suspicious=""):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        c.execute("INSERT INTO logs (date, time, username, activity, additional_info, suspicious) VALUES (?, ?, ?, ?, ?, ?)",
                  (date, time, username, activity, additional_info, suspicious))
        conn.commit()
        conn.close()

    def fetch_logs(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM logs")
        logs = c.fetchall()
        conn.close()
        return logs
