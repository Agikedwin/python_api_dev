"""add content column to post table

Revision ID: 963da539fcc5
Revises: e0c9e3737a5b
Create Date: 2024-10-28 15:11:54.863609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '963da539fcc5'
down_revision: Union[str, None] = 'e0c9e3737a5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(250), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
