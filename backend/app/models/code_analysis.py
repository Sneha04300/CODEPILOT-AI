import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class CodeAnalysis(Base):
    __tablename__ = "code_analyses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    repository_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "repositories.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        default="pending",
    )

    total_files = Column(
        Integer,
        nullable=False,
        default=0,
    )

    total_findings = Column(
        Integer,
        nullable=False,
        default=0,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    findings = relationship(
        "AnalysisFinding",
        back_populates="analysis",
        cascade="all, delete-orphan",
    )