"""add other post table columns

Revision ID: 78383c469311
Revises: 9977f741302f
Create Date: 2024-10-28 15:56:25.500985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78383c469311'
down_revision: Union[str, None] = '9977f741302f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='1'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text('now()')))

    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts', 'created_at')

    pass
