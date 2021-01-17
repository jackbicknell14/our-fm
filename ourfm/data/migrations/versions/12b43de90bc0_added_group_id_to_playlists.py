"""Added group id to playlists

Revision ID: 12b43de90bc0
Revises: 7db0ac809d99
Create Date: 2021-01-17 10:52:04.754299

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '12b43de90bc0'
down_revision = '7db0ac809d99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('playlists', sa.Column('group_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_index(op.f('ix_playlists_group_id'), 'playlists', ['group_id'], unique=False)
    op.create_foreign_key(None, 'playlists', 'groups', ['group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'playlists', type_='foreignkey')
    op.drop_index(op.f('ix_playlists_group_id'), table_name='playlists')
    op.drop_column('playlists', 'group_id')
    # ### end Alembic commands ###
