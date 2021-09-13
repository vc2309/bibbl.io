import json

import pytest

import os
import boto3

def test_fetch_notes(insert_items, notes_dao):
    expected_results = [
        {
            "note_id": "example-note-01",
            "text": "abcd",
            "s3_upload_object": "vishnu.com",
        }
    ]

    actual_results = notes_dao.get_notes_by_s3_objkey("vishnu.com")

    assert expected_results == actual_results


def test_fetch_notes_non_existent_item(notes_dao):
    assert notes_dao.get_notes_by_s3_objkey("vishnu.com") == []


def test_fetch_notes_non_string_uri(notes_dao):
    assert notes_dao.get_notes_by_s3_objkey(5) == []
