"""create_ranking_model

Revision ID: 7ea3bc3ef34b
Revises: 227fcdefcdf2
Create Date: 2024-08-20 14:59:13.036948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ea3bc3ef34b'
down_revision: Union[str, None] = '227fcdefcdf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Rankings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ranking_genero', sa.JSON(), nullable=True),
        sa.Column('ranking_top_genero', sa.JSON(), nullable=True),
        sa.Column('audit_user_ip', sa.String(length=16), nullable=False),
        sa.Column('audit_created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('audit_updated_on', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('audit_user_login', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('Rankings')
