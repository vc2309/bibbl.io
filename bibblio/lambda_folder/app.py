import json
import urllib
import boto3
import uuid
import os
from bs4 import BeautifulSoup
from pkg.engine import RawNoteEngine, SmartNoteEngine, SnapShotEngine
from pkg.dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO
from pkg.dao import S3Dao
RAW_NOTES_TABLE = os.environ.get('') or 'raw-notes'
SMART_NOTES_TABLE = os.environ.get('') or 'smart-notes'
SNAP_SHOTS_TABLE = os.environ.get('') or 'snap-shots'

def note_file_handler(event, context):
    print("Object Uploaded in S3")
    print("event", event)
    print("context", context)
    user_id = 'test_user'
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print("Bucket Name of Object", bucket_name)
    print("Object Key of Object", object_key)
    parser = RawNoteEngine()
    parsed_notes = parser.parse_kindle_file(bucket_name, object_key, user_id, S3Dao())
    print("Kindle file parsed, Saving notes")
    raw_notes_dao = RawNotesDAO(RAW_NOTES_TABLE)
    saved = raw_notes_dao.save_notes(parsed_notes)
    print("Raw Notes saved, parsing for smart notes")
    smart_notes_engine = SmartNoteEngine()
    parsed_smart_notes = smart_notes_engine.parse_raw_notes(object_key, raw_notes_dao)
    print("Raw Notes parsed, saving for smart notes")
    smart_notes_dao = SmartNotesDAO(SMART_NOTES_TABLE)
    saved = smart_notes_dao.save_notes(parsed_smart_notes)
    print("Smart Notes saved, creating snaps")
    snap_engine = SnapShotEngine()
    snaps = snap_engine.create_snaps(object_key, smart_notes_dao)
    print("Saving snap shots")
    snap_shot_dao = SnapShotsDAO(SNAP_SHOTS_TABLE)
    snap_shot_dao.save_snapshot(snaps)


def test_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }
