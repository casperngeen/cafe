class AppError(Exception):
    """Base class for all custom exceptions"""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {"success": False, "error": self.message}


class DatabaseError(AppError):
    """Raised when a database error occurs"""
    def __init__(self, message="A database error occurred"):
        super().__init__(message, status_code=500)


class NotFoundError(AppError):
    """Raised when a resource is not found"""
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)


class ValidationError(AppError):
    """Raised when there is a validation error"""
    def __init__(self, message="Invalid input provided"):
        super().__init__(message, status_code=400)