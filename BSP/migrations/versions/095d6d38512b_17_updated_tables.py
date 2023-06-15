"""17 Updated tables

Revision ID: 095d6d38512b
Revises: 7b0d39ab5efe
Create Date: 2023-06-15 11:10:28.374035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '095d6d38512b'
down_revision = '7b0d39ab5efe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'clients', ['passport_number'])
    op.create_unique_constraint(None, 'clients', ['phone'])
    op.create_unique_constraint(None, 'clients', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'clients', type_='unique')
    op.drop_constraint(None, 'clients', type_='unique')
    op.drop_constraint(None, 'clients', type_='unique')
    # ### end Alembic commands ###
