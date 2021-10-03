import json
import urllib
import boto3
import uuid
import os
from datetime import date
from bs4 import BeautifulSoup
from pkg.engine import RawNoteEngine, SmartNoteEngine, SnapShotEngine, EmailEngine
from pkg.dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO, UserDAO
from pkg.dao import S3Dao

RAW_NOTES_TABLE = os.environ.get("") or "raw-notes"
SMART_NOTES_TABLE = os.environ.get("") or "smart-notes"
SNAP_SHOTS_TABLE = os.environ.get("") or "snap-shots"


def note_file_handler(event, context):
    print("Object Uploaded in S3")
    print("event", event)
    print("context", context)
    user_id = "test_user"
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    print("Bucket Name of Object", bucket_name)
    print("Object Key of Object", object_key)
    parser = RawNoteEngine()
    parsed_notes = parser.parse_kindle_file(bucket_name, object_key, user_id, S3Dao())
    print("Kindle file parsed, Saving notes")
    raw_notes_dao = RawNotesDAO(RAW_NOTES_TABLE)
    saved = raw_notes_dao.save_notes(parsed_notes)
    print("Raw Notes saved, parsing for smart notes")
    smart_notes_engine = SmartNoteEngine()
    parsed_smart_notes = smart_notes_engine.create_smart_notes(parsed_notes)
    if not parsed_smart_notes: return
    print("Raw Notes parsed, saving for smart notes")
    smart_notes_dao = SmartNotesDAO(SMART_NOTES_TABLE)
    saved = smart_notes_dao.save_notes(parsed_smart_notes)
    print("Smart Notes saved, creating snaps")
    snap_engine = SnapShotEngine()
    snaps = snap_engine.create_snaps(parsed_smart_notes, user_id)
    print("Saving snap shots")
    snap_shot_dao = SnapShotsDAO(SNAP_SHOTS_TABLE)
    snap_shot_dao.save_snapshot(snaps)
    return


def test_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }


def snap_delivery_handler(event, context):
    snap_shot_dao = SnapShotsDAO()
    snap_engine = SnapShotEngine()
    user_dao = UserDAO()
    email_engine = EmailEngine()
    delivery_snaps = snap_shot_dao.get_snaps_by_date(str(date.today()))
    for snap in delivery_snaps:
        content = snap_engine.get_snap_content_by_snap_id(snap['snap_shot_id'],
         snap_shot_dao, SmartNotesDAO())
        email_id = user_dao.get_user_by_userid(snap['user_id'])['email_id']
        email_engine.send_email(email_id, content)
        snap_shot_dao.update_snap_status(snap['snap_shot_id'], 'Delivered')
        # for smart_note_id in snap["smart_note_list"]:
        #     smart_note_dao.update_smart_note_status(smart_note_id, snap['snap_shot_id'])
        # TODO: update status of snap
        # TODO: update status of smart notes
