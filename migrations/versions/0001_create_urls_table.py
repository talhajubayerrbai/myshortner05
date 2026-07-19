"""create urls table

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "urls",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("short_code", sa.String(length=16), nullable=False),
        sa.Column("original_url", sa.String(length=2048), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("hit_count", sa.BigInteger(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_urls_id"), "urls", ["id"], unique=False)
    op.create_index(op.f("ix_urls_short_code"), "urls", ["short_code"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_urls_short_code"), table_name="urls")
    op.drop_index(op.f("ix_urls_id"), table_name="urls")
    op.drop_table("urls")
