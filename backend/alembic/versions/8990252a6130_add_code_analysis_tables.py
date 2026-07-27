"""add code analysis tables

Revision ID: 8990252a6130
Revises: a96767c95d95
Create Date: 2026-07-27 11:21:41.687252
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8990252a6130"
down_revision: Union[str, Sequence[str], None] = "a96767c95d95"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create Phase 8 code analysis tables."""

    # ---------------------------------------------------------
    # CODE ANALYSES
    # ---------------------------------------------------------

    op.create_table(
        "code_analyses",

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "repository_id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "total_files",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "total_findings",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["repository_id"],
            ["repositories.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_code_analyses_repository_id"),
        "code_analyses",
        ["repository_id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # ANALYSIS FINDINGS
    # ---------------------------------------------------------

    op.create_table(
        "analysis_findings",

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "analysis_id",
            sa.UUID(),
            nullable=False,
        ),

        sa.Column(
            "file_id",
            sa.UUID(),
            nullable=True,
        ),

        sa.Column(
            "category",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "severity",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "title",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "recommendation",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "line_number",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["analysis_id"],
            ["code_analyses.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["file_id"],
            ["project_files.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_analysis_findings_analysis_id"),
        "analysis_findings",
        ["analysis_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_analysis_findings_file_id"),
        "analysis_findings",
        ["file_id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove Phase 8 code analysis tables."""

    op.drop_index(
        op.f("ix_analysis_findings_file_id"),
        table_name="analysis_findings",
    )

    op.drop_index(
        op.f("ix_analysis_findings_analysis_id"),
        table_name="analysis_findings",
    )

    op.drop_table(
        "analysis_findings"
    )

    op.drop_index(
        op.f("ix_code_analyses_repository_id"),
        table_name="code_analyses",
    )

    op.drop_table(
        "code_analyses"
    )