"""create comments table

Revision ID: 86a3ae93c923
Revises: baf7d4bacbd0
Create Date: 2022-04-29 09:31:37.798299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86a3ae93c923'
down_revision = 'baf7d4bacbd0'
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
            ['contain_id'], ['posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_id'), 'comments', ['id'], unique=False)


def downgrade():
    op.drop_table('comments')
