from typing import Optional
from .app_errors import AppError


class LLMAPIUnauthorizedAccessError(AppError):
    code = "LLMAPI_UnauthorizedAccess"
    message = "Unauthorized access to LLM API"

    def __init__(self, cause: Optional[Exception] = None):
        super().__init__(cause=cause)


class LLMAPIUnavailableError(AppError):
    code = "LLMAPI_Unavailable"
    message = "LLM API is not available"

    def __init__(self, cause: Optional[Exception] = None):
        super().__init__(cause=cause)
