"""Audio fields

Revision ID: dd3e9f5e0fde
Revises: df098fbc6379
Create Date: 2021-05-18 00:37:09.818880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd3e9f5e0fde'
down_revision = 'df098fbc6379'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('collocation_dictionary', sa.Column('audio', sa.Boolean(), nullable=True))
    op.add_column('word', sa.Column('audio', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('word', 'audio')
    op.drop_column('collocation_dictionary', 'audio')
    # ### end Alembic commands ###
