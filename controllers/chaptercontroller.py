import logging
import requests
from common.error import AppError
from models.chapter import Chapter, db
from services.chapterservice import ChapterService
from flask import render_template, request, jsonify

class ChapterController:

    def __init__(self,app):
        self.app = app
        self.chapter_service = ChapterService()
        self.chapter_routes()

    def chapter_routes():
        pass