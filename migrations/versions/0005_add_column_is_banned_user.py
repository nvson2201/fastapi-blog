from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns create_date to users table
    op.add_column(
        'users',
        sa.Column('is_banned', sa.Boolean(), nullable=True)
    ),


def downgrade():
    op.drop_column('users', 'is_banned')
