"""Added spotify ids

Revision ID: 3523ac1dd6c5
Revises: f40ed8955b3f
Create Date: 2021-01-09 19:30:34.556987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3523ac1dd6c5'
down_revision = 'f40ed8955b3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('spotify_id', sa.String(), nullable=True))
    op.add_column('playlists', sa.Column('spotify_id', sa.String(), nullable=True))
    op.add_column('tracks', sa.Column('spotify_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tracks', 'spotify_id')
    op.drop_column('playlists', 'spotify_id')
    op.drop_column('artists', 'spotify_id')
    # ### end Alembic commands ###
