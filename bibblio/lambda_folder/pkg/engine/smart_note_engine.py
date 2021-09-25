from typing import List
from ..dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO
import uuid


class SmartNoteEngine(object):
    def __init__(self) -> None:
        super().__init__()

    def trim_text(self, text: str) -> str:
        start_index, end_index = None, None
        text_len = len(text)
        for i in range(0, text_len):
            if start_index == None or end_index == None:
                # the open quotation mark was copied from the text
                # not sure if this is the best way
                if start_index == None and (text[i].isupper() or text[i] == "“"):
                    start_index = i
                if end_index == None and text[text_len - i - 1] in [".","?","!","\""]:
                    end_index = text_len - i - 1
        if start_index != None and end_index != None:
            return text[start_index:end_index + 1]
        return ""

    def create_smart_notes(self, raw_notes: List) -> List:
        """
        Generate a list of SmartNotes given `raw_notes`.
        """
        smart_notes = []
        for note in raw_notes:
            trimmed_text = self.trim_text(note["note_text"].replace("\n", ""))
            if not trimmed_text: continue
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
                    "note_text": trimmed_text,
                    "snap_id": "",
                    "last_added": "",
                }
                smart_notes.append(obj)
            except KeyError as e:
                print(e)

        return smart_notes
