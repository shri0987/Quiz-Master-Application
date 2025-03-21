class ApplicationError(Exception):
    INVALID_REQUEST = ('ERROR1000', 400)
    INVALID_CREDENTIALS = ('ERROR1001', 400)
    USER_NOT_FOUND = ('ERROR1002', 404)
    USER_EXISTS = ('ERROR1005', 400)
    USER_NOT_FOUND = ('ERROR1006', 404)
    SUBJECTS_NOT_FOUND = ('ERROR1007', 404)
    SUBJECT_EXISTS = ('ERROR1008', 400)
    CHAPTER_EXISTS = ('ERROR1010', 400)
    CHAPTERS_NOT_FOUND  = ('ERROR1011',404)
    QUIZ_NOT_FOUND = ('ERROR1012', 404)
    UNAUTHORIZED = ('ERROR1009', 403)
    VALIDATION_ERROR = ('ERROR1003', 400)

    INTERNAL_SERVER_ERROR = ('ERROR1004', 500)

    def __init__(self, error_message, error_code_tuple):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_code, self.status_code = error_code_tuple

    def to_dict(self):
        return {"error": self.error_message, "code": self.error_code}
