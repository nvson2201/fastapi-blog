"""create posts table

Revision ID: baf7d4bacbd0
Revises: 2dc8cdf26964
Create Date: 2022-04-29 09:28:27.884992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'baf7d4bacbd0'
down_revision = '2dc8cdf26964'
branch_labels = None
depends_on = None


def upgrade():
    # create posts table
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=50), nullable=True),
        sa.Column('body', sa.String(length=255), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_id'), 'posts', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_post_id'), table_name='posts')
    op.drop_table('posts')
