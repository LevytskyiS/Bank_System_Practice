"""7 Updated tables

Revision ID: 23e773f03fb1
Revises: 5dd7bb70c8cc
Create Date: 2023-06-13 18:46:45.431581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23e773f03fb1'
down_revision = '5dd7bb70c8cc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('clients_email_key', 'clients', type_='unique')
    op.drop_constraint('clients_passport_number_key', 'clients', type_='unique')
    op.drop_constraint('clients_phone_key', 'clients', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('clients_phone_key', 'clients', ['phone'])
    op.create_unique_constraint('clients_passport_number_key', 'clients', ['passport_number'])
    op.create_unique_constraint('clients_email_key', 'clients', ['email'])
    # ### end Alembic commands ###
