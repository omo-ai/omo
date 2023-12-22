"""add object_id col

Revision ID: 8fe556082641
Revises: b0eec74e32be
Create Date: 2023-12-21 10:43:25.048108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fe556082641'
down_revision: Union[str, None] = 'b0eec74e32be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gdriveobject', sa.Column('object_id', sa.String(), server_default='BACKFILL', nullable=False))
    op.create_index(op.f('ix_gdriveobject_object_id'), 'gdriveobject', ['object_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_gdriveobject_object_id'), table_name='gdriveobject')
    op.drop_column('gdriveobject', 'object_id')
    # ### end Alembic commands ###