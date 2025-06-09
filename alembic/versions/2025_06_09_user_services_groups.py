"""user, services, groups

Revision ID: bd5db2e93bc5
Revises:
Create Date: 2025-06-09 13:18:39.045017

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "bd5db2e93bc5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("subscription_price", sa.Float(), nullable=False),
        sa.Column("user_price", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("group_name", sa.String(), nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("max_slots", sa.Integer(), nullable=False),
        sa.Column("free_slots", sa.Integer(), nullable=False),
        sa.Column("admin_email", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("group_name"),
    )
    op.create_table(
        "linked_services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "group_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("linked_service_id", sa.Integer(), nullable=False),
        sa.Column("last_payment", sa.DateTime(), nullable=True),
        sa.Column("next_payment", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["linked_service_id"],
            ["linked_services.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_index(op.f("ix_requests_id"), table_name="requests")
    op.drop_table("requests")
    op.drop_table("reservations")
    op.add_column(
        "users", sa.Column("telegram_id", sa.Integer(), nullable=False)
    )
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.create_unique_constraint(None, "users", ["telegram_id"])
    op.create_unique_constraint(None, "users", ["username"])
    op.drop_constraint(
        op.f("users_manager_id_fkey"), "users", type_="foreignkey"
    )
    op.drop_column("users", "role")
    op.drop_column("users", "manager_id")
    op.drop_column("users", "hashed_password")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "hashed_password", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "manager_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "users",
        sa.Column("role", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        op.f("users_manager_id_fkey"), "users", "users", ["manager_id"], ["id"]
    )
    op.drop_constraint("uq_users_telegram_id", "users", type_="unique")
    op.drop_constraint("uq_users_username", "users", type_="unique")

    op.create_index(
        op.f("ix_users_username"), "users", ["username"], unique=True
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.drop_column("users", "telegram_id")
    op.create_table(
        "reservations",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("date", sa.DATE(), autoincrement=False, nullable=True),
        sa.Column(
            "time", postgresql.TIME(), autoincrement=False, nullable=True
        ),
        sa.Column("guests", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("phone", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("reservations_pkey")),
    )
    op.create_table(
        "requests",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "bottoken", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column("chatid", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("message", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "response", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("requests_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("requests_pkey")),
    )
    op.create_index(op.f("ix_requests_id"), "requests", ["id"], unique=False)
    op.drop_table("payments")
    op.drop_table("group_users")
    op.drop_table("linked_services")
    op.drop_table("groups")
    op.drop_table("services")
