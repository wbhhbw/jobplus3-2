"""complete job table

Revision ID: 99a5252b1638
Revises: cd076d7133ae
Create Date: 2018-01-21 18:48:09.896610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99a5252b1638'
down_revision = 'cd076d7133ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'job', 'company', ['company_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'job', type_='foreignkey')
    op.drop_column('job', 'company_id')
    # ### end Alembic commands ###
