"""payment_code added to payment model

Revision ID: 0ce68a0ca7bc
Revises: 96343b2661dd
Create Date: 2025-06-17 17:24:42.011822

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0ce68a0ca7bc"
down_revision: Union[str, None] = "96343b2661dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "payments", sa.Column("payment_code", sa.String(), nullable=True)
    )
    op.create_unique_constraint(None, "payments", ["payment_code"])


def downgrade() -> None:
    op.drop_constraint(None, "payments", type_="unique")
    op.drop_column("payments", "payment_code")
