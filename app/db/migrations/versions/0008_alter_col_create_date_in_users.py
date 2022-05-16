from alembic import op
import sqlalchemy as sa

revision = '0008'
down_revision = '0007'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'created_date',
                    new_column_name='created_at',
                    existing_type=sa.DateTime())


def downgrade():
    op.alter_column('users', 'created_at',
                    new_column_name='created_date',
                    existing_type=sa.DateTime())
