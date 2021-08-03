from models import Note, SmartNote
import pytest


def test_create_note_from_record():
    record = {
        "note_id": {"S": "example-note-01"},
        "text": {"S": "abcd"},
        "upload_uri": {"S": "vishnu.com"},
        "user_id": {"S": "1203"},
    }
    note = Note.create_note_from_db_item(record)
    assert note.note_id == "example-note-01"
    assert note.text == "abcd"
    assert note.upload_uri == "vishnu.com"
    assert note.user_id == "1203"


def test_create_note_without_keys():
    record = {
        "note_id": {"S": "example-note-01"},
        "text": {"S": "abcd"},
        "user_id": {"S": "1203"},
    }

    with pytest.raises(ValueError):
        Note.create_note_from_db_item(record)


def test_create_smart_note_from_record():
    record = {
        "smart_note_id": {"S": "example-note-01"},
        "text": {"S": "abcd"},
        "upload_uri": {"S": "vishnu.com"},
        "user_id": {"S": "1203"},
        "note_ids": {"SS": ["note01", "note02"]},
    }
    note = SmartNote.create_smart_note_from_db_item(record)
    assert note.smart_note_id == "example-note-01"
    assert note.text == "abcd"
    assert note.upload_uri == "vishnu.com"
    assert note.user_id == "1203"
    assert sorted(note.note_ids) == sorted(["note01", "note02"])
