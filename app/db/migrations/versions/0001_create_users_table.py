from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(
            length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(
            length=225), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_user_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_user_full_name'), 'users',
                    ['full_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'users', ['id'], unique=False)


def downgrade():
    op.drop_table('users')
