"""modify company.name

Revision ID: 7b66c6831067
Revises: 10f9e057d94f
Create Date: 2018-01-23 21:00:10.628559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b66c6831067'
down_revision = '10f9e057d94f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_company_name', table_name='company')
    op.create_index(op.f('ix_company_name'), 'company', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_company_name'), table_name='company')
    op.create_index('ix_company_name', 'company', ['name'], unique=True)
    # ### end Alembic commands ###
