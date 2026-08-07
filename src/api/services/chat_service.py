from fastapi import HTTPException, status

from src.api.models.chat_conversation import (
    ChatConversation,
)

from src.api.models.chat_message import (
    ChatMessage,
)

from src.api.models.enums import ChatRole

from src.api.repository.chat_repository import (
    ChatRepository,
)


class ChatService:

    def __init__(self, db):
        self.repository = ChatRepository(db)

    #Conversation CRUD operations
    def get_conversations(
        self,
        user_id: int,
    ):
        return (
            self.repository
            .get_conversations_for_user(
                user_id
            )
        )

    def get_conversation(
        self,
        user_id: int,
        conversation_id: int,
    ):

        conversation = (
            self.repository
            .get_conversation(
                conversation_id
            )
        )

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        if conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this conversation",
            )

        return conversation

    def create_conversation(
        self,
        user_id: int,
        request,
    ):

        conversation = ChatConversation(
            user_id=user_id,
            lesson_day_id=request.lesson_day_id,
            title=request.title,
        )

        return (
            self.repository
            .create_conversation(
                conversation
            )
        )

    def update_conversation(
        self,
        user_id: int,
        conversation_id: int,
        request,
    ):

        conversation = self.get_conversation(
            user_id,
            conversation_id,
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                conversation,
                field,
                value,
            )

        return (
            self.repository
            .update_conversation(
                conversation
            )
        )

    def delete_conversation(
        self,
        user_id: int,
        conversation_id: int,
    ):

        conversation = self.get_conversation(
            user_id,
            conversation_id,
        )

        return (
            self.repository
            .delete_conversation(
                conversation
            )
        )

    # Messages
    def get_messages(
        self,
        user_id: int,
        conversation_id: int,
    ):

        self.get_conversation(
            user_id,
            conversation_id,
        )

        return self.repository.get_messages(
            conversation_id
        )

    def send_message(
        self,
        user_id: int,
        conversation_id: int,
        message: str,
    ):

        conversation = self.get_conversation(
            user_id,
            conversation_id,
        )

        # Save user's message
        user_message = ChatMessage(
            conversation_id=conversation.id,
            role=ChatRole.USER,
            content=message,
        )
        self.repository.create_message(
            user_message
        )

        # -------------------------------------------------
        # TODO: RAG + LLM
        # -------------------------------------------------
        assistant_content = (
            "RAG response will be generated here."
        )
        #will replace with sth like:assistant_content = 
        # self.rag_service.answer(
        #     question=message,
        #     lesson_day_id=conversation.lesson_day_id,
        # )

        # -------------------------------------------------
        # Save assistant response
        # -------------------------------------------------

        assistant_message = ChatMessage(
            conversation_id=conversation.id,
            role=ChatRole.ASSISTANT,
            content=assistant_content,
        )
        return self.repository.create_message(
            assistant_message
        )