from datetime import datetime
from pydantic import ValidationError
from mistralai import Mistral
from mistralai.models import (
    Messages as ChatCompletionRequestMessages,
    ChatCompletionResponse,
    HTTPValidationError,
    SDKError,
)
from ..models.sql_model import ChatMessage
from ..models.domain_model import Role
from ..config import settings
from ..config.logger import logger
from ..errors.app_errors import TechnicalError
from ..errors.llm_api_errors import (
    LLMAPIUnauthorizedAccessError,
    LLMAPIUnavailableError,
)


class LLMRepository:
    def __init__(self):
        self.client = Mistral(api_key=settings().mistral_api_key)

    def chat_completion(self, messages: list[ChatMessage]) -> ChatMessage:
        """
        Chat completion with Mistral AI.

        Raises:
            LLMAPIUnauthorizedAccessError: If the API key is invalid.
            LLMAPIUnavailableError: If the API is not available.
        """
        try:
            chat_completion_response = self.client.chat.complete(
                model=settings().mistral_model_name,
                messages=map_chat_messages_to_completion_request_messages(messages),
            )

            logger.info(f"Chat completion response: {chat_completion_response}")

            return map_completion_response_to_chat_message(chat_completion_response)

        except HTTPValidationError as e:
            raise TechnicalError(
                message="HTTP validation error",
                cause=e,
            )
        except SDKError as e:
            if e.status_code == 401:
                raise LLMAPIUnauthorizedAccessError()
            elif e.status_code == 400:
                raise TechnicalError(
                    message="HTTP validation error",
                    cause=e,
                )
            else:
                raise LLMAPIUnavailableError(cause=e)
        except ValidationError as e:
            raise LLMAPIUnavailableError(cause=e)


def map_chat_messages_to_completion_request_messages(
    messages: list[ChatMessage],
) -> ChatCompletionRequestMessages:
    return [
        {
            "role": message.role.value,
            "content": message.content,
        }
        for message in messages
    ]


def map_completion_response_to_chat_message(
    response: ChatCompletionResponse,
) -> ChatMessage:
    """
    Map a Mistral chat completion response to a ChatMessage.

    Raises:
        ValidationError: If the response has no choices or the message is missing a role or content.
    """
    if not len(response.choices):
        raise ValidationError("No choices in response")
    assistant_message = response.choices[0].message

    return ChatMessage.model_validate(
        {
            "id": response.id,
            "role": Role(assistant_message.role),
            "content": assistant_message.content,
            "created_at": datetime.fromtimestamp(response.created),
        }
    )
