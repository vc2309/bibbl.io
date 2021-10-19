import pytest
from lambda_folder.pkg.engine import SnapShotEngine
from datetime import date, timedelta, datetime

def test_create_snaps_from_empty_smart_notes(insert_user):
    smart_notes = []
    expected_snapshots = []
    engine = SnapShotEngine()

    assert engine.create_snaps(smart_notes, 'test_user') == expected_snapshots

def test_create_snaps_normal(insert_user):
    smart_notes = [{
        "user_id": "user01",
        "smart_note_id": "1"},
    {
        "user_id": "user01",
        "smart_note_id": "3"},
    {
        "user_id": "user01",
        "smart_note_id": "6"},
    {
        "user_id": "user01",
        "smart_note_id": "32"},
    {
        "user_id": "user01",
        "smart_note_id": "4"},
    {
        "user_id": "user01",
        "smart_note_id": "9"},
    {
        "user_id": "user01",
        "smart_note_id": "11"}
    ]

    chunk_size = 3
    expected_snaps = [
        {
            'user_id' : "user01",
            'smart_note_list' : ["1","3","6"],
            'delivery_status' : 'Pending'
        },
        {
            'user_id' : "user01",
            'smart_note_list' : ["32","4","9"],
            'delivery_status' : 'Pending'
        },
        {
            'user_id' : "user01",
            'smart_note_list' : ["11"],
            'delivery_status' : 'Pending'
        }
    ]

    engine = SnapShotEngine()
    actual_snaps = engine.create_snaps(smart_notes, 'user01')
    assert len(expected_snaps) == len(actual_snaps)

    for a,b in zip(expected_snaps, actual_snaps):
        for key in a:
            assert a[key] == b[key]

def test_get_latest_date(insert_user, insert_snapshots):
    engine = SnapShotEngine()
    date = engine._get_latest_date('user01')
    assert str(date) == '2021-01-03'
