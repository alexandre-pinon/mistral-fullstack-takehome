from typing import Annotated
from mistralai import Mistral
from sqlmodel import Session
from fastapi import Depends
from .db import get_session
from .mistral import mistral_client


SessionDep = Annotated[Session, Depends(get_session)]
MistralClientDep = Annotated[Mistral, Depends(mistral_client)]
