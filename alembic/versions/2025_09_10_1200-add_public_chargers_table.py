"""add public chargers table

Revision ID: add_public_chargers_table
Revises: 2237c1d34f69
Create Date: 2025-09-10 12:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_public_chargers_table'
down_revision = '2237c1d34f69'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'public_chargers',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('external_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=2), nullable=False),
        sa.Column('latitude', sa.Numeric(10, 7), nullable=False),
        sa.Column('longitude', sa.Numeric(10, 7), nullable=False),
        sa.Column('power_kw', sa.Float(), nullable=True),
        sa.Column('connectors', sa.Text(), nullable=True),
        sa.Column('operator', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('last_seen', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('source', 'external_id', name='uq_public_charger_source_ext'),
    )
    op.create_index('idx_public_charger_country', 'public_chargers', ['country'])
    op.create_index('idx_public_charger_lat_lon', 'public_chargers', ['latitude', 'longitude'])


def downgrade() -> None:
    op.drop_index('idx_public_charger_lat_lon', table_name='public_chargers')
    op.drop_index('idx_public_charger_country', table_name='public_chargers')
    op.drop_table('public_chargers')

