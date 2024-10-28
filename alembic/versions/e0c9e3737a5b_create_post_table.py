"""create post table

Revision ID: e0c9e3737a5b
Revises: 
Create Date: 2024-10-28 14:58:22.994100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0c9e3737a5b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(200), nullable=False))


def downgrade():
    op.drop_table('posts')
    pass
