"""Add spreadsheet config to user.

Revision ID: f36d15d8e86f
Revises: a3fb9237765e
Create Date: 2021-09-05 23:40:49.625504

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "f36d15d8e86f"
down_revision = "a3fb9237765e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("spreadsheet_id", sa.String(length=100), nullable=True)
    )
    op.add_column("user", sa.Column("sheet_name", sa.String(length=100), nullable=True))
    op.add_column("user", sa.Column("match_column", sa.String(length=3), nullable=True))
    op.add_column("user", sa.Column("date_column", sa.String(length=3), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "date_column")
    op.drop_column("user", "match_column")
    op.drop_column("user", "sheet_name")
    op.drop_column("user", "spreadsheet_id")
    # ### end Alembic commands ###