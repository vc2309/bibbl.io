from typing import List
from ..dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO
import uuid


class SmartNoteEngine(object):
    def __init__(self) -> None:
        super().__init__()

    def create_smart_notes(self, raw_notes: List) -> List:
        """
        Generate a list of SmartNotes given `raw_notes`.
        """
        smart_notes = []
        for note in raw_notes:
            try:
                obj = {
                    "smart_note_id": str(uuid.uuid1()),
                    "raw_note_id": note["note_id"],
                    "user_id": note["user_id"],
                    "s3_upload_bucket": note["s3_upload_bucket"],
                    "s3_upload_object": note["s3_upload_object"],
                    "book_title": note["book_title"].replace("\n", ""),
                    "book_author": (note.get("book_author") or "").replace("\n", ""),
                    "note_chapter": (note.get("note_chapter") or "").replace("\n", ""),
                    "note_type_and_location": note.get("note_type_and_location"),
                    "note_text": note["note_text"].replace("\n", ""),
                    "snap_id": "",
                    "last_added": "",
                }
                smart_notes.append(obj)
            except KeyError as e:
                print(e)

        return smart_notes
