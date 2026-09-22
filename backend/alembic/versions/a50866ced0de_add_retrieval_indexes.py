"""add retrieval indexes

Revision ID: a50866ced0de
Revises: df0c6b014c3b
Create Date: 2026-09-22 13:40:46.762246

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a50866ced0de"
down_revision: Union[str, Sequence[str], None] = "df0c6b014c3b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # GIN index for PostgreSQL full-text search
    op.execute("""
        CREATE INDEX ix_document_chunks_content_tsv_gin
        ON document_chunks
        USING gin (content_tsv)
        """)

    # HNSW index for vector similarity search
    op.execute("""
        CREATE INDEX ix_document_chunks_embedding_hnsw
        ON document_chunks
        USING hnsw (embedding vector_cosine_ops)
        """)


def downgrade() -> None:
    """Downgrade schema."""

    op.execute("""
        DROP INDEX IF EXISTS ix_document_chunks_embedding_hnsw
        """)

    op.execute("""
        DROP INDEX IF EXISTS ix_document_chunks_content_tsv_gin
        """)
