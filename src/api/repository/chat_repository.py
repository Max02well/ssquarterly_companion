from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.models.chat_conversation import (
    ChatConversation,
)
from src.api.models.chat_message import (
    ChatMessage,
)


class ChatRepository:

    def __init__(self, db: Session):
        self.db = db

    # Conversation CRUD operations
    def get_conversations_for_user(
        self,
        user_id: int,
    ):
        result = self.db.execute(
            select(ChatConversation)
            .where(
                ChatConversation.user_id
                == user_id
            )
            .order_by(
                ChatConversation.updated_at.desc()
            )
        )

        return result.scalars().all()

    def get_conversation(
        self,
        conversation_id: int,
    ):
        return self.db.get(
            ChatConversation,
            conversation_id,
        )

    def create_conversation(
        self,
        conversation: ChatConversation,
    ):
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def update_conversation(
        self,
        conversation: ChatConversation,
    ):
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def delete_conversation(
        self,
        conversation: ChatConversation,
    ):
        self.db.delete(conversation)
        self.db.commit()

        return conversation

    # Messages

    def get_messages(
        self,
        conversation_id: int,
    ):
        result = self.db.execute(
            select(ChatMessage)
            .where(
                ChatMessage.conversation_id
                == conversation_id
            )
            .order_by(
                ChatMessage.created_at
            )
        )

        return result.scalars().all()

    def create_message(
        self,
        message: ChatMessage,
    ):
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message