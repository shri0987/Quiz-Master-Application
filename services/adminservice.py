import re
import uuid
import logging
from datetime import datetime

from models.admin import Admin
from common.error import AppError
from repository.adminrepository import AdminRepository
logging.basicConfig(filename='app.log', level=logging.INFO) 

class AdminService:
    pass