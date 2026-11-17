"""catálogo: marca de permisos curados

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-17
"""
import sqlalchemy as sa
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("permission_catalog", sa.Column("curated", sa.Boolean(), server_default=sa.false(), nullable=False))


def downgrade() -> None:
    op.drop_column("permission_catalog", "curated")
