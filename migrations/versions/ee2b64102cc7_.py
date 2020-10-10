"""empty message

Revision ID: ee2b64102cc7
Revises: d5c3b30eaf6f
Create Date: 2020-05-01 12:16:03.685044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee2b64102cc7'
down_revision = 'd5c3b30eaf6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'dropoff_location')
    op.add_column('price', sa.Column('FirstDiscount', sa.Integer(), nullable=True))
    op.add_column('price', sa.Column('SecondDiscount', sa.Integer(), nullable=True))
    op.add_column('price', sa.Column('ThirdDiscount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('price', 'ThirdDiscount')
    op.drop_column('price', 'SecondDiscount')
    op.drop_column('price', 'FirstDiscount')
    op.add_column('bookings', sa.Column('dropoff_location', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###