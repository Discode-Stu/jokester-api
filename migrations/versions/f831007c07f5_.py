"""empty message

Revision ID: f831007c07f5
Revises: 7422a54e4cbe
Create Date: 2020-09-15 13:32:41.389148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f831007c07f5'
down_revision = '7422a54e4cbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.TEXT(),
               type_=sa.Binary(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.Binary(),
               type_=sa.TEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###