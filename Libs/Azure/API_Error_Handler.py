class APIError(Exception):
    def __init__(self, message, status_code=400, charset="utf-8"):
        self.message = message
        self.status_code = status_code
        self.charset = charset
        super().__init__(message)

class APISuccess(Exception):
    def __init__(self, message, status_code=200, charset="utf-8"):
        self.message = message
        self.status_code = status_code
        self.charset = charset
        super().__init__(message)
