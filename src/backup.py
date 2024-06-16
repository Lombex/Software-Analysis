import sqlite3
import os
import shutil
import datetime

class Backup:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def create_backup(self):
        try:
            # Construct backup file name with timestamp
            backup_name = f"{self.db_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bak"

            # Perform backup using shutil.copy
            shutil.copy(self.db_name, backup_name)

            print(f"Backup created successfully: {backup_name}")
        
        except FileNotFoundError:
            print(f"Error: Database file '{self.db_name}' not found.")

        except Exception as e:
            print(f"An error occurred during backup: {e}")

    def restore_backup(self, backup_name):
        try:
            # Check if backup file exists
            if os.path.exists(backup_name):
                # Perform restore using shutil.copy
                shutil.copy(backup_name, self.db_name)
                print(f"Backup '{backup_name}' restored successfully.")
            else:
                raise FileNotFoundError(f"Backup file '{backup_name}' not found.")

        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"An error occurred during restore: {e}")
