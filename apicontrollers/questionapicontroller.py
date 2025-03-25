import logging
import requests
from common.error import ApplicationError
from models.question import Question, db
from services.questionservice import QuestionService
from flask import redirect, render_template, request, jsonify, session, url_for

class QuestionController:

    def __init__(self, app):
        self.app = app
        self.question_service = QuestionService()
        self.question_api_routes()

    def question_api_routes(self):

        @self.app.route('/<quiz_id>/question/<question_id>', methods=['GET'])
        def render_question_page(quiz_id, question_id):
            try:
                base_url = self.app.config["URL"]
                response = requests.get(f'{base_url}/api/v1/question/info/{question_id}')

                if response.status_code != 200:
                    logging.error(f"Failed to fetch question: {response.text}")
                    return f"Error fetching question: {response.text}", response.status_code
                
                question_data = response.json()
                
                return render_template('updatequestionpage.html', quiz_id = quiz_id, question=question_data, username=session.get('admin_username'))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('quizdetails.html', error_message=error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('quizdetails.html', error_message="Operation Timed out"), 504
            
            except Exception as e:
                return render_template('quizdetails.html', error_message="Error occurred while processing request"), 500


        @self.app.route('/<quiz_id>/question/create', methods=['GET'])
        def render_question_create_page(quiz_id):
            try:
                username = session.get('admin_username')
                if username is None:
                    redirect(url_for('render_admin_login_page'))

                return render_template('createquestionpage.html', username = username, quiz_id=quiz_id)
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('quizdetails.html', error_message=error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('quizdetails.html', error_message="Operation Timed out"), 504
            
            except Exception as e:
                return render_template('quizdetails.html', error_message="Error occurred while processing request"), 500
            
        
        @self.app.route('/api/v1/question/<quiz_id>', methods=['GET'])
        def get_questions_by_quiz_id(quiz_id):
            try:
                logging.info(f'Start fetching questions using {quiz_id}') 

                questions = self.question_service.get_questions_by_quiz_id(quiz_id)

                if questions is None:
                    raise ApplicationError("Error occurred while fetching questions", ApplicationError.INTERNAL_SERVER_ERROR)
                
                return jsonify(questions), 200
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing request {e}"}), 500


        @self.app.route('/api/v1/question/info/<question_id>', methods=['GET'])
        def get_question_by_question_id(question_id): 
            try:
                logging.info(f'Start fetching question {question_id}') 

                question = self.question_service.get_question_by_question_id(question_id)

                if question is None:
                    raise ApplicationError("Error occurred while fetching question", ApplicationError.INTERNAL_SERVER_ERROR)
                
                return jsonify(question), 200
            
            except ApplicationError as e:
                return jsonify(e.to_dict()), e.status_code
            
            except TimeoutError as e:
                return jsonify({"error": f"Timeout error occurred while processing request {e}"}), 504
            
            except Exception as e:
                return jsonify({"error": f"Error occurred while processing request {e}"}), 500


        @self.app.route('/api/v1/<quiz_id>/question/create', methods=['POST'])
        def create_question(quiz_id):
            try:
                logging.info(f'Create question request by {session.get("admin_username")} for quiz {quiz_id}')

                question_statement = request.form.get('questionStatement')
                option1 = request.form.get('option1')
                option2 = request.form.get('option2')
                option3 = request.form.get('option3')
                option4 = request.form.get('option4')
                correct_option = request.form.get('correctOption')
                marks = request.form.get('marks')

                username = session.get ('admin_user')

                if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option or not marks:
                    raise ApplicationError("Invalid Request", ApplicationError.INVALID_REQUEST)
               
                question = self.question_service.create_question(quiz_id, question_statement, option1, option2, option3, option4, correct_option, marks)

                if question is None:
                    raise ApplicationError("Error occurred while creating question", ApplicationError.INTERNAL_SERVER_ERROR)

                return redirect(url_for('render_quiz_page_by_id', username = username, quiz_id=quiz_id))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('createquestionpage.html', error_message=error_details["error"]), e.status_code
            
            except TimeoutError as e:
                return render_template('createquestionpage.html', error_message="Operation Timed out"), 504
            
            except Exception as e:
                return render_template('createquestionpage.html', error_message="Error occurred while processing request"), 500
        

        @self.app.route('/api/v1/<quiz_id>/question/<question_id>/update', methods=['POST'])
        def update_question(quiz_id, question_id):
            try:
                question_statement = request.form.get('questionStatement')
                option1 = request.form.get('option1')
                option2 = request.form.get('option2')
                option3 = request.form.get('option3')
                option4 = request.form.get('option4')
                correct_option = request.form.get('correctOption')
                marks = request.form.get('marks')
                username = session.get('admin_username')

                if not username:
                    logging.info(f'session expired')
                    return redirect(url_for('render_admin_login_page'))

                logging.info(f'Start updating question {question_statement} and id {question_id} by user {username}')

                if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option or not marks:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                question = self.question_service.update_question(quiz_id, question_id, question_statement, option1, option2, option3, option4, correct_option, marks)

                if question is None:
                    raise ApplicationError("Error occurred while updating question", ApplicationError.INTERNAL_SERVER_ERROR)
    
                return redirect(url_for('render_quiz_page_by_id', quiz_id = quiz_id))
            
            except ApplicationError as e:
                error_details = e.to_dict()

            except TimeoutError:
                error_details = {"error": "Operation Timed out"}

            except Exception:
                error_details = {"error": "Error occurred while processing update request"}

            existing_question = self.question_service.get_question_by_question_id(question_id)
            username = session.get('admin_username')

            if existing_question is None:
                return render_template('updatequestionpage.html', error_message=error_details["error"]), 500

            return render_template('updatequestionpage.html', quiz_id = existing_question.get('quizId'), question=existing_question, username = username, error_message=error_details["error"])
            

        @self.app.route('/api/v1/<quiz_id>/question/delete/<question_id>', methods=['POST'])
        def delete_question(quiz_id, question_id):
            question = None
            try:
                username = session.get('admin_username')
                if not username:
                    raise ApplicationError("Username is required", ApplicationError.INVALID_REQUEST)
                
                logging.info(f'Start deleting question request {question_id} by {username}')

                if not question_id:
                    raise ApplicationError("Invalid request", ApplicationError.INVALID_REQUEST)
                
                question = self.question_service.delete_question(question_id)

                if question is None:
                    raise ApplicationError("Error occurred while deleting question", ApplicationError.INTERNAL_SERVER_ERROR)

                return redirect(url_for('render_quiz_page_by_id', quiz_id = quiz_id))
            
            except ApplicationError as e:
                error_details = e.to_dict()
                return render_template('updatequestionpage.html', error_message=error_details["error"], question=question), e.status_code
            
            except TimeoutError as e:
                return render_template('updatequestionpage.html', error_message="Operation Timed out", question=question), 504
            
            except Exception as e:
                return render_template('updatequestionpage.html', error_message="Error occurred while processing request", question=question), 500