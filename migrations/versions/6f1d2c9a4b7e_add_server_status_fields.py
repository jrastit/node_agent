"""add server status fields

Revision ID: 6f1d2c9a4b7e
Revises: 10b5a3f48f96
Create Date: 2026-03-06 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6f1d2c9a4b7e"
down_revision: Union[str, Sequence[str], None] = "10b5a3f48f96"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("server", sa.Column("hostname", sa.String(), nullable=True))
    op.add_column("server", sa.Column("fqdn", sa.String(), nullable=True))
    op.add_column("server", sa.Column("os", sa.String(), nullable=True))
    op.add_column("server", sa.Column("kernel", sa.String(), nullable=True))
    op.add_column(
        "server", sa.Column("cpu_cores", sa.Integer(), nullable=True)
    )
    op.add_column(
        "server", sa.Column("ram_total_mb", sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("server", "ram_total_mb")
    op.drop_column("server", "cpu_cores")
    op.drop_column("server", "kernel")
    op.drop_column("server", "os")
    op.drop_column("server", "fqdn")
    op.drop_column("server", "hostname")
