from flask import render_template, request, jsonify
from models.admin import Admin, db
from services.adminservice import AdminService

class AdminController:

    def __init__(self,app):
        self.app = app
        self.admin_service = AdminService()
        self.admin_routes()

    def admin_routes(self):
        pass
