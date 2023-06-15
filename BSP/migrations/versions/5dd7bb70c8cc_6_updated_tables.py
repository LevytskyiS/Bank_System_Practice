"""6 Updated tables

Revision ID: 5dd7bb70c8cc
Revises: 0aab2f8ee8c2
Create Date: 2023-06-13 18:40:08.443197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dd7bb70c8cc'
down_revision = '0aab2f8ee8c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clientm2mbank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('banks_m2m_clients')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banks_m2m_clients',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('bank_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], name='banks_m2m_clients_bank_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name='banks_m2m_clients_client_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='banks_m2m_clients_pkey')
    )
    op.drop_table('clientm2mbank')
    # ### end Alembic commands ###