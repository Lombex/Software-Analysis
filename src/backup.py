import sqlite3
import shutil
import os

class Backup:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def create_backup(self):
        shutil.copy(self.db_name, f"{self.db_name}.backup")
        print("Backup created successfully.")

    def restore_backup(self, backup_name):
        if os.path.exists(backup_name):
            shutil.copy(backup_name, self.db_name)
            print("Backup restored successfully.")
        else:
            print("Backup file does not exist.")
