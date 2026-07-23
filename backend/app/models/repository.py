import uuid

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    language: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Indexing"
    )

    progress: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    total_files: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    github_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    project_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    project_files = relationship(
        "ProjectFile",
        back_populates="repository",
        cascade="all, delete-orphan"
    )