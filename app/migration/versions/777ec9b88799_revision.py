"""revision

Revision ID: 777ec9b88799
Revises: 1d9a83428938
Create Date: 2025-01-21 18:43:22.439509

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '777ec9b88799'
down_revision: str | None = '1d9a83428938'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('chat_id', sa.String(), nullable=True))
    op.drop_column('groups', 'chat_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('chat_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('groups', 'chat_id')
    # ### end Alembic commands ###
