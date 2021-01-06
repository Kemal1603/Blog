"""Add a column

Revision ID: 74c13b12aa70
Revises: 
Create Date: 2021-01-06 11:55:32.555690

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '74c13b12aa70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	op.drop_column('blog_posts', 'description')


def downgrade():
	pass
