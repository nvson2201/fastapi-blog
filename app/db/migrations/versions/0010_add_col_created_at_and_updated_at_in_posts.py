from alembic import op
import sqlalchemy as sa

revision = '0010'
down_revision = '0009'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns updated_at to users table
    op.add_column(
        'posts',
        sa.Column('created_at', sa.DateTime),
    ),
    op.add_column(
        'posts',
        sa.Column('updated_at', sa.DateTime),
    )


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'updated_at')
