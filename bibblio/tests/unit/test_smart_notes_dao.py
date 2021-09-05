import pytest
import os
import boto3


def test_get_smart_notes_by_uri(insert_smart_notes, smart_notes_dao):
    expected_smart_notes = [
        {
            "smart_note_id": "example-smart-note-01",
            "text": "abcd 1234",
            "s3_upload_object": "vishnu.com",
        },
        {
            "smart_note_id": "example-smart-note-02",
            "text": "xyz 1234",
            "s3_upload_object": "vishnu.com",
        },
    ]
    actual_smart_notes = smart_notes_dao.get_notes_by_s3_objkey("vishnu.com")
    key = lambda x: x["smart_note_id"]
    assert sorted(actual_smart_notes, key=key) == sorted(expected_smart_notes, key=key)
