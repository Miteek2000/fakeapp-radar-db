"""crear tabla analyses

Revision ID: 0001
Revises:
Create Date: 2026-11-17
"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("risk_score", sa.SmallInteger(), nullable=True),
        sa.Column("risk_level", sa.String(length=8), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("report_enc", sa.LargeBinary(), nullable=True),
        sa.Column("key_version", sa.SmallInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("status in ('pending','running','done','failed')", name="ck_analyses_status"),
        sa.CheckConstraint("risk_score is null or (risk_score >= 0 and risk_score <= 100)", name="ck_analyses_score"),
        sa.CheckConstraint("length(sha256) = 64", name="ck_analyses_sha256"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analyses_sha256", "analyses", ["sha256"])
    op.create_index("ix_analyses_created_at", "analyses", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_analyses_created_at", table_name="analyses")
    op.drop_index("ix_analyses_sha256", table_name="analyses")
    op.drop_table("analyses")
