"""gdrive_id can be null

Revision ID: 39892383a09a
Revises: b338de28165a
Create Date: 2024-04-23 07:10:05.509380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39892383a09a'
down_revision: Union[str, None] = 'b338de28165a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('googledriveconfig', 'gdrive_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('googledriveconfig', 'gdrive_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
