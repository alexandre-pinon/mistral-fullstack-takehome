from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlmodel import select
from pydantic import ValidationError
from mistralai.models import HTTPValidationError, SDKError

from .config import settings
from .deps import MistralClientDep, SessionDep
from .models import ChatMessage, ChatRequest, HealthCheckResponse, Role
from .mistral import map_completion_response_to_chat_message


app = FastAPI(
    title="Turtle chat API",
    description="API for the Turtle chat app",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().allowed_origins,
    allow_methods=["GET", "POST"],
)


@app.get("/health", response_model=HealthCheckResponse)
def health_check():
    return HealthCheckResponse(status="ok")


@app.get("/chat", response_model=List[ChatMessage])
def get_chat_history(session: SessionDep):
    return session.exec(select(ChatMessage)).all()


@app.post("/chat", response_model=ChatMessage)
def chat(
    mistral_client: MistralClientDep,
    session: SessionDep,
    request: ChatRequest,
):
    user_message = ChatMessage.model_validate(request)
    session.add(user_message)
    session.commit()

    messages = session.exec(select(ChatMessage)).all()

    try:
        chat_completion_response = mistral_client.chat.complete(
            model=settings().mistral_model_name,
            messages=messages,
        )
        assistant_message = map_completion_response_to_chat_message(
            chat_completion_response
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=502, detail=f"Invalid response from AI service: {str(e)}"
        )
    except HTTPValidationError as e:
        raise HTTPException(
            status_code=502, detail=f"Invalid request to AI service: {str(e)}"
        )
    except SDKError as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}")

    session.add(assistant_message)
    session.commit()
    session.refresh(assistant_message)

    return assistant_message
