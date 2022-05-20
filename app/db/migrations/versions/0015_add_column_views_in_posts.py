from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0015'
down_revision = '0014'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns views to posts table
    op.add_column(
        'posts',
        sa.Column('views', sa.Integer(), nullable=False, default=0)
    ),


def downgrade():
    op.drop_column('posts', 'views')
