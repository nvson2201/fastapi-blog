from alembic import op
import sqlalchemy as sa


revision = '0016'
down_revision = '0015'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns username to users table
    op.add_column(
        'users',
        sa.Column('username', sa.String(length=50), nullable=False)
    ),
    op.create_index(op.f('ix_user_username'), 'users',
                    ['username'], unique=True)


def downgrade():
    op.drop_column('users', 'username')
