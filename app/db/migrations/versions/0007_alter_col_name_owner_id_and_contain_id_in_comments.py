from alembic import op
import sqlalchemy as sa

revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('comments', 'owner_id',
                    new_column_name='author_id', existing_type=sa.Integer())
    op.alter_column('comments', 'contain_id',
                    new_column_name='post_id', existing_type=sa.Integer())


def downgrade():
    op.alter_column('comments', 'author_id',
                    new_column_name='owner_id', existing_type=sa.Integer())
    op.alter_column('comments', 'post_id',
                    new_column_name='contain_id', existing_type=sa.Integer())
