"""ListUserLink

Revision ID: d9129f1385be
Revises: 89e9998af2b3
Create Date: 2021-10-21 21:47:06.764643

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd9129f1385be'
down_revision = '89e9998af2b3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'list_user_link',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('list_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('read_only', sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(
            ['list_id'],
            ['list.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['user.id'],
        ),
        sa.PrimaryKeyConstraint('user_id', 'list_id'),
    )
    op.execute(
        '''
        INSERT INTO list_user_link(user_id, list_id, created_at, updated_at)
        SELECT user_id, id, created_at, updated_at
        FROM list
    '''
    )
    op.drop_constraint('list_user_id_fkey', 'list', type_='foreignkey')
    op.drop_column('list', 'user_id')


def downgrade():
    op.add_column('list', sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.execute('')  # TODO
    op.create_foreign_key('list_user_id_fkey', 'list', 'user', ['user_id'], ['id'])
    op.drop_table('list_user_link')
