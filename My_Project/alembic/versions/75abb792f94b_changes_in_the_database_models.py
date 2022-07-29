"""Changes in the Database Models

Revision ID: 75abb792f94b
Revises: 80d14a269053
Create Date: 2022-07-29 14:28:10.588503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75abb792f94b'
down_revision = '80d14a269053'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doctors', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.drop_column('doctors', 'is_actives')
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.drop_column('users', 'is_actives')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_actives', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('users', 'is_active')
    op.add_column('doctors', sa.Column('is_actives', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('doctors', 'is_active')
    # ### end Alembic commands ###