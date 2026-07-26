from app.models.ai_conversation import AIConversation
from app.models.ai_message import AIMessage


class AIConversationService:

    @staticmethod
    def create_conversation(
        db,
        repository_id,
        title="New Conversation",
    ):
        conversation = AIConversation(
            repository_id=repository_id,
            title=title,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def get_conversations(
        db,
        repository_id,
    ):
        conversations = (
            db.query(AIConversation)
            .filter(
                AIConversation.repository_id == repository_id
            )
            .order_by(
                AIConversation.updated_at.desc()
            )
            .all()
        )

        return conversations

    @staticmethod
    def get_conversation(
        db,
        conversation_id,
    ):
        return (
            db.query(AIConversation)
            .filter(
                AIConversation.id == conversation_id
            )
            .first()
        )

    @staticmethod
    def get_messages(
        db,
        conversation_id,
    ):
        messages = (
            db.query(AIMessage)
            .filter(
                AIMessage.conversation_id == conversation_id
            )
            .order_by(
                AIMessage.created_at.asc()
            )
            .all()
        )

        return messages

    @staticmethod
    def add_message(
        db,
        conversation_id,
        role,
        content,
    ):
        message = AIMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    @staticmethod
    def delete_conversation(
        db,
        conversation_id,
    ):
        conversation = (
            db.query(AIConversation)
            .filter(
                AIConversation.id == conversation_id
            )
            .first()
        )

        if conversation is None:
            return False

        try:
            # Delete all messages first
            db.query(AIMessage).filter(
                AIMessage.conversation_id == conversation_id
            ).delete(
                synchronize_session=False
            )

            # Delete conversation
            db.delete(conversation)

            db.commit()

            return True

        except Exception:
            db.rollback()
            raise