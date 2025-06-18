"""payment model changes

Revision ID: 33cb750fd497
Revises: 96343b2661dd
Create Date: 2025-06-17 22:18:10.118053

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "33cb750fd497"
down_revision: Union[str, None] = "96343b2661dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    payment_status_enum = sa.Enum("WAITING", "PAID", "EXPIRED", name="paymentstatus")
    payment_status_enum.create(op.get_bind())

    op.add_column(
        "payments",
        sa.Column("status", payment_status_enum, nullable=True),
    )

    op.add_column(
        "payments", sa.Column("payment_code", sa.String(), nullable=True)
    )
    op.create_unique_constraint(None, "payments", ["payment_code"])

    op.drop_column("payments", "next_payment")
    op.drop_column("payments", "last_payment")



def downgrade() -> None:
    op.add_column(
        "payments",
        sa.Column("last_payment", postgresql.TIMESTAMP(), nullable=True),
    )
    op.add_column(
        "payments",
        sa.Column("next_payment", postgresql.TIMESTAMP(), nullable=True),
    )

    op.drop_column("payments", "payment_code")
    op.drop_column("payments", "status")

    sa.Enum(name="paymentstatus").drop(op.get_bind())
