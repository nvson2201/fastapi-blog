from alembic import op
import sqlalchemy as sa


revision = '0009'
down_revision = '0008'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns updated_at to users table
    op.add_column(
        'users',
        sa.Column('updated_at', sa.DateTime),
    ),


def downgrade():
    op.drop_column('users', 'updated_at')
