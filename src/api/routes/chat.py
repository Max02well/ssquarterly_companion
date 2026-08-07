from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.database.database import get_db

from src.api.models.user import User

from src.api.security.dependencies import (
    get_current_user,
)

from src.api.controller.chat_controller import (
    get_conversations,
    get_conversation,
    create_conversation,
    update_conversation,
    delete_conversation,
    get_messages,
    send_message,
)

from src.api.schemas.chat import (
    CreateConversationRequest,
    UpdateConversationRequest,
    SendMessageRequest,
    ChatConversationResponse,
    ChatConversationDetailResponse,
    ChatMessageResponse,
)


router = APIRouter()

# Conversation routes
@router.get(
    "/conversations",
    response_model=list[
        ChatConversationResponse
    ],
)
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_conversations(
        current_user.id,
        db,
    )


@router.post(
    "/conversations",
    response_model=ChatConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_conversation(
    request: CreateConversationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return create_conversation(
        current_user.id,
        request,
        db,
    )


@router.get(
    "/conversations/{conversation_id}",
    response_model=ChatConversationDetailResponse,
)
def retrieve_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_conversation(
        current_user.id,
        conversation_id,
        db,
    )


@router.patch(
    "/conversations/{conversation_id}",
    response_model=ChatConversationResponse,
)
def modify_conversation(
    conversation_id: int,
    request: UpdateConversationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return update_conversation(
        current_user.id,
        conversation_id,
        request,
        db,
    )


@router.delete(
    "/conversations/{conversation_id}",
)
def remove_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return delete_conversation(
        current_user.id,
        conversation_id,
        db,
    )


# Messages
@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[
        ChatMessageResponse
    ],
)
def list_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return get_messages(
        current_user.id,
        conversation_id,
        db,
    )


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=ChatMessageResponse,
)
def create_message(
    conversation_id: int,
    request: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return send_message(
        current_user.id,
        conversation_id,
        request.message,
        db,
    )