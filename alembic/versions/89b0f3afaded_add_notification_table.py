"""add notification table

Revision ID: 89b0f3afaded
Revises: 91d707b16289
Create Date: 2025-06-24 22:25:01.493734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89b0f3afaded'
down_revision = '91d707b16289'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('notification_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('level', sa.Text(), nullable=True),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.PrimaryKeyConstraint('notification_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification')
    # ### end Alembic commands ###
