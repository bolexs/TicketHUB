"""fix tables

Revision ID: f00a1ebde929
Revises: f6d0e08c594e
Create Date: 2024-03-20 21:44:38.763313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f00a1ebde929'
down_revision: Union[str, None] = 'f6d0e08c594e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('ticket', sa.Integer(), nullable=False))
    op.drop_index('ix_events_tickets', table_name='events')
    op.create_index(op.f('ix_events_ticket'), 'events', ['ticket'], unique=False)
    op.drop_column('events', 'tickets')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('tickets', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_events_ticket'), table_name='events')
    op.create_index('ix_events_tickets', 'events', ['tickets'], unique=False)
    op.drop_column('events', 'ticket')
    # ### end Alembic commands ###