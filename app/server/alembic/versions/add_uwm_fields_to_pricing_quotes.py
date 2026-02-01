"""Add UWM API fields to pricing_quotes table

Revision ID: add_uwm_fields
Revises: 493e9d321d7f
Create Date: 2025-12-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_uwm_fields'
down_revision: Union[str, Sequence[str], None] = '493e9d321d7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add UWM-specific fields to pricing_quotes table."""
    # Add uwm_scenario_id column for tracking UWM scenarios
    op.add_column(
        'pricing_quotes',
        sa.Column(
            'uwm_scenario_id',
            sa.String(length=100),
            nullable=True,
            comment='UWM scenario identifier for quote tracking'
        )
    )

    # Add uwm_request_payload to store the exact request sent to UWM
    op.add_column(
        'pricing_quotes',
        sa.Column(
            'uwm_request_payload',
            sa.JSON(),
            nullable=True,
            comment='Original request payload sent to UWM API'
        )
    )

    # Add request_params to store the internal request parameters before mapping
    op.add_column(
        'pricing_quotes',
        sa.Column(
            'request_params',
            sa.JSON(),
            nullable=True,
            comment='Internal request parameters before UWM mapping'
        )
    )

    # Create index on uwm_scenario_id for faster lookups
    op.create_index(
        'ix_pricing_quotes_uwm_scenario_id',
        'pricing_quotes',
        ['uwm_scenario_id'],
        unique=False
    )


def downgrade() -> None:
    """Remove UWM-specific fields from pricing_quotes table."""
    op.drop_index('ix_pricing_quotes_uwm_scenario_id', table_name='pricing_quotes')
    op.drop_column('pricing_quotes', 'request_params')
    op.drop_column('pricing_quotes', 'uwm_request_payload')
    op.drop_column('pricing_quotes', 'uwm_scenario_id')
