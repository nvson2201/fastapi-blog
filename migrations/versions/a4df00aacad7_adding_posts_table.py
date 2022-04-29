"""Adding Posts Table

Revision ID: a4df00aacad7
Revises:
Create Date: 2022-04-16 22:49:04.121505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4df00aacad7'
down_revision = None
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
            ['owner_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_id'), 'posts', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_post_id'), table_name='posts')
    op.drop_table('posts')
