"""usuarios, sesiones (refresh tokens) y dueño de cada análisis

Revision ID: 0006
Revises: 0005
Create Date: 2026-11-18
"""
import sqlalchemy as sa
from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),  # Argon2id; nunca la contraseña
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.CheckConstraint("email = lower(email)", name="ck_users_email_lower"),
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        # Todos los tokens que salen de un mismo login comparten familia: si se reutiliza uno viejo, se revoca la familia.
        sa.Column("family_id", sa.Uuid(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),  # SHA-256 del token; el token en sí no se guarda
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        # true = se revocó porque se cambió por uno nuevo (rotación); false = cierre de sesión o robo detectado.
        sa.Column("rotated", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_refresh_tokens_user", ondelete="CASCADE"),
        sa.UniqueConstraint("token_hash", name="uq_refresh_tokens_token_hash"),
        sa.CheckConstraint("length(token_hash) = 64", name="ck_refresh_tokens_hash"),
    )
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"])
    op.create_index("ix_refresh_tokens_family_id", "refresh_tokens", ["family_id"])
    op.create_index("ix_refresh_tokens_expires_at", "refresh_tokens", ["expires_at"])

    # Dueño del análisis. Vacío = análisis anónimo. Si se borra la cuenta, se borran sus análisis.
    op.add_column("analyses", sa.Column("user_id", sa.Uuid(), nullable=True))
    op.create_foreign_key("fk_analyses_user", "analyses", "users", ["user_id"], ["id"], ondelete="CASCADE")
    op.create_index("ix_analyses_user_id", "analyses", ["user_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_analyses_user_id", table_name="analyses")
    op.drop_constraint("fk_analyses_user", "analyses", type_="foreignkey")
    op.drop_column("analyses", "user_id")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
