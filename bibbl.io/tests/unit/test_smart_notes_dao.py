import pytest
import os
import boto3


def test_get_smart_notes_by_uri(insert_smart_notes, smart_notes_dao):
    expected_smart_notes = [
        {
            "smart_note_id": {"S": "example-smart-note-01"},
            "text": {"S": "abcd 1234"},
            "upload_uri": {"S": "vishnu.com"},
        },
        {
            "smart_note_id": {"S": "example-smart-note-02"},
            "text": {"S": "xyz 1234"},
            "upload_uri": {"S": "vishnu.com"},
        },
    ]
    actual_smart_notes = smart_notes_dao.get_notes_by_upload_uri("vishnu.com")
    key = lambda x: x["smart_note_id"]["S"]
    assert sorted(actual_smart_notes, key=key) == sorted(expected_smart_notes, key=key)
