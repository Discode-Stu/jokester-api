"""empty message

Revision ID: 0bb8611072da
Revises: f831007c07f5
Create Date: 2020-09-15 16:55:34.509414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bb8611072da'
down_revision = 'f831007c07f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.TEXT(),
               type_=sa.LargeBinary(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.LargeBinary(),
               type_=sa.TEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###