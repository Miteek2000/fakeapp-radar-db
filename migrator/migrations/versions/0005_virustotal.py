"""virustotal: resultado por análisis y caché por SHA-256

Revision ID: 0005
Revises: 0004
Create Date: 2026-11-17
"""
import sqlalchemy as sa
from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None

ESTADOS = "('pending','found','not_found','unavailable')"


def upgrade() -> None:
    op.add_column("analyses", sa.Column("vt_status", sa.String(length=16), nullable=True))
    op.add_column("analyses", sa.Column("vt_malicious", sa.SmallInteger(), nullable=True))
    op.add_column("analyses", sa.Column("vt_total", sa.SmallInteger(), nullable=True))
    op.create_check_constraint("ck_analyses_vt_status", "analyses", f"vt_status is null or vt_status in {ESTADOS}")

    # Caché: el mismo archivo (mismo SHA-256) no se vuelve a consultar durante unas horas.
    # Solo guarda respuestas definitivas (found / not_found), nunca errores.
    op.create_table(
        "vt_cache",
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("malicious", sa.SmallInteger(), nullable=True),
        sa.Column("total", sa.SmallInteger(), nullable=True),
        sa.Column("checked_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("sha256"),
        sa.CheckConstraint("length(sha256) = 64", name="ck_vt_cache_sha256"),
        sa.CheckConstraint("status in ('found','not_found')", name="ck_vt_cache_status"),
    )


def downgrade() -> None:
    op.drop_table("vt_cache")
    op.drop_constraint("ck_analyses_vt_status", "analyses", type_="check")
    op.drop_column("analyses", "vt_total")
    op.drop_column("analyses", "vt_malicious")
    op.drop_column("analyses", "vt_status")
