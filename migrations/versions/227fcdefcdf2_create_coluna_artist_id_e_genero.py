"""create coluna artist_id e genero

Revision ID: 227fcdefcdf2
Revises: e29b76565839
Create Date: 2024-08-19 18:03:09.947679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '227fcdefcdf2'
down_revision: Union[str, None] = 'e29b76565839'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artists', sa.Column('id_artista', sa.String(), nullable=False))
    op.add_column('Artists', sa.Column('genero', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artists', 'genero')
    op.drop_column('Artists', 'id_artista')
    # ### end Alembic commands ###
