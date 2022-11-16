"""create users table

Revision ID: bcf2bf3ea7b3
Revises: c3001f90c541
Create Date: 2022-11-16 08:33:20.842051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcf2bf3ea7b3'
down_revision = 'c3001f90c541'
branch_labels = None
depends_on = None


def upgrade():
     op.create_table('users',
                     sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(),nullable=False),
                     sa.Column('password', sa.String(), nullable=False),
                     sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                          server_default=sa.text('now()'), nullable=False),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('email'))
     pass


def downgrade():
    op.drop_table('users')
    pass
