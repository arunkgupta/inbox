from datetime import datetime
from tests.util.base import (add_fake_message, add_fake_thread,
                             add_fake_imapuid)
from inbox.crispin import GmailFlags
from inbox.mailsync.backends.imap.common import (remove_deleted_uids,
                                                 update_metadata)
from inbox.models import Folder, Message, Thread

ACCOUNT_ID = 1
NAMESPACE_ID = 1


def test_only_uids_deleted_synchronously(db):
    folder_name = 'Inbox'
    msg_uid = 2222
    thread = add_fake_thread(db.session, NAMESPACE_ID)
    message = add_fake_message(db.session, NAMESPACE_ID, thread)
    add_fake_imapuid(db.session, ACCOUNT_ID, message, msg_uid,
                     folder_name)
    folder = db.session.query(Folder).filter(
        Folder.account_id == ACCOUNT_ID,
        Folder.name == folder_name).one()
    update_metadata(ACCOUNT_ID, db.session, folder_name, folder.id, [msg_uid],
                    {msg_uid: GmailFlags((), ('label',))})
    assert 'inbox' in [t.name for t in thread.tags]
    assert 'label' in [t.name for t in thread.tags]
    remove_deleted_uids(ACCOUNT_ID, db.session, [msg_uid], folder_name)
    message = db.session.query(Message).get(message.id)
    thread = db.session.query(Thread).get(thread.id)
    assert 'inbox' not in [t.name for t in thread.tags]
    assert 'label' not in [t.name for t in thread.tags]
    assert abs((message.deleted_at - datetime.utcnow()).total_seconds()) < 1
