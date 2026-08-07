from sqlalchemy.orm import Session

from src.api.services.chat_service import (
    ChatService,
)


def get_conversations(
    user_id: int,
    db: Session,
):
    service = ChatService(db)

    return service.get_conversations(
        user_id
    )


def get_conversation(
    user_id: int,
    conversation_id: int,
    db: Session,
):
    service = ChatService(db)

    return service.get_conversation(
        user_id,
        conversation_id,
    )


def create_conversation(
    user_id: int,
    request,
    db: Session,
):
    service = ChatService(db)

    return service.create_conversation(
        user_id,
        request,
    )


def update_conversation(
    user_id: int,
    conversation_id: int,
    request,
    db: Session,
):
    service = ChatService(db)

    return service.update_conversation(
        user_id,
        conversation_id,
        request,
    )


def delete_conversation(
    user_id: int,
    conversation_id: int,
    db: Session,
):
    service = ChatService(db)

    service.delete_conversation(
        user_id,
        conversation_id,
    )

    return {
        "message": "Conversation deleted successfully"
    }


def get_messages(
    user_id: int,
    conversation_id: int,
    db: Session,
):
    service = ChatService(db)

    return service.get_messages(
        user_id,
        conversation_id,
    )


def send_message(
    user_id: int,
    conversation_id: int,
    message: str,
    db: Session,
):
    service = ChatService(db)

    return service.send_message(
        user_id,
        conversation_id,
        message,
    )