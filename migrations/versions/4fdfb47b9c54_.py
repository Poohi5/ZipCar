"""empty message

Revision ID: 4fdfb47b9c54
Revises: 2dddcb0f1bba
Create Date: 2020-05-01 20:18:52.996924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fdfb47b9c54'
down_revision = '2dddcb0f1bba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('password', sa.String(length=10), nullable=False))
    op.drop_column('admin', 'passowrd')
    op.add_column('bookings', sa.Column('price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'price')
    op.add_column('admin', sa.Column('passowrd', sa.VARCHAR(length=10), autoincrement=False, nullable=False))
    op.drop_column('admin', 'password')
    # ### end Alembic commands ###
