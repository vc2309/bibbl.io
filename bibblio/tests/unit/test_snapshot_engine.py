import pytest
from lambda_folder.pkg.engine import SnapShotEngine

def test_create_snaps_from_empty_smart_notes():
    smart_notes = []
    expected_snapshots = []
    engine = SnapShotEngine()

    assert engine.create_snaps(smart_notes) == expected_snapshots

def test_create_snaps_normal():
    smart_notes = [{
        "user_id": "test_user",
        "smart_note_id": "1"},
    {
        "user_id": "test_user",
        "smart_note_id": "3"},
    {
        "user_id": "test_user",
        "smart_note_id": "6"},
    {
        "user_id": "test_user",
        "smart_note_id": "32"},
    {
        "user_id": "test_user",
        "smart_note_id": "4"},
    {
        "user_id": "test_user",
        "smart_note_id": "9"},
    {
        "user_id": "test_user",
        "smart_note_id": "11"}
    ]

    chunk_size = 3
    expected_snaps = [
        {
            'user_id' : "test_user",
            'smart_note_list' : ["1","3","6"],
            'status' : 'Pending_Delivery'
        },
        {
            'user_id' : "test_user",
            'smart_note_list' : ["32","4","9"],
            'status' : 'Pending_Delivery'
        },
        {
            'user_id' : "test_user",
            'smart_note_list' : ["11"],
            'status' : 'Pending_Delivery'
        }
    ]

    engine = SnapShotEngine()
    actual_snaps = engine.create_snaps(smart_notes, chunk_size=3)
    assert len(expected_snaps) == len(actual_snaps)

    for a,b in zip(expected_snaps, actual_snaps):
        for key in a:
            assert a[key] == b[key]
    
