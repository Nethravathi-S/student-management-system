import json
import os
from typing import List, Dict, Optional

class FileHandler:
    def __init__(self, filename="students_data.json"):
        self.filename = filename
    
    def read_data(self) -> Dict:
        if not os.path.exists(self.filename):
            return {"students": [], "last_id": 0}
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading file: {e}")
            return {"students": [], "last_id": 0}
    
    def write_data(self, data: Dict) -> bool:
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False
    
    def backup_data(self):
        try:
            if os.path.exists(self.filename):
                backup_filename = f"{self.filename}.backup"
                with open(self.filename, 'r', encoding='utf-8') as source:
                    with open(backup_filename, 'w', encoding='utf-8') as dest:
                        dest.write(source.read())
                return True
        except Exception as e:
            print(f"Backup failed: {e}")
            return False
