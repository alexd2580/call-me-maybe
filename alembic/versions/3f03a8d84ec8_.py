"""Add oauth2 data to the user.

Revision ID: 3f03a8d84ec8
Revises: b2b7b990ed98
Create Date: 2021-09-05 20:56:21.587518

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "3f03a8d84ec8"
down_revision = "b2b7b990ed98"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("oauth2_state", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "user",
        sa.Column(
            "oauth2_credentials", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "oauth2_credentials")
    op.drop_column("user", "oauth2_state")
    # ### end Alembic commands ###
