"""Id of tasks

Revision ID: a24e48b8746a
Revises: 302902cf5e3a
Create Date: 2021-03-26 18:55:38.255681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a24e48b8746a'
down_revision = '302902cf5e3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_in_section', sa.Column('task_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_in_section', 'task_id')
    # ### end Alembic commands ###
