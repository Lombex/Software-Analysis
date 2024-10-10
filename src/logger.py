import sqlite3
import datetime
import base64
import os
import json

class Logger:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.salt = self.load_or_generate_salt()
        self.log_file = 'encrypted_log.bin'

    def load_or_generate_salt(self):
        salt_file = 'log_salt.bin'
        if os.path.exists(salt_file):
            with open(salt_file, 'rb') as file:
                return file.read()
        else:
            salt = os.urandom(16)
            with open(salt_file, 'wb') as file:
                file.write(salt)
            return salt

    def encrypt(self, data):
        return base64.b64encode(bytes([b ^ self.salt[i % len(self.salt)] for i, b in enumerate(data.encode())]))

    def decrypt(self, data):
        decoded = base64.b64decode(data)
        return bytes([b ^ self.salt[i % len(self.salt)] for i, b in enumerate(decoded)]).decode()

    def log_activity(self, username, activity, additional_info='', suspicious='No'):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "username": username,
            "activity": activity,
            "additional_info": additional_info,
            "suspicious": suspicious
        }

        encrypted_entry = self.encrypt(json.dumps(log_entry))

        with open(self.log_file, 'ab') as f:
            f.write(encrypted_entry + b'\n')

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("""
                INSERT INTO logs (date, time, username, activity, additional_info, suspicious)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                timestamp.split()[0],
                timestamp.split()[1],
                username,
                activity,
                additional_info,
                suspicious
            ))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    def fetch_logs(self):
        logs = []
        with open(self.log_file, 'rb') as f:
            for line in f:
                try:
                    decrypted_line = self.decrypt(line.strip())
                    log_entry = json.loads(decrypted_line)
                    logs.append(log_entry)
                except:
                    continue
        return logs

    def get_recent_suspicious_activities(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("""
                SELECT * FROM logs
                WHERE suspicious = 'Yes'
                ORDER BY date DESC, time DESC
                LIMIT 10
            """)
            return c.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            conn.close()

    def detect_suspicious_activity(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            five_minutes_ago = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""
                SELECT COUNT(*) FROM logs
                WHERE username = ? AND activity = 'Login Attempt'
                AND datetime(date || ' ' || time) > datetime(?)
            """, (username, five_minutes_ago))
            login_attempts = c.fetchone()[0]
            return login_attempts > 5
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            conn.close()

    def alert_unread_suspicious_activities(self):
        recent_suspicious = self.get_recent_suspicious_activities()
        if recent_suspicious:
            print("ALERT: There are unread suspicious activities!")
            print("Recent suspicious activities:")
            for activity in recent_suspicious:
                print(f"Date: {activity[1]}, Time: {activity[2]}, User: {activity[3]}, Activity: {activity[4]}")
        else:
            print("No recent suspicious activities.")