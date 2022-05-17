from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0012'
down_revision = '0011'
branch_labels = None
depends_on = None


def upgrade():
    # create posts_to_tags table
    op.create_table(
        'posts_to_tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=True),
        sa.Column('tag_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['tag_id'], ['tags.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_post_id'), 'posts_to_tags',
                    ['post_id'], unique=False)
    op.create_index(op.f('ix_tag_id'), 'posts_to_tags',
                    ['post_id'], unique=False)
    op.create_index(op.f('ix_posts_to_tags_id'),
                    'posts_to_tags', ['id'], unique=False)


def downgrade():
    op.drop_table('posts_to_tags')
