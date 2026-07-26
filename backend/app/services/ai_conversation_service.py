from app.models.ai_conversation import AIConversation
from app.models.ai_message import AIMessage


class AIConversationService:

    # ---------------------------------------------------------
    # 1. CREATE CONVERSATION
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # 2. GET ALL CONVERSATIONS FOR A REPOSITORY
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # 3. GET SINGLE CONVERSATION
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # 4. GET CONVERSATION MESSAGES
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # 5. ADD MESSAGE
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # 6. UPDATE CONVERSATION TITLE
    # ---------------------------------------------------------

    @staticmethod
    def update_conversation_title(
        db,
        conversation_id,
        title,
    ):
        conversation = (
            db.query(AIConversation)
            .filter(
                AIConversation.id == conversation_id
            )
            .first()
        )

        if conversation is None:
            return None

        conversation.title = title

        db.commit()
        db.refresh(conversation)

        return conversation


    # ---------------------------------------------------------
    # 7. DELETE CONVERSATION
    # ---------------------------------------------------------

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
            # Delete messages belonging to this conversation
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