import sqlite3
import os
import shutil
import datetime

class Backup:
    def __init__(self, db_name='unique_meal.db'):
        self.db_name = db_name

    def create_backup(self):
        backup_name = f"{self.db_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
        shutil.copy(self.db_name, backup_name)

    def restore_backup(self, backup_name):
        if os.path.exists(backup_name):
            shutil.copy(backup_name, self.db_name)
        else:
            raise FileNotFoundError("Backup file not found")
