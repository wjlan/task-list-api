"""empty message

Revision ID: abb8b0b6d160
Revises: 60e84c640125
Create Date: 2022-11-09 16:49:31.982488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abb8b0b6d160'
down_revision = '60e84c640125'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###