class AppError(Exception):
    """Base error for the task-manager application."""


class NotFoundError(AppError):
    """Raised when a requested object cannot be found."""


class ValidationError(AppError):
    """Raised when supplied data is invalid."""
