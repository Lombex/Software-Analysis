import sqlite3
import datetime

class Logger:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def log_activity(self, username, activity):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        c.execute("INSERT INTO logs (date, time, username, activity) VALUES (?, ?, ?, ?)", (date, time, username, activity))
        conn.commit()
        conn.close()

    def fetch_logs(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM logs")
        logs = c.fetchall()
        conn.close()
        return logs
