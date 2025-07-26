from typing import Annotated
from mistralai import Mistral
from fastapi import Depends

from .config import settings


def get_mistral_client() -> Mistral:
    settings = settings()
    return Mistral(
        api_key=settings.mistral_api_key,
    )


LlmClientDep = Annotated[Mistral, Depends(get_mistral_client)]
