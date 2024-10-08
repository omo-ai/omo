"""add connectors column to usercelerytask

Revision ID: b338de28165a
Revises: cf7f4249cc31
Create Date: 2024-04-18 08:53:58.830965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b338de28165a'
down_revision: Union[str, None] = 'cf7f4249cc31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # This should also be a no-op (see previous down_revision)
    # This column will get created automatically
    # op.add_column('usercelerytasks', sa.Column('connector', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    # ### end Alembic commands ###
    pass


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_column('usercelerytasks', 'connector')
    # ### end Alembic commands ###
    pass
