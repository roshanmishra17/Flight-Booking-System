"""add passenger contact fields

Revision ID: 288224d9e8c2
Revises: 7437eaa31765
Create Date: 2026-10-18 00:34:40.627814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '288224d9e8c2'
down_revision: Union[str, Sequence[str], None] = '7437eaa31765'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("bookings", sa.Column("passenger_age", sa.Integer(), nullable=True))
    op.add_column("bookings", sa.Column("passenger_phone", sa.String(15), nullable=True))
    op.add_column("bookings", sa.Column("passenger_email", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("bookings", "passenger_email")
    op.drop_column("bookings", "passenger_phone")
    op.drop_column("bookings", "passenger_age")
