"""Update table fields to name

Revision ID: d75e71a25e92
Revises: 7c573af2cff3
Create Date: 2024-01-22 04:28:40.575558

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd75e71a25e92'
down_revision = '7c573af2cff3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instructions', sa.Column('name', sa.String(length=128), nullable=False))
    op.drop_column('instructions', 'title')
    op.add_column('nutritional_values', sa.Column('name', sa.String(length=128), nullable=False))
    op.drop_column('nutritional_values', 'title')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nutritional_values', sa.Column('title', mysql.VARCHAR(length=128), nullable=False))
    op.drop_column('nutritional_values', 'name')
    op.add_column('instructions', sa.Column('title', mysql.VARCHAR(length=128), nullable=False))
    op.drop_column('instructions', 'name')
    # ### end Alembic commands ###
