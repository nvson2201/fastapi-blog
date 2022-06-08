from alembic import op
import sqlalchemy as sa


revision = '0019'
down_revision = '0018'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns avatar to users table
    op.add_column(
        'users',
        sa.Column('avatar', sa.String(length=50), nullable=True)
    )


def downgrade():
    op.drop_column('users', 'avatar')
