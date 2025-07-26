from datetime import datetime
from mistralai import Mistral, models
from mistralai.models import ChatCompletionResponse
from functools import lru_cache
from pydantic import ValidationError

from .models import ChatMessage
from .config import settings


@lru_cache
def mistral_client() -> Mistral:
    return Mistral(
        api_key=settings().mistral_api_key,
    )


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
        id=response.id,
        role=assistant_message.role,
        content=assistant_message.content,
        created_at=datetime.fromtimestamp(response.created),
    )
