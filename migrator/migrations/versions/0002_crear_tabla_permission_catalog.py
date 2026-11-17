"""crear tabla permission_catalog

Permisos de Android que sabemos explicar. Los datos los carga seeds/01-catalogo-permisos.sql.

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-17
"""
import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "permission_catalog",
        sa.Column("id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("android_name", sa.Text(), nullable=False),
        sa.Column("friendly_title", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("weight", sa.SmallInteger(), nullable=False),
        sa.Column("icon", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("android_name", name="uq_permission_catalog_android_name"),
        sa.CheckConstraint("severity in ('peligroso','atencion','normal')", name="ck_permission_catalog_severity"),
        sa.CheckConstraint("weight >= 0 and weight <= 100", name="ck_permission_catalog_weight"),
    )


def downgrade() -> None:
    op.drop_table("permission_catalog")
