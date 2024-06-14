import shutil
import os
from datetime import datetime

class Backup:
    def __init__(self, db_name="unique_meal.db"):
        self.db_name = db_name

    def create_backup(self):
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
        shutil.make_archive(backup_name, 'zip', '.', self.db_name)
        print(f"Backup created: {backup_name}")

    def restore_backup(self, backup_name):
        shutil.unpack_archive(backup_name, '.')
        print(f"Backup restored from: {backup_name}")
