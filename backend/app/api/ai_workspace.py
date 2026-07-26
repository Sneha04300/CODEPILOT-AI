import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.ai_workspcae import (
    AIQuestionRequest,
    CodeExplainRequest,
    RepositoryFileExplainRequest,
    CreateConversationRequest,
)

from app.services.ai_workspace_service import AIWorkspaceService
from app.services.ai_service import AIService
from app.services.ai_conversation_service import AIConversationService


router = APIRouter(
    prefix="/ai-workspace",
    tags=["AI Workspace"],
)


# ---------------------------------------------------------
# 1. ASK QUESTIONS ABOUT A REPOSITORY
# ---------------------------------------------------------

@router.post("/ask")
def ask_repository_question(
    data: AIQuestionRequest,
    db: Session = Depends(get_db),
):
    # Load repository and indexed files
    result = AIWorkspaceService.get_repository_context(
        db=db,
        repository_id=data.repository_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    repository = result["repository"]
    files = result["files"]

    # Check whether conversation exists
    conversation = AIConversationService.get_conversation(
        db=db,
        conversation_id=data.conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    # Make sure conversation belongs to the repository
    if conversation.repository_id != data.repository_id:
        raise HTTPException(
            status_code=400,
            detail="Conversation does not belong to this repository",
        )

    # Find files relevant to the current question
    relevant_files = AIWorkspaceService.find_relevant_files(
        db=db,
        repository_id=data.repository_id,
        question=data.question,
    )

    # Build repository context
    context_result = AIWorkspaceService.build_context(
        relevant_files
    )

    # Load previous conversation messages
    history = AIConversationService.get_messages(
        db=db,
        conversation_id=data.conversation_id,
    )

    # Ask AI using repository context + previous conversation
    ai_answer = AIService.ask_repository(
        question=data.question,
        context=context_result["context"],
        history=history,
    )

    # Save current user message
    AIConversationService.add_message(
        db=db,
        conversation_id=data.conversation_id,
        role="user",
        content=data.question,
    )

    # Save current AI response
    AIConversationService.add_message(
        db=db,
        conversation_id=data.conversation_id,
        role="assistant",
        content=ai_answer,
    )

    return {
        "success": True,

        "repository": {
            "id": str(repository.id),
            "name": repository.name,
        },

        "conversation": {
            "id": str(conversation.id),
            "title": conversation.title,
        },

        "question": data.question,

        "answer": ai_answer,

        "sources": [
            {
                "id": str(file.id),
                "filename": file.filename,
                "path": file.path,
                "language": file.language,
            }
            for file in context_result["included_files"]
        ],

        "context_info": {
            "available_files": len(files),
            "relevant_files": len(relevant_files),
            "included_files": len(
                context_result["included_files"]
            ),
            "characters": context_result["characters"],
            "history_messages": len(history),
        },
    }


# ---------------------------------------------------------
# 2. EXPLAIN MANUALLY PROVIDED CODE
# ---------------------------------------------------------

@router.post("/explain")
def explain_code(
    data: CodeExplainRequest,
):
    explanation = AIService.explain_code(
        code=data.code,
        language=data.language,
        filename=data.filename,
    )

    return {
        "success": True,
        "filename": data.filename,
        "language": data.language,
        "explanation": explanation,
    }


# ---------------------------------------------------------
# 3. EXPLAIN A FILE FROM AN INDEXED REPOSITORY
# ---------------------------------------------------------

@router.post("/explain-file")
def explain_repository_file(
    data: RepositoryFileExplainRequest,
    db: Session = Depends(get_db),
):
    file = AIWorkspaceService.get_repository_file(
        db=db,
        repository_id=data.repository_id,
        file_id=data.file_id,
    )

    if file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found in this repository",
        )

    explanation = AIService.explain_code(
        code=file.content,
        language=file.language,
        filename=file.filename,
    )

    return {
        "success": True,

        "file": {
            "id": str(file.id),
            "repository_id": str(file.repository_id),
            "filename": file.filename,
            "path": file.path,
            "language": file.language,
            "extension": file.extension,
        },

        "explanation": explanation,
    }


# ---------------------------------------------------------
# 4. CREATE A NEW AI CONVERSATION
# ---------------------------------------------------------

@router.post("/conversations")
def create_conversation(
    data: CreateConversationRequest,
    db: Session = Depends(get_db),
):
    # Check whether repository exists
    result = AIWorkspaceService.get_repository_context(
        db=db,
        repository_id=data.repository_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    conversation = AIConversationService.create_conversation(
        db=db,
        repository_id=data.repository_id,
        title=data.title,
    )

    return {
        "success": True,

        "conversation": {
            "id": str(conversation.id),
            "repository_id": str(
                conversation.repository_id
            ),
            "title": conversation.title,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
        },
    }


# ---------------------------------------------------------
# 5. GET ALL CONVERSATIONS FOR A REPOSITORY
# ---------------------------------------------------------

@router.get("/repositories/{repository_id}/conversations")
def get_repository_conversations(
    repository_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    conversations = AIConversationService.get_conversations(
        db=db,
        repository_id=repository_id,
    )

    return {
        "success": True,
        "count": len(conversations),

        "conversations": [
            {
                "id": str(conversation.id),
                "repository_id": str(
                    conversation.repository_id
                ),
                "title": conversation.title,
                "created_at": conversation.created_at,
                "updated_at": conversation.updated_at,
            }
            for conversation in conversations
        ],
    }


# ---------------------------------------------------------
# 6. GET MESSAGES FROM A CONVERSATION
# ---------------------------------------------------------

@router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    # Check whether conversation exists
    conversation = AIConversationService.get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    messages = AIConversationService.get_messages(
        db=db,
        conversation_id=conversation_id,
    )

    return {
        "success": True,

        "conversation": {
            "id": str(conversation.id),
            "title": conversation.title,
            "repository_id": str(
                conversation.repository_id
            ),
        },

        "count": len(messages),

        "messages": [
            {
                "id": str(message.id),
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }

# ---------------------------------------------------------
# 7. DELETE A CONVERSATION
# ---------------------------------------------------------

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    deleted = AIConversationService.delete_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {
        "success": True,
        "message": "Conversation deleted successfully",
    }