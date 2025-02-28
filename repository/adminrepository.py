import sqlite3
import logging
from models.admin import Admin
from models.user import User
logging.basicConfig(filename='app.log', level=logging.INFO) 

class AdminRepository:
    
    def get_admin_by_username(self, username) -> User:
        try:
            conn = sqlite3.connect('instance/quizmasterapp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admins WHERE userName = ?", (username,))
            result = cursor.fetchone()
            if result is None:
                return None
            admin = Admin(*result)
            logging.info("Admin %s fetched successfully", username)
            return admin
                
        except sqlite3.Error as e:
            logging.error("Database error in fetch admin : %s", e)
            raise Exception("Database error occured while executing SQL query")
        
        except Exception as e:
            logging.error("Error occured in fetch admin : %s", e)
            raise Exception("Error occured in fetch admin")
        
        finally:
            conn.close()
