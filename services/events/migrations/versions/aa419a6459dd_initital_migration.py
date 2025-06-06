"""Initital migration

Revision ID: aa419a6459dd
Revises: 
Create Date: 2025-04-22 10:53:25.368901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'aa419a6459dd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('city', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('state', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('country', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_venues_id'), 'venues', ['id'], unique=False)
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('event_type', sa.Enum('PPV', 'SPECIAL', 'NETWORK', 'PREMIUM', name='eventtype'), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('attendance', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)
    op.create_index(op.f('ix_events_name'), 'events', ['name'], unique=False)
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('show_type', sa.Enum('RAW', 'SMACKDOWN', 'NXT', 'MAIN_EVENT', 'SUPERSTARS', 'ECW', 'WCW', 'HEAT', 'VELOCITY', 'THUNDER', 'NITRO', 'OTHER', name='showtype'), nullable=False),
    sa.Column('episode_number', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('is_live', sa.Boolean(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('attendance', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shows_id'), 'shows', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_shows_id'), table_name='shows')
    op.drop_table('shows')
    op.drop_index(op.f('ix_events_name'), table_name='events')
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.drop_table('events')
    op.drop_index(op.f('ix_venues_id'), table_name='venues')
    op.drop_table('venues')
    # ### end Alembic commands ###
