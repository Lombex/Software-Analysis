import sqlite3
from datetime import datetime

def log_activity(username, activity, additional_info='', suspicious='No'):
    conn = sqlite3.connect('unique_meal.db')
    c = conn.cursor()
    
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    
    c.execute("INSERT INTO logs (date, time, username, activity, additional_info, suspicious) VALUES (?, ?, ?, ?, ?, ?)",
              (date, time, username, activity, additional_info, suspicious))
    
    conn.commit()
    conn.close()
