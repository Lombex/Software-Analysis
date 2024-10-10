import os
import shutil
import datetime
import zipfile

class Backup:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name
        self.backup_dir = 'backups'
        self.log_file = 'encrypted_log.bin'

    def create_backup(self):
        try:
            os.makedirs(self.backup_dir, exist_ok=True)

            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            backup_name = f"backup_{timestamp}.zip"
            backup_path = os.path.join(self.backup_dir, backup_name)

            with zipfile.ZipFile(backup_path, 'w') as zipf:
                zipf.write(self.db_name, os.path.basename(self.db_name))
                zipf.write(self.log_file, os.path.basename(self.log_file))

            print(f"Backup created successfully: {backup_name}")
            return True

        except FileNotFoundError:
            print(f"Error: Database file '{self.db_name}' or log file '{self.log_file}' not found.")
            return False

        except Exception as e:
            print(f"An error occurred during backup: {e}")
            return False

    def restore_backup(self, backup_name):
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            if os.path.exists(backup_path):
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall()
                print(f"Backup '{backup_name}' restored successfully.")
                return True
            else:
                raise FileNotFoundError(f"Backup file '{backup_name}' not found.")

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return False

        except Exception as e:
            print(f"An error occurred during restore: {e}")
            return False

    def list_backups(self):
        try:
            backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.zip')]
            return sorted(backups, reverse=True)
        except Exception as e:
            print(f"An error occurred while listing backups: {e}")
            return []