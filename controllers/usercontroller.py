import logging
import uuid
from flask import g, render_template, request, jsonify
from common.error import AppError
from models.admin import Admin, db
from services.userservice import UserService

class UserController:

    def __init__(self,app):
        self.app = app
        self.user_service = UserService()
        self.user_routes()

    def user_routes(self):

        @self.app.route('/user/login')
        def user_home():
            return render_template('userlogin.html')
        
        
        @self.app.route('/user/register')
        def user_register():
            return render_template('usercreate.html')


        @self.app.route('/v1/user/login', methods=['POST'])
        def user_login():
            try:
                username = request.form.get('username')
                password = request.form.get('password')

                logging.info(f'Login request for user {username}')

                if len(username) == 0 or username is None or len(password) == 0 or password is None:
                    raise AppError("Invalid request", AppError.INVALID_REQUEST)
                
                isSuccess = self.user_service.user_login(username, password)

                if not isSuccess:
                    raise AppError("Invalid credentials", AppError.INVALID_CREDENTIALS)
                    
                response = {"message": "Login successful"}
                return response, 200
            
            except AppError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": "Timeout error occurred while processing login request"}), 504

            except Exception as e:
                return jsonify({"error": f"Error occurred while processing login request"}), 500
            

        @self.app.route('/v1/user/create', methods=['POST'])
        def user_create():
            try:
                create_request = request.form
                username = create_request.get('username')
                email = create_request.get('email')

                logging.info(f'Create user request for {username}')

                if len(username) == 0 or username is None or len(email) == 0 or email is None:
                    raise AppError("Invalid request", AppError.INVALID_REQUEST)

                user = self.user_service.create_user(create_request)

                if user is None:
                    raise AppError("User creation failed", AppError.INTERNAL_SERVER_ERROR)
                
                return render_template('userlogin.html', message = "User created successfully"), 201
                
            except AppError as e:
                return jsonify(e.to_dict()), e.status_code
              
            except TimeoutError as e:      
                return jsonify({"error": "Timeout error occurred while processing user creation request"}), 504

            except Exception as e:
                return jsonify({"error": "Error occurred while processing user creation request"}), 500