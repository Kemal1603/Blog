"""create comment table

Revision ID: 14edb6e0b26e
Revises: 74c13b12aa70
Create Date: 2021-01-06 12:52:25.590550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14edb6e0b26e'
down_revision = '74c13b12aa70'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('author_id', sa.Integer, sa.ForeignKey("users.id")),
        sa.Column('post_id', sa.Integer, sa.ForeignKey("blog_posts.id")),
        sa.Column('text', sa.Text),
    )


def downgrade():
    pass
