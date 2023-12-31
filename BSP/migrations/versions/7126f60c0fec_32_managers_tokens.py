"""32 Managers tokens

Revision ID: 7126f60c0fec
Revises: df4d4438bedb
Create Date: 2023-06-24 12:00:48.415641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7126f60c0fec'
down_revision = 'df4d4438bedb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('managers', sa.Column('password', sa.String(length=255), nullable=False))
    op.add_column('managers', sa.Column('refresh_token', sa.String(length=255), nullable=True))
    op.add_column('managers', sa.Column('reset_password_token', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('managers', 'reset_password_token')
    op.drop_column('managers', 'refresh_token')
    op.drop_column('managers', 'password')
    # ### end Alembic commands ###
