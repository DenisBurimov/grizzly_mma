"""transaction_reseller_foreign_key

Revision ID: ec40cb66b438
Revises: 028fbf789e91
Create Date: 2022-05-16 11:51:17.902456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec40cb66b438'
down_revision = '028fbf789e91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('reseller_id', sa.Integer(), nullable=True))
    op.drop_constraint('transactions_user_id_fkey', 'transactions', type_='foreignkey')
    op.create_foreign_key(None, 'transactions', 'users', ['reseller_id'], ['id'])
    op.drop_column('transactions', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.create_foreign_key('transactions_user_id_fkey', 'transactions', 'users', ['user_id'], ['id'])
    op.drop_column('transactions', 'reseller_id')
    # ### end Alembic commands ###
