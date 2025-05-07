"""Test connection

Revision ID: f3aead1d8181
Revises: 50c1f1c11740
Create Date: 2025-05-07 09:26:44.785790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3aead1d8181'
down_revision: Union[str, None] = '50c1f1c11740'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
