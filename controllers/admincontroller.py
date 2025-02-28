import logging
from flask import render_template, request, jsonify
from common.error import AppError
from models.admin import Admin, db
from services.adminservice import AdminService

class AdminController:

    def __init__(self,app):
        self.app = app
        self.admin_service = AdminService()
        self.admin_routes()

    def admin_routes(self):

        @self.app.route('/admin/login')
        def admin_home():
            return render_template('adminlogin.html')
        
        
        @self.app.route('/v1/admin/login', methods=['POST'])
        def admin_login():
            try:
                username = request.form.get('username')
                password = request.form.get('password')

                logging.info(f'Login request for admin {username}')

                if len(username) == 0 or username is None or len(password) == 0 or password is None:
                    raise AppError("Invalid request", AppError.INVALID_REQUEST)
                
                isSuccess = self.admin_service.admin_login(username, password)

                if not isSuccess:
                    raise AppError("Invalid credentials", AppError.INVALID_CREDENTIALS)
                    
                response = {"message": "Login successful"}
                return response, 200
            
            except AppError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": "Timeout error occurred while processing admin login request"}), 504

            except Exception as e:
                return jsonify({"error": f"Error occurred while processing admin login request"}), 500
            
