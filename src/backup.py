import sqlite3
import os
import shutil
import datetime
import zipfile

class Backup:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.backup_dir = 'src/backups'

    def create_backup(self):
        try:
            # Create backup directory if it doesn't exist
            os.makedirs(self.backup_dir, exist_ok=True)

            # Construct backup file name with timestamp
            backup_name = f"{os.path.basename(self.db_name)}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
            backup_path = os.path.join(self.backup_dir, backup_name)

            # Perform backup using shutil.copy
            shutil.copy(self.db_name, backup_path)

            # Create a zip file for the backup
            zip_name = backup_name.replace('.bak', '.zip')
            zip_path = os.path.join(self.backup_dir, zip_name)

            with zipfile.ZipFile(zip_path, 'w') as zipf:
                zipf.write(backup_path, os.path.basename(backup_path))

            # Remove the original backup file after zipping
            os.remove(backup_path)

            print(f"Backup created and zipped successfully: {zip_name}")

        except FileNotFoundError:
            print(f"Error: Database file '{self.db_name}' not found.")

        except Exception as e:
            print(f"An error occurred during backup: {e}")

    def restore_backup(self, zip_name):
        try:
            # Check if zip backup file exists
            zip_path = os.path.join(self.backup_dir, zip_name)
            if os.path.exists(zip_path):
                # Extract the backup from the zip file
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    zipf.extractall(self.backup_dir)

                # Get the extracted backup file path
                backup_name = zip_name.replace('.zip', '.bak')
                backup_path = os.path.join(self.backup_dir, backup_name)

                # Perform restore using shutil.copy
                shutil.copy(backup_path, self.db_name)

                # Optionally, remove the extracted .bak file after restoration
                os.remove(backup_path)

                print(f"Backup '{zip_name}' restored successfully.")
            else:
                raise FileNotFoundError(f"Zip backup file '{zip_name}' not found.")

        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"An error occurred during restore: {e}")