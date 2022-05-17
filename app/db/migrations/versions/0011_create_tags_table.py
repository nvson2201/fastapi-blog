from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0011'
down_revision = '0010'
branch_labels = None
depends_on = None


def upgrade():
    # create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tag', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tag_id'), 'tags', ['id'], unique=False)
    op.create_index(op.f('ix_tag_tag'), 'tags', ['tag'], unique=False)


def downgrade():
    op.drop_table('tags')
