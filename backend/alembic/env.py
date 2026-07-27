from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.config import DATABASE_URL
from app.db.database import Base


# ---------------------------------------------------------
# IMPORT ALL SQLALCHEMY MODELS
# ---------------------------------------------------------
# These imports are required so Alembic can discover
# every table registered with Base.metadata.

from app.models.user import User
from app.models.repository import Repository
from app.models.project_file import ProjectFile
from app.models.ai_conversation import AIConversation
from app.models.ai_message import AIMessage

# Phase 8 models
from app.models.code_analysis import CodeAnalysis
from app.models.analysis_finding import AnalysisFinding


# ---------------------------------------------------------
# ALEMBIC CONFIGURATION
# ---------------------------------------------------------

config = context.config


# Use DATABASE_URL from app/core/config.py
# instead of hardcoding database credentials in alembic.ini.
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL,
)


# Configure Python logging using alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Alembic uses this metadata to detect tables,
# columns, foreign keys, indexes, etc.
target_metadata = Base.metadata


# ---------------------------------------------------------
# OFFLINE MIGRATIONS
# ---------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.
    """

    url = config.get_main_option(
        "sqlalchemy.url"
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------
# ONLINE MIGRATIONS
# ---------------------------------------------------------

def run_migrations_online() -> None:
    """
    Run migrations using a real database connection.
    """

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {}
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------
# START ALEMBIC
# ---------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()