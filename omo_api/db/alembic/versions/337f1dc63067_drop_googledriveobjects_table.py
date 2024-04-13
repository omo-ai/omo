"""drop googledriveobjects table

Revision ID: 337f1dc63067
Revises: a46723f7a099
Create Date: 2024-04-12 16:56:40.482125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '337f1dc63067'
down_revision: Union[str, None] = 'a46723f7a099'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_gdriveobject_name', table_name='gdriveobject')
    op.drop_index('ix_gdriveobject_object_id', table_name='gdriveobject')
    op.drop_table('gdriveobject')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gdriveobject',
    sa.Column('service_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('last_edited_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('size_bytes', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('last_synced_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('drive_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('object_id', sa.VARCHAR(), server_default=sa.text("'BACKFILL'::character varying"), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['drive_id'], ['googledriveconfig.id'], name='gdriveobject_drive_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='gdriveobject_pkey')
    )
    op.create_index('ix_gdriveobject_object_id', 'gdriveobject', ['object_id'], unique=False)
    op.create_index('ix_gdriveobject_name', 'gdriveobject', ['name'], unique=False)
    # ### end Alembic commands ###