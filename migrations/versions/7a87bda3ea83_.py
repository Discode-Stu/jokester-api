"""empty message

Revision ID: 7a87bda3ea83
Revises: 07c193d5566b
Create Date: 2020-09-14 20:39:07.461042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a87bda3ea83'
down_revision = '07c193d5566b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=500),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###