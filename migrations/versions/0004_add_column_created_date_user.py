from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns create_date and is_banned to users table
    op.add_column(
        'users',
        sa.Column('created_date', sa.DateTime,
                  default=datetime.datetime.utcnow),
        sa.Column('is_banned', sa.Boolean(), nullable=True)
    ),


def downgrade():
    op.drop_column('users', 'created_date')
