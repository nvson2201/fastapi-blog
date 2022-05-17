from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0013'
down_revision = '0012'
branch_labels = None
depends_on = None


def upgrade():
    # create favorites table
    op.create_table(
        'favorites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_post_id'), 'favorites',
                    ['post_id'], unique=False)
    op.create_index(op.f('ix_user_id'), 'favorites',
                    ['user_id'], unique=False)
    op.create_index(op.f('ix_favorites_id'),
                    'favorites', ['id'], unique=False)


def downgrade():
    op.drop_table('favorites')
