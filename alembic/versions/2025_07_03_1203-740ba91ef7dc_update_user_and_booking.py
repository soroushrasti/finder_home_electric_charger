"""update user and booking

Revision ID: 740ba91ef7dc
Revises: 3a1a21ff70cd
Create Date: 2025-07-03 12:03:50.119063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '740ba91ef7dc'
down_revision = '3a1a21ff70cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('status', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('email_varification_code', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('is_validated', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('phone_varification_code', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_varification_code')
    op.drop_column('users', 'is_validated')
    op.drop_column('users', 'email_varification_code')
    op.drop_column('booking', 'status')
    # ### end Alembic commands ###
