import uuid


class NoteBase(object):
    def __init__(
        self,
        upload_uri: str,
        user_id: str,
        book_id: str,
        text: str,
        metadata: dict = None,
        create_uuid: bool = True,
    ) -> None:
        self.upload_uri = upload_uri
        self.user_id = user_id
        self.book_id = book_id
        self.metadata = metadata
        self.text = text

    @classmethod
    def create_note_base_from_db_item(cls, item: dict):
        """
        Return a Note object from the given 'item' . The 'item' must be a valid Note record from a DynamoDB query.
        """
        upload_uri = item.get("upload_uri")
        user_id = item.get("user_id")
        book_id = item.get("book_id")
        text = item.get("text")

        if not (upload_uri and user_id):
            raise ValueError("Missing values for note_id or upload_uri or user_id")

        upload_uri_val = upload_uri.get("S")
        book_id_val = ""
        if book_id:
            book_id_val = book_id.get("S")
        user_id_val = user_id.get("S")
        text_val = ""
        if text:
            text_val = text.get("S")
        return cls(
            upload_uri=upload_uri_val,
            book_id=book_id_val,
            user_id=user_id_val,
            text=text_val,
            create_uuid=False,
        )

    @property
    def upload_uri(self):
        return self._upload_uri

    @upload_uri.setter
    def upload_uri(self, upload_uri):
        if not hasattr(self, "_upload_uri"):
            self._upload_uri = upload_uri

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        if not hasattr(self, "_user_id"):
            self._user_id = user_id

    @property
    def book_id(self):
        return self._book_id

    @book_id.setter
    def book_id(self, book_id):
        if not hasattr(self, "_book_id"):
            self._book_id = book_id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if not hasattr(self, "_text"):
            self._text = text

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        if not hasattr(self, "_metadata"):
            self._metadata = metadata


class Note(NoteBase):
    def __init__(
        self,
        upload_uri: str,
        user_id: str,
        book_id: str,
        text: str,
        metadata: dict = None,
        note_id: str = None,
        create_uuid: bool = True,
    ) -> None:
        super().__init__(
            upload_uri=upload_uri,
            user_id=user_id,
            book_id=book_id,
            text=text,
            metadata=metadata,
        )
        if note_id:
            self.note_id = note_id
        elif create_uuid:
            self.note_id = str(uuid.uuid4())

    @property
    def note_id(self):
        return self._note_id

    @note_id.setter
    def note_id(self, note_id):
        if not hasattr(self, "_note_id"):
            self._note_id = note_id

    @classmethod
    def create_note_from_db_item(cls, item: dict):
        instance = cls.create_note_base_from_db_item(item)
        note_id = item.get("note_id")
        if not note_id:
            raise ValueError("note_id is missing in item")
        note_id_val = note_id.get("S")
        instance.note_id = note_id_val
        return instance
