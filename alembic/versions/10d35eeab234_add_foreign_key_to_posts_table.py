"""add foreign key to posts table

Revision ID: 10d35eeab234
Revises: bcf2bf3ea7b3
Create Date: 2022-11-16 09:52:55.665916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10d35eeab234'
down_revision = 'bcf2bf3ea7b3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')

    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('owner_id')
    pass
