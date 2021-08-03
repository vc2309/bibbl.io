from . import SmartNote
import uuid


class Snapshot(object):
    """
    Model for a Bibbl Snapshot for a particular segment of a book for a user. Made up of a series of SmartNotes
    """

    def __init__(
        self,
        upload_uri: str,
        user_id: str,
        book_id: str = None,
        snapshot_id: str = None,
        create_uuid: bool = True,
    ):
        self.upload_uri = upload_uri
        self.user_id = user_id
        self.book_id = book_id
        self.smart_notes = []
        self.snapshot_id = (
            snapshot_id if snapshot_id else str(uuid.uuid4()) if create_uuid else None
        )

    def add_smart_note(self, smart_note: SmartNote):
        self.smart_notes.append(smart_note)
