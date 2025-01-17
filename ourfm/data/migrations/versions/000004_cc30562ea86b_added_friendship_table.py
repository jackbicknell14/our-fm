"""Added friendship table

Revision ID: cc30562ea86b
Revises: 5232a969d3ce
Create Date: 2021-01-16 12:03:01.399632

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cc30562ea86b'
down_revision = '5232a969d3ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friends',
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('friend_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['friend_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'friend_id')
    )
    op.create_index(op.f('ix_friends_friend_id'), 'friends', ['friend_id'], unique=False)
    op.create_index(op.f('ix_friends_user_id'), 'friends', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_friends_user_id'), table_name='friends')
    op.drop_index(op.f('ix_friends_friend_id'), table_name='friends')
    op.drop_table('friends')
    # ### end Alembic commands ###
