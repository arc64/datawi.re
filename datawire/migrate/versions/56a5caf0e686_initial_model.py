"""initial model

Revision ID: 56a5caf0e686
Revises: None
Create Date: 2015-07-07 14:34:15.032821

"""

# revision identifiers, used by Alembic.
revision = '56a5caf0e686'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('login', sa.Unicode(length=255), nullable=True),
        sa.Column('email', sa.Unicode(), nullable=True),
        sa.Column('oauth_id', sa.Unicode(), nullable=True),
        sa.Column('api_key', sa.Unicode(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collection',
        sa.Column('id', sa.Unicode(length=50), nullable=False),
        sa.Column('slug', sa.Unicode(length=250), nullable=True),
        sa.Column('public', sa.Boolean(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entity',
        sa.Column('id', sa.Unicode(length=50), nullable=False),
        sa.Column('label', sa.Unicode(), nullable=True),
        sa.Column('category', sa.Enum('Person', 'Company', 'Organization', 'Other', name='entity_categories'), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=True),
        sa.Column('collection_id', sa.Unicode(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['collection_id'], ['collection.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('selector',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Unicode(), nullable=True),
        sa.Column('normalized', sa.Unicode(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('entity_id', sa.Unicode(length=50), nullable=True),
        sa.ForeignKeyConstraint(['entity_id'], ['entity.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_selector_normalized'), 'selector', ['normalized'], unique=False)
    op.create_index(op.f('ix_selector_text'), 'selector', ['text'], unique=False)


def downgrade():
    pass
