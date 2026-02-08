"""Update chat tables for Gemini function calling.

Revision ID: 7a2b9c3d4e5f
Revises: 3f8d2b9a7c1e
Create Date: 2026-01-21 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '7a2b9c3d4e5f'
down_revision = '3f8d2b9a7c1e'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns for Gemini function calling
    op.add_column('messages', sa.Column('function_call', JSONB, nullable=True))
    op.add_column('messages', sa.Column('function_response', JSONB, nullable=True))

    # Drop old column (optional, or keep for backward compatibility but application code removed it)
    op.drop_column('messages', 'tools_used')


def downgrade():
    # Revert changes
    op.add_column('messages', sa.Column('tools_used', sa.String(4000), nullable=True))
    op.drop_column('messages', 'function_response')
    op.drop_column('messages', 'function_call')
