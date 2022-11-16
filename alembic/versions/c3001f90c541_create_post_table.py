"""create post table

Revision ID: c3001f90c541
Revises: 
Create Date: 2022-11-12 18:50:43.051618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3001f90c541'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # create post table
  
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                            sa.Column('title', sa.String(), nullable = False),
                            sa.Column('content', sa.String(), nullable=False),
                            sa.Column('published', sa.Boolean(),nullable=False, server_default='TRUE'),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                            server_default=sa.text('now()'),nullable=False))
    
    pass


def downgrade():
    op.drop_table("posts")
    pass
