"""add has_accommodation to charging_locations

Revision ID: add_has_accomm
Revises: add_public_chargers_table
Create Date: 2025-09-11 10:10:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_has_accomm'
down_revision = 'add_public_chargers_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('charging_locations', sa.Column('has_accommodation', sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.drop_column('charging_locations', 'has_accommodation')
