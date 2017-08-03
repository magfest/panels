"""Adds panel application fields

Revision ID: a3d71270256c
Revises: 416eb615ff1a
Create Date: 2017-08-03 15:42:52.406397

"""


# revision identifiers, used by Alembic.
revision = 'a3d71270256c'
down_revision = '416eb615ff1a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import sideboard



try:
    is_sqlite = op.get_context().dialect.name == 'sqlite'
except:
    is_sqlite = False

if is_sqlite:
    op.get_context().connection.execute('PRAGMA foreign_keys=ON;')
    utcnow_server_default = "(datetime('now', 'utc'))"
else:
    utcnow_server_default = "timezone('utc', current_timestamp)"

def sqlite_column_reflect_listener(inspector, table, column_info):
    """Adds parenthesis around SQLite datetime defaults for utcnow."""
    if column_info['default'] == "datetime('now', 'utc')":
        column_info['default'] = utcnow_server_default

sqlite_reflect_kwargs = {
    'listeners': [('column_reflect', sqlite_column_reflect_listener)]
}

# ===========================================================================
# HOWTO: Handle alter statements in SQLite
#
# def upgrade():
#     if is_sqlite:
#         with op.batch_alter_table('table_name', reflect_kwargs=sqlite_reflect_kwargs) as batch_op:
#             batch_op.alter_column('column_name', type_=sa.Unicode(), server_default='', nullable=False)
#     else:
#         op.alter_column('table_name', 'column_name', type_=sa.Unicode(), server_default='', nullable=False)
#
# ===========================================================================


def upgrade():
    if is_sqlite:
        with op.batch_alter_table('panel_applicant', reflect_kwargs=sqlite_reflect_kwargs) as batch_op:
            batch_op.add_column(sa.Column('communication_pref', sa.Unicode(), server_default='', nullable=False))
            batch_op.add_column(sa.Column('occupation', sa.Unicode(), server_default='', nullable=False))
            batch_op.add_column(sa.Column('other_communication_pref', sa.Unicode(), server_default='', nullable=False))
            batch_op.add_column(sa.Column('other_credentials', sa.Unicode(), server_default='', nullable=False))
            batch_op.add_column(sa.Column('social_media', sideboard.lib.sa.JSON(), server_default='{}', nullable=False))
            batch_op.add_column(sa.Column('website', sa.Unicode(), server_default='', nullable=False))
    else:
        op.add_column('panel_applicant', sa.Column('communication_pref', sa.Unicode(), server_default='', nullable=False))
        op.add_column('panel_applicant', sa.Column('occupation', sa.Unicode(), server_default='', nullable=False))
        op.add_column('panel_applicant', sa.Column('other_communication_pref', sa.Unicode(), server_default='', nullable=False))
        op.add_column('panel_applicant', sa.Column('other_credentials', sa.Unicode(), server_default='', nullable=False))
        op.add_column('panel_applicant', sa.Column('social_media', sideboard.lib.sa.JSON(), server_default='{}', nullable=False))
        op.add_column('panel_applicant', sa.Column('website', sa.Unicode(), server_default='', nullable=False))


def downgrade():
    op.drop_column('panel_applicant', 'website')
    op.drop_column('panel_applicant', 'social_media')
    op.drop_column('panel_applicant', 'other_credentials')
    op.drop_column('panel_applicant', 'other_communication_pref')
    op.drop_column('panel_applicant', 'occupation')
    op.drop_column('panel_applicant', 'communication_pref')