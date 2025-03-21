"""updated response model

Revision ID: e5620eabda6c
Revises: 32c9ea303506
Create Date: 2025-03-05 02:08:13.723861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5620eabda6c'
down_revision = '32c9ea303506'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('responseId', sa.String(length=100), nullable=False))
        batch_op.create_foreign_key(None, 'users', ['userId'], ['userId'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('responseId')

    # ### end Alembic commands ###
