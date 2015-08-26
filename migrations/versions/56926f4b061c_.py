"""empty message

Revision ID: 56926f4b061c
Revises: None
Create Date: 2015-08-21 18:50:30.456326

"""

# revision identifiers, used by Alembic.
revision = '56926f4b061c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'users', ['author_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'author_id')
    ### end Alembic commands ###