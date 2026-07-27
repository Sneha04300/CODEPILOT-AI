import uuid

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    ForeignKey,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class AnalysisFinding(Base):
    __tablename__ = "analysis_findings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    analysis_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "code_analyses.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    file_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "project_files.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        index=True,
    )

    category = Column(
        String,
        nullable=False,
    )

    severity = Column(
        String,
        nullable=False,
    )

    title = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    recommendation = Column(
        Text,
        nullable=True,
    )

    line_number = Column(
        Integer,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    analysis = relationship(
        "CodeAnalysis",
        back_populates="findings",
    )