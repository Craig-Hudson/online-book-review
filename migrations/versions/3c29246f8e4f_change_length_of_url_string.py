"""change length of url string

Revision ID: 3c29246f8e4f
Revises: 
Create Date: 2023-11-16 22:34:20.246731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c29246f8e4f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=512),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###
