"""Add notify column to db model

Revision ID: c161fdcfab19
Revises: 93a638b96375
Create Date: 2020-09-14 16:00:33.501681
"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'c161fdcfab19'
down_revision = '93a638b96375'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'newdles',
        sa.Column('notify', sa.Boolean(), server_default='false', nullable=False),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('newdles', 'notify')
    # ### end Alembic commands ###
