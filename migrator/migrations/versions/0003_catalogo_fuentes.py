"""catálogo: nivel de protección de AOSP y fuentes

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-17
"""
import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("permission_catalog", sa.Column("protection_level", sa.Text(), nullable=True))
    op.add_column("permission_catalog", sa.Column("source", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("permission_catalog", "source")
    op.drop_column("permission_catalog", "protection_level")
