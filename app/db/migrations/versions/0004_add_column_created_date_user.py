from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns created_date to users table
    op.add_column(
        'users',
        sa.Column('created_date', sa.DateTime),
    ),


def downgrade():
    op.drop_column('users', 'created_date')
