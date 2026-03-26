"""lowercase_tables_and_refresh_token

Revision ID: 1f6dfef30b10
Revises: 400f4e0c3dc2
Create Date: 2026-03-26 17:38:22.545815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f6dfef30b10'
down_revision: Union[str, Sequence[str], None] = '400f4e0c3dc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("Users", "users")
    op.rename_table("Categories", "categories")
    op.rename_table("Tasks", "tasks")

    op.execute('ALTER INDEX "ix_Users_email" RENAME TO ix_users_email')
    op.execute('ALTER INDEX "ix_Categories_name" RENAME TO ix_categories_name')

    op.add_column("users", sa.Column("refresh_token", sa.VARCHAR(length=512), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "refresh_token")

    op.execute("ALTER INDEX ix_users_email RENAME TO \"ix_Users_email\"")
    op.execute("ALTER INDEX ix_categories_name RENAME TO \"ix_Categories_name\"")

    op.rename_table("tasks", "Tasks")
    op.rename_table("categories", "Categories")
    op.rename_table("users", "Users")
