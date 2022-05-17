from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0014'
down_revision = '0013'
branch_labels = None
depends_on = None


def upgrade():
    # create followers_to_followings table
    op.create_table(
        'followers_to_followings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('follower_id', sa.Integer(),
                  nullable=True),
        sa.Column('following_id', sa.Integer(),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['follower_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['following_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_follower_id'), 'followers_to_followings',
                    ['follower_id'], unique=False)
    op.create_index(op.f('ix_following_id'), 'followers_to_followings',
                    ['following_id'], unique=False)
    op.create_index(op.f('ix_followers_to_followings_id'),
                    'followers_to_followings', ['id'], unique=False)


def downgrade():
    op.drop_table('followers_to_followings')
