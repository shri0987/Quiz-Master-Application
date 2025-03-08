import logging
import requests
from common.error import AppError
from common.utility import Utility
from models.admin import Admin, db
from services.adminservice import AdminService
from flask import flash, redirect, render_template, request, jsonify, session, url_for

class AdminController:

    def __init__(self,app):
        self.app = app
        self.admin_service = AdminService()
        self.utility = Utility()
        self.admin_routes()

    def admin_routes(self):

        @self.app.route('/admin/login')
        def admin_home():
            return render_template('adminlogin.html')
        
        
        @self.app.route('/admin/dashboard/<username>', methods=['GET'])
        def admin_dashboard(username):
            try:
                logging.info(f'Admin dashboard request for session {session.get('admin_user')}') 
                logging.info(f'Admin dashboard request for {username}') 

                base_url = self.app.config["URL"]
                response = requests.get(f'{base_url}/v1/subjects')

                if response.status_code != 200:
                    logging.error(f"Failed to fetch subject: {response.text}")
                    return f"Error fetching subject: {response.text}", response.status_code
                
                subject_data = response.json()
                return render_template('admindashboard.html', username=username, subjects = subject_data)
            
            except AppError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing admin dashboard request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing admin dashboard request {e}"}), 500
        

        @self.app.route('/v1/admin/login', methods=['POST'])
        def admin_login():
            try:
                username = request.form.get('username')
                password = request.form.get('password')

                logging.info(f'Login request for admin {username}')

                if not username or not password:
                    raise AppError("Invalid request", AppError.INVALID_REQUEST)
                
                is_login_success = self.admin_service.admin_login(username, password)

                if not is_login_success:
                    raise AppError("Invalid credentials", AppError.INVALID_CREDENTIALS)
                
                session['admin_user'] = username
                session['is_admin_logged_in'] = True
            
                return redirect(url_for('admin_dashboard', username = username))
            
            except AppError as e:
                error_details = e.to_dict()
                return render_template('adminlogin.html', error_message = error_details["error"]), e.status_code

            except TimeoutError as e:
                return render_template('adminlogin.html', error_message = "Operation Timed out"), 504

            except Exception as e:
                return render_template('adminlogin.html', error_message = "Error occurred while processing admin login request"), 500
            
        
       