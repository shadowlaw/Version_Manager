"""empty message

Revision ID: 6c177213dae3
Revises: a37b8b44feab
Create Date: 2018-03-19 03:31:16.295745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c177213dae3'
down_revision = 'a37b8b44feab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application_list', sa.Column('name', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('application_list', 'name')
    # ### end Alembic commands ###
