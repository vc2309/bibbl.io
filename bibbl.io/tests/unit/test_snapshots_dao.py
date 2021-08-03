import pytest


def test_get_snapshot_by_user_id(insert_snapshots, snapshots_dao):
    expected_snapshots = [
        {
            "snapshot_id": {"S": "example-snapshot-01"},
            "user_id": {"S": "user01"},
            "upload_uri": {"S": "vishnu.com"},
            "smart_note_ids": {"SS": ["smart-note01", "smart-note02"]},
        },
        {
            "snapshot_id": {"S": "example-snapshot-02"},
            "user_id": {"S": "user01"},
            "upload_uri": {"S": "vishnu.com"},
            "smart_note_ids": {"SS": ["smart-note03", "smart-note02"]},
        },
    ]
    actual_snapshots = snapshots_dao.get_snapshots_by_user_id("user01")
    key = lambda x: x["snapshot_id"]["S"]
    for a, b in zip(
        sorted(expected_snapshots, key=key), sorted(actual_snapshots, key=key)
    ):
        assert a["snapshot_id"] == b["snapshot_id"]
        assert a["user_id"] == b["user_id"]
        assert sorted(a["smart_note_ids"]["SS"]) == sorted(b["smart_note_ids"]["SS"])


def test_get_snapshots_empty(snapshots_dao):
    assert snapshots_dao.get_snapshots_by_user_id("...") == []


# def test_write_snapshot(snapshots_dao):
#     snapshot_id = snapshots_dao.
