"""drop booking table

Revision ID: 1a083d1e1960
Revises: 89b0f3afaded
Create Date: 2025-06-26 23:39:12.924213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a083d1e1960'
down_revision = '89b0f3afaded'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('notification')
    op.drop_table('booking')


def downgrade() -> None:
    pass