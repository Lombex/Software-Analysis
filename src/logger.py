import sqlite3
import datetime
import re
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

class Logger:
    def __init__(self, db_name='unique_meal.db', private_key_path='src/private_key.pem'):
        self.db_name = db_name
        self.private_key = self.load_private_key(private_key_path)

    # Method to load the private key
    def load_private_key(self, private_key_path):
        with open(private_key_path, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
        return private_key

    # Method to decrypt encrypted data
    def decrypt_field(self, encrypted_data):
        try:
            decrypted_data = self.private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted_data.decode('utf-8')  # Convert from bytes to string
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

    def log_activity(self, username, activity, additional_info='', suspicious='No'):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        c.execute("INSERT INTO logs (date, time, username, activity, additional_info, suspicious) VALUES (?, ?, ?, ?, ?, ?)", 
                  (date, time, username, activity, additional_info, suspicious))
        conn.commit()
        conn.close()

    def fetch_logs(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM logs")
        logs = c.fetchall()

        # Decrypt usernames in the logs
        decrypted_logs = []
        for log in logs:
            decrypted_username = self.decrypt_field(log[3]) if log[3] else log[3]  # Assuming username is at index 3
            decrypted_logs.append((log[0], log[1], decrypted_username, log[4], log[5], log[6]))  # Rebuild log tuple with decrypted username

        conn.close()
        return decrypted_logs

    def detect_suspicious_activity(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        five_minutes_ago = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        c.execute("SELECT COUNT(*) FROM logs WHERE username = ? AND activity = 'Login Attempt' AND date || ' ' || time > ?", 
                  (username, five_minutes_ago))
        login_attempts = c.fetchone()[0]
        conn.close()
        return login_attempts > 5