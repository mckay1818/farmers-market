"""adds Product, Customer, Order, and OrderProduct models after properly registering in app factory fn

Revision ID: b56962de9cd9
Revises: b9bc1a37bce3
Create Date: 2023-01-26 09:10:06.233856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b56962de9cd9'
down_revision = 'b9bc1a37bce3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('address_1', sa.String(length=80), nullable=False),
    sa.Column('city', sa.String(length=80), nullable=False),
    sa.Column('region', sa.String(length=80), nullable=False),
    sa.Column('postal_code', sa.Integer(), nullable=False),
    sa.Column('credits', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.Column('is_shipped', sa.Boolean(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['seller_id'], ['seller.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_product',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('order_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_product')
    op.drop_table('product')
    op.drop_table('order')
    op.drop_table('customer')
    # ### end Alembic commands ###
