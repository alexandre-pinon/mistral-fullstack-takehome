from typing import AsyncGenerator
from mistralai import Mistral
from mistralai.models import (
    Messages as ChatCompletionRequestMessages,
    HTTPValidationError,
    SDKError,
)
from ..models import ChatMessage
from ..config import settings, logger
from ..errors import (
    TechnicalError,
    LLMAPIUnauthorizedAccessError,
    LLMAPIUnavailableError,
)


class LLMRepository:
    def __init__(self):
        self.client = Mistral(api_key=settings().mistral_api_key)

    async def chat_completion_stream(
        self, messages: list[ChatMessage]
    ) -> AsyncGenerator[str]:
        """
        Stream chat completion with Mistral AI.
        Yields content chunks as they arrive.
        """
        try:
            response = await self.client.chat.stream_async(
                model=settings().mistral_model_name,
                messages=map_chat_messages_to_completion_request_messages(messages),
            )

            async for chunk in response:
                logger.debug(f"Received chunk: {chunk}")
                if len(chunk.data.choices) > 0 and chunk.data.choices[0].delta.content:
                    yield chunk.data.choices[0].delta.content

            logger.debug(f"Stream finished")

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
