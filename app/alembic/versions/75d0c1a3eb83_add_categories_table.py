"""Add categories table

Revision ID: 75d0c1a3eb83
Revises: 2dbc472f908c
Create Date: 2024-03-21 23:08:29.102572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75d0c1a3eb83'
down_revision: Union[str, None] = '2dbc472f908c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String)
    )


def downgrade() -> None:
    op.drop_table('categories')

