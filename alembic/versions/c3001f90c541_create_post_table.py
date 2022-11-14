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


def upgrade() -> None:
    op.create_table("alembic-test",sa.Column("id", sa.Integer(), nullable= False, primary_key=True),
    sa.Column("description", sa.String()))
    pass


def downgrade() -> None:
    op.drop_table("alembic-test")
    pass
