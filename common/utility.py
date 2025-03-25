import uuid
from flask import app
from datetime import datetime

class Utility:

    def generate_current_datetime(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_guid_id(self) -> str:
        return str(uuid.uuid4())
    
    def get_date_object(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, "%Y-%m-%d")
    
    def get_current_date(self) -> datetime:
        return datetime.now()