import boto3

db_client = boto3.client("dynamodb")
from pkg.engine import RawNoteEngine, SmartNoteEngine, SnapShotEngine
from pkg.dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO
from pkg.dao import S3Dao

RAW_NOTES_TABLE = "raw-notes"
SMART_NOTES_TABLE = "smart-notes"
SNAP_SHOTS_TABLE = "snap-shots"
raw_notes_dao = RawNotesDAO(RAW_NOTES_TABLE)
smart_notes_dao = SmartNotesDAO(SMART_NOTES_TABLE)
snap_shot_dao = SnapShotsDAO(SNAP_SHOTS_TABLE)

object_key_list = [
    "test_user/Extreme Economies-Notebook.html",
    "test_user/Being Mortal-Notebook.html.html",
    "test_user/Zero to One-Notebook.html",
    "test_user/The Righteous Mind-Notebook.html",
]

for object_key in object_key_list:
    raw_notes = raw_notes_dao.get_notes_by_s3_objkey(object_key)
    for item in raw_notes:
        raw_notes_dao.delete_item_by_id(item["note_id"])
    smart_notes = smart_notes_dao.get_notes_by_s3_objkey(object_key)
    for item in smart_notes:
        smart_notes_dao.delete_item_by_id(item["smart_note_id"])
    snapshots = snap_shot_dao.get_snapshots_by_user_id("test_user")
    for item in snapshots:
        print(item)
        snap_shot_dao.delete_item_by_id(item["snap_shot_id"])
