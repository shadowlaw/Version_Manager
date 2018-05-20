"""empty message

Revision ID: 38cf60181d56
Revises: 7b0e4ebcb15b
Create Date: 2018-05-20 01:00:34.055236

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '38cf60181d56'
down_revision = '7b0e4ebcb15b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group_list_assoc',
    sa.Column('list_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('list_id', 'group_id')
    )
    op.drop_column(u'app_list', 'group_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'app_list', sa.Column('group_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_table('group_list_assoc')
    # ### end Alembic commands ###
