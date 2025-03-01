from datetime import datetime
import uuid

class Utility:

    def generate_current_datetime(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_guid_id(self) -> str:
        return str(uuid.uuid4())