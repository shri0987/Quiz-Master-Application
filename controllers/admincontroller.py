import logging
import requests
from common.error import AppError
from models.admin import Admin, db
from services.adminservice import AdminService
from flask import flash, redirect, render_template, request, jsonify, session, url_for

class AdminController:

    def __init__(self,app):
        self.app = app
        self.admin_service = AdminService()
        self.admin_routes()

    def admin_routes(self):

        @self.app.route('/admin/login')
        def admin_home():
            return render_template('adminlogin.html')
        
        
        @self.app.route('/admin/dashboard/<username>', methods=['GET'])
        def admin_dashboard(username):
            try:
                logging.info(f'Admin dashboard request for {username}') 
                if 'admin_user' not in session or session['admin_user'] != username:
                    flash("Login required", "error")
                    return redirect(url_for('admin_home'))

                base_url = self.app.config['URL']
                subjects = requests.get(f'{base_url}/v1/subjects')
                logging.info(f'Subjects fetched for admin dashboard {jsonify(subjects)}')

                return render_template('admindashboard.html', username=username, subjects = subjects)
            
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
            
                return redirect(url_for('admin_dashboard', username=username))
            
            except AppError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing admin login request {e}"}), 504

            except Exception as e:
                return jsonify({"error": f"Error occurred while processing admin login request {e}"}), 500
            
        
       