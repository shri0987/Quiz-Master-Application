class AppError(Exception):
    INVALID_REQUEST = ('E1000', 400)
    INVALID_CREDENTIALS = ('E1001', 400)
    USER_NOT_FOUND = ('E1002', 404)
    VALIDATION_ERROR = ('E1003', 400)
    INTERNAL_SERVER_ERROR = ('E1004', 500)
    USER_EXISTS = ('E1005', 400)
    USER_NOT_FOUND = ('E1006', 404)

    def __init__(self, error_message, error_code_tuple):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_code, self.status_code = error_code_tuple

    def to_dict(self):
        return {"error": self.error_message, "code": self.error_code}
