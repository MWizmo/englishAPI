"""Collocation stats

Revision ID: f264b9e003b5
Revises: 59114ccf6e42
Create Date: 2021-04-28 00:22:07.346070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f264b9e003b5'
down_revision = '59114ccf6e42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_collocation_stat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('collocation_id', sa.Integer(), nullable=True),
    sa.Column('correct_attempts', sa.Integer(), nullable=True),
    sa.Column('wrong_attempts', sa.Integer(), nullable=True),
    sa.Column('last_try_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['collocation_id'], ['collocation.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_collocation_stat')
    # ### end Alembic commands ###
