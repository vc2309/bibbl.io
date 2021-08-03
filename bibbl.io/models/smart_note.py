from . import NoteBase
import uuid


class SmartNote(NoteBase):
    """
    Smart notes are aggregated, summarised and enriched text segments compiled from raw Note objects.
    """

    def __init__(
        self,
        upload_uri: str,
        user_id: str,
        book_id: str,
        text: str,
        metadata: dict = None,
        smart_note_id: str = None,
        create_uuid: bool = True,
    ) -> None:
        super().__init__(
            upload_uri=upload_uri,
            user_id=user_id,
            book_id=book_id,
            text=text,
            metadata=metadata,
        )
        if smart_note_id:
            self.smart_note_id = smart_note_id
        elif create_uuid:
            self.smart_note_id = str(uuid.uuid4())

    @property
    def smart_note_id(self):
        return self._smart_note_id

    @smart_note_id.setter
    def smart_note_id(self, smart_note_id):
        if not hasattr(self, "_smart_note_id"):
            self._smart_note_id = smart_note_id

    @property
    def note_ids(self):
        return self._note_ids

    @note_ids.setter
    def note_ids(self, note_ids):
        if not hasattr(self, "_note_ids"):
            self._note_ids = note_ids

    @classmethod
    def create_smart_note_from_db_item(cls, item: dict):
        instance = cls.create_note_base_from_db_item(item)
        smart_note_id = item.get("smart_note_id")
        noted_ids = item.get("note_ids")
        if not smart_note_id:
            raise ValueError("smart_note_id is missing in item")
        smart_note_id_val = smart_note_id.get("S")
        if noted_ids:
            instance.note_ids = noted_ids.get("SS")
        instance.smart_note_id = smart_note_id_val
        return instance
