"""alter_column_qnt_seguidores_table_artist

Revision ID: a93229511c16
Revises: 7ea3bc3ef34b
Create Date: 2024-08-21 15:47:52.978823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a93229511c16'
down_revision: Union[str, None] = '7ea3bc3ef34b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('artists') as batch_op:
        batch_op.alter_column('qntd_seguidores', existing_type=sa.String(), type_=sa.Integer())


def downgrade() -> None:
    with op.batch_alter_table('artists') as batch_op:
        batch_op.alter_column('qntd_seguidores', existing_type=sa.Integer(), type_=sa.String())
