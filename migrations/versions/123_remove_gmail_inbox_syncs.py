"""Remove gmail inbox syncs

Revision ID: 3c743bd31ee2
Revises:476c5185121b
Create Date: 2014-12-08 03:53:36.829238

"""

# revision identifiers, used by Alembic.
revision = '3c743bd31ee2'
down_revision = '476c5185121b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Remove UIDs and sync status for inbox IMAP syncs -- otherwise
    # archives/deletes may not be synced correctly.
    from inbox.models.backends.imap import ImapFolderSyncStatus, ImapUid
    from inbox.models import Folder
    from inbox.models.backends.gmail import GmailAccount
    from inbox.models.session import session_scope
    with session_scope(ignore_soft_deletes=False, versioned=False) as \
            db_session:
        import pdb; pdb.set_trace()
        # STOPSHIP(emfree) this just deletes everything :(
        q = db_session.query(ImapFolderSyncStatus). \
            join(Folder, sa.and_(ImapFolderSyncStatus.folder_id == Folder.id,
                                 Folder.canonical_name == 'inbox')). \
            join(GmailAccount, Folder.account_id == GmailAccount.id)
        q.delete()

        q = db_session.query(ImapUid). \
            join(Folder, sa.and_(ImapUid.folder_id == Folder.id,
                                 Folder.canonical_name == 'inbox')). \
            join(GmailAccount, Folder.account_id == GmailAccount.id)

        q.delete()
        db_session.commit()


def downgrade():
    pass
