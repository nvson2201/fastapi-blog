from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0018'
down_revision = '0017'
branch_labels = None
depends_on = None


def upgrade():
    # create favorites table
    op.create_table(
        'codes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('body', sa.String(length=50), nullable=True),
        sa.Column('fails', sa.Integer(), nullable=True),
        sa.Column('time_lock_send_code', sa.DateTime, nullable=True),
        sa.Column('time_lock_fail', sa.DateTime, nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_user_id'), 'codes',
                    ['user_id'], unique=False)
    op.create_index(op.f('ix_code_id'),
                    'codes', ['id'], unique=False)


def downgrade():
    op.drop_table('codes')
