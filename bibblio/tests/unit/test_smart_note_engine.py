import pytest
from lambda_folder.pkg.engine import SmartNoteEngine

def test_empty_raw_notes():
    engine = SmartNoteEngine()
    raw_notes = []
    assert engine.create_smart_notes(raw_notes) == []

def test_formatted_note():
    engine = SmartNoteEngine()
    raw_notes = [{
    "note_id": "ab55c8fd-0e98-11ec-a771-199d5676ef09",
    "user_id": "test_user",
    "note_chapter": "6. Letting Go",
    "book_title": "Being Mortal\n",
    "s3_upload_object": "test_user/Test.html",
    "note_text": "“ A large part of the task is helping people negotiate the overwhelming anxiety — anxiety about death , anxiety about suffering , anxiety about loved ones , anxiety about finances , ” she explained . “ There are many worries and real terrors . ” No one conversation can address them all . Arriving at an acceptance of one’s mortality and a clear understanding of the limits and the possibilities of medicine is a process , not an epiphany .\n",
    "s3_upload_bucket": "bibbl-notefilebucket-1v8xy57fre02p",
    "note_type_and_location": "Highlight (yellow) - Page 182 · Location 2562",
    "book_author": "\nGawande, Atul\n"
    }]
    expected_smart_notes = [{
        "snap_id":"",
        "note_chapter": "6. Letting Go",
        "s3_upload_object": "test_user/Test.html",
        "note_text":"“ A large part of the task is helping people negotiate the overwhelming anxiety — anxiety about death , anxiety about suffering , anxiety about loved ones , anxiety about finances , ” she explained . “ There are many worries and real terrors . ” No one conversation can address them all . Arriving at an acceptance of one’s mortality and a clear understanding of the limits and the possibilities of medicine is a process , not an epiphany .",
        "last_added": "",
        "user_id": "test_user",
        "raw_note_id": "ab55c8fd-0e98-11ec-a771-199d5676ef09",
        "book_title": "Being Mortal",
        "s3_upload_bucket": "bibbl-notefilebucket-1v8xy57fre02p",
        "note_type_and_location" : "Highlight (yellow) - Page 182 · Location 2562",
        "book_author" : "Gawande, Atul"
        }]

    actual_smart_notes = engine.create_smart_notes(raw_notes)
    print(actual_smart_notes[0]["note_text"])
    actual_smart_notes[0].pop("smart_note_id")
    assert actual_smart_notes == expected_smart_notes

def test_trimmed_smart_note():
    engine = SmartNoteEngine()
    raw_notes = [{
    "note_id": "ab55c8fd-0e98-11ec-a771-199d5676ef09",
    "user_id": "test_user",
    "note_chapter": "6. Letting Go",
    "book_title": "Being Mortal\n",
    "s3_upload_object": "test_user/Test.html",
    "note_text": "“ A large part of the task is helping people negotiate the overwhelming anxiety — anxiety about death , anxiety about suffering , anxiety about loved ones , anxiety about finances , ” she explained . “ There are many worries ",
    "s3_upload_bucket": "bibbl-notefilebucket-1v8xy57fre02p",
    "note_type_and_location": "Highlight (yellow) - Page 182 · Location 2562",
    "book_author": "\nGawande, Atul\n"
    }]
    expected_smart_notes = [{
    "snap_id":"",
    "note_chapter": "6. Letting Go",
    "s3_upload_object": "test_user/Test.html",
    "note_text":"“ A large part of the task is helping people negotiate the overwhelming anxiety — anxiety about death , anxiety about suffering , anxiety about loved ones , anxiety about finances , ” she explained .",
    "last_added": "",
    "user_id": "test_user",
    "raw_note_id": "ab55c8fd-0e98-11ec-a771-199d5676ef09",
    "book_title": "Being Mortal",
    "s3_upload_bucket": "bibbl-notefilebucket-1v8xy57fre02p",
    "note_type_and_location" : "Highlight (yellow) - Page 182 · Location 2562",
    "book_author" : "Gawande, Atul"
    }]
    actual_smart_notes = engine.create_smart_notes(raw_notes)
    print(actual_smart_notes[0]["note_text"])
    actual_smart_notes[0].pop("smart_note_id")
    assert actual_smart_notes == expected_smart_notes

def test_notes_with_missing_fields():
    engine = SmartNoteEngine()
    raw_notes = [{
    "note_id": "ab55c8fd-0e98-11ec-a771-199d5676ef09",
    "user_id": "test_user",
    # "note_chapter": "6. Letting Go", --> No chapter
    "book_title": "Being Mortal\n",
    "s3_upload_object": "test_user/Test.html",
    "note_text": "“ A large part of the task is helping people negotiate the overwhelming anxiety — anxiety about death , anxiety about suffering , anxiety about loved ones , anxiety about finances , ” she explained . “ There are many worries and real terrors . ” No one conversation can address them all . Arriving at an acceptance of one’s mortality and a clear understanding of the limits and the possibilities of medicine is a process , not an epiphany .\n",
    "s3_upload_bucket": "bibbl-notefilebucket-1v8xy57fre02p",
    "note_type_and_location": "Highlight (yellow) - Page 182 · Location 2562",
    "book_author": "\nGawande, Atul\n"
    }]

    expected_smart_notes = [{
        "snap_id":"",
        "note_chapter": "",
        "s3_upload_object": "test_user/Test.html",
        "note_text":"“ A large part of the task is helping people negotiate the overwhelming anxiety — anxiety about death , anxiety about suffering , anxiety about loved ones , anxiety about finances , ” she explained . “ There are many worries and real terrors . ” No one conversation can address them all . Arriving at an acceptance of one’s mortality and a clear understanding of the limits and the possibilities of medicine is a process , not an epiphany .",
        "last_added": "",
        "user_id": "test_user",
        "raw_note_id": "ab55c8fd-0e98-11ec-a771-199d5676ef09",
        "book_title": "Being Mortal",
        "s3_upload_bucket": "bibbl-notefilebucket-1v8xy57fre02p",
        "note_type_and_location" : "Highlight (yellow) - Page 182 · Location 2562",
        "book_author" : "Gawande, Atul"
  }]

    actual_smart_notes = engine.create_smart_notes(raw_notes)
    actual_smart_notes[0].pop("smart_note_id")
    assert actual_smart_notes == expected_smart_notes

def test_notes_with_missing_required_fields():
    engine = SmartNoteEngine()
    raw_notes = [{
    "note_id": "ab55c8fd-0e98-11ec-a771-199d5676ef09",
    # "user_id": "test_user", --> No user
    "note_chapter": "6. Letting Go",
    "book_title": "Being Mortal\n",
    "s3_upload_object": "test_user/Test.html",
    "note_text": "“ A large part of the task is helping people negotiate the overwhelming anxiety — anxiety about death , anxiety about suffering , anxiety about loved ones , anxiety about finances , ” she explained . “ There are many worries and real terrors . ” No one conversation can address them all . Arriving at an acceptance of one’s mortality and a clear understanding of the limits and the possibilities of medicine is a process , not an epiphany .\n",
    "s3_upload_bucket": "bibbl-notefilebucket-1v8xy57fre02p",
    "note_type_and_location": "Highlight (yellow) - Page 182 · Location 2562",
    "book_author": "\nGawande, Atul\n"
    }]


    actual_smart_notes = engine.create_smart_notes(raw_notes)
    assert actual_smart_notes == []
