import sqlite3
import os
import shutil
import datetime

class Backup:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.backup_dir = 'backups'

    def create_backup(self):
        try:
            # Create backup directory if it doesn't exist
            os.makedirs(self.backup_dir, exist_ok=True)

            # Construct backup file name with timestamp
            backup_name = f"{os.path.basename(self.db_name)}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bak"

            # Perform backup using shutil.copy
            shutil.copy(self.db_name, os.path.join(self.backup_dir, backup_name))

            print(f"Backup created successfully: {backup_name}")

        except FileNotFoundError:
            print(f"Error: Database file '{self.db_name}' not found.")

        except Exception as e:
            print(f"An error occurred during backup: {e}")

    def restore_backup(self, backup_name):
        try:
            # Check if backup file exists
            backup_path = os.path.join(self.backup_dir, backup_name)
            if os.path.exists(backup_path):
                # Perform restore using shutil.copy
                shutil.copy(backup_path, self.db_name)
                print(f"Backup '{backup_name}' restored successfully.")
            else:
                raise FileNotFoundError(f"Backup file '{backup_name}' not found.")

        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"An error occurred during restore: {e}")