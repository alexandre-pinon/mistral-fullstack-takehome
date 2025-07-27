from typing import Generator
from pydantic import ValidationError
from mistralai import Mistral
from mistralai.models import (
    Messages as ChatCompletionRequestMessages,
    HTTPValidationError,
    SDKError,
)
from ..models import ChatMessage, Role
from ..config import settings, logger
from ..errors import (
    TechnicalError,
    LLMAPIUnauthorizedAccessError,
    LLMAPIUnavailableError,
)


class LLMRepository:
    def __init__(self):
        self.client = Mistral(api_key=settings().mistral_api_key)

    def chat_completion_stream(self, messages: list[ChatMessage]) -> Generator[str]:
        """
        Stream chat completion with Mistral AI.
        Yields content chunks as they arrive.
        """
        try:
            response = self.client.chat.stream(
                model=settings().mistral_model_name,
                messages=map_chat_messages_to_completion_request_messages(messages),
            )

            with response as stream:
                for chunk in stream:
                    logger.info(f"Received chunk: {chunk}")
                    if (
                        len(chunk.data.choices) > 0
                        and chunk.data.choices[0].delta.content
                    ):
                        yield chunk.data.choices[0].delta.content

            logger.info(f"Stream finished")

        except HTTPValidationError as e:
            raise TechnicalError(
                message="HTTP validation error during streaming",
                cause=e,
            )
        except SDKError as e:
            if e.status_code == 401:
                raise LLMAPIUnauthorizedAccessError()
            elif e.status_code == 400:
                raise TechnicalError(
                    message="HTTP validation error during streaming",
                    cause=e,
                )
            else:
                raise LLMAPIUnavailableError(cause=e)
        except Exception as e:
            logger.error(f"Unexpected error streaming chat completion: {e}")
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
