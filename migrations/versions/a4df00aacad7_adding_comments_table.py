"""Adding Comments Table

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
    # create comments table
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('body', sa.String(length=255), nullable=True),
        sa.Column('contain_id', sa.Integer(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ['contain_id'], ['post.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['owner_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_id'), 'comments', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_comment_id'), table_name='comments')
    op.drop_table('comments')
