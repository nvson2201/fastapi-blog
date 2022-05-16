from alembic import op
import sqlalchemy as sa

revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('posts', 'owner_id',
                    new_column_name='author_id', existing_type=sa.Integer())


def downgrade():
    op.alter_column('posts', 'author_id',
                    new_column_name='owner_id', existing_type=sa.Integer())
