"""update_table_columns

Revision ID: 551d63e4c0f3
Revises: 
Create Date: 2023-09-29 04:59:05.909472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '551d63e4c0f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('recipes', sa.Column('calories_per_serving', sa.Integer, nullable=True))


def downgrade() -> None:
    pass
