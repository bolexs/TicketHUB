"""Fix tables

Revision ID: dc5a7f693302
Revises: 139a50c27333
Create Date: 2024-03-23 23:38:56.564828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc5a7f693302'
down_revision: Union[str, None] = '139a50c27333'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('quantity', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_tickets_quantity'), 'tickets', ['quantity'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tickets_quantity'), table_name='tickets')
    op.drop_column('tickets', 'quantity')
    # ### end Alembic commands ###