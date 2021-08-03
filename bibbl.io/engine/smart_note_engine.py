from typing import List
from models import SmartNote, Note


class SmartNoteEngine(object):
    """
    Fabricates SmartNote objects from groups of Note objects
    """

    def __init__(self) -> None:
        super().__init__()

    def generate_smart_notes(notes: List[Note]) -> List[SmartNote]:
        """
        TO-DO: Placeholder logic - will be built upon
        """
        result = []
        for note in notes:
            result.append(
                SmartNote(
                    upload_uri=note.upload_uri,
                    user_id=note.user_id,
                    book_id=note.book_id,
                    text=note.text,
                )
            )
        return result
