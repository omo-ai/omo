"""added files json type to GoogleDriveConfig

Revision ID: a46723f7a099
Revises: 13a3d0fa557a
Create Date: 2024-04-12 15:57:02.711502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a46723f7a099'
down_revision: Union[str, None] = '13a3d0fa557a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('googledriveconfig', sa.Column('files', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('googledriveconfig', 'files')
    # ### end Alembic commands ###