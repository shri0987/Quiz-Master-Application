import logging
from flask import jsonify
from common.utility import Utility
from models.subject import Subject
from common.error import AppError
from repository.chapterrepository import ChapterRepository
logging.basicConfig(filename='app.log', level=logging.INFO) 

class ChapterService:
    
    def __init__(self):
        self.subject_repository = ChapterRepository()
        self.utility = Utility()