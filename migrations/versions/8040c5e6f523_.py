"""empty message

Revision ID: 8040c5e6f523
Revises: 81e8d592bd18
Create Date: 2024-01-18 16:02:12.705516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8040c5e6f523'
down_revision = '81e8d592bd18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet_fav',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planet_fav')
    # ### end Alembic commands ###
