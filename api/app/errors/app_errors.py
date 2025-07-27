from abc import ABC
from typing import Optional


class AppError(Exception, ABC):
    code: str
    message: str
    cause: Optional[Exception]

    def __init__(self, message: str = None, cause: Optional[Exception] = None):
        self.message = message or getattr(self, "message", "")
        self.cause = cause
        super().__init__(self.message)

    def __str__(self):
        return f"{self.code}: {self.message}{f"\nCause: {self.cause}" if self.cause else ""}"


class TechnicalError(AppError):
    code = "Technical"

    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message=message, cause=cause)
