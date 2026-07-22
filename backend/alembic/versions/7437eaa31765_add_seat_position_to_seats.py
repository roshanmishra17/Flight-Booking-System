"""add seat_position to seats

Revision ID: 7437eaa31765
Revises: b904c83867a0
Create Date: 2026-07-23 01:43:26.783102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '7437eaa31765'
down_revision: Union[str, Sequence[str], None] = 'b904c83867a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    seat_position_enum = postgresql.ENUM(
        "window",
        "middle",
        "aisle",
        name="seat_position",
    )

    seat_position_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "seats",
        sa.Column(
            "seat_position",
            seat_position_enum,
            nullable=False,
        ),
    )


def downgrade() -> None:
    seat_position_enum = postgresql.ENUM(
        "window",
        "middle",
        "aisle",
        name="seat_position",
    )

    op.drop_column(
        "seats",
        "seat_position",
    )

    seat_position_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )
