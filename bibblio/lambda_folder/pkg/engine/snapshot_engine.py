from datetime import date, timedelta
from typing import List
import uuid
from ..dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO


class SnapShotEngine(object):
    def __init__(self) -> None:
        super().__init__()

    def create_snaps(self, smart_notes: List, chunk_size=5) -> List:
        """
        Create and return a list of Snapshots given the `smart_notes`
        """
        chunks = [
            smart_notes[x : x + chunk_size]
            for x in range(0, len(smart_notes), chunk_size)
        ]
        print("len chunks", len(chunks))
        snapshots = []
        today = date.today()
        for i, item in enumerate(chunks):
            obj = {
                "snap_shot_id": str(uuid.uuid1()),
                "user_id": item[0]["user_id"],
                "smart_note_list": [x["smart_note_id"] for x in item],
                "delivery_date": str(today + timedelta(days=i)),
                "status": "Pending_Delivery",
            }
            print(obj)
            snapshots.append(obj)
        return snapshots

    def get_snap_content_by_snap_id(
        self, snap_id, snap_shots_dao=None, smart_notes_dao=None
    ):
        """
        Gets snap from dynamodb, get smart notes in snap, create final
        snap content
        params - snap_id - string -  snap object id
        params - snap_shots_dao - SnapShotsDAO - object for accessing snapshots
        params - smart_notes_dao - SmartNotesDAO - object for accessing smart notes
        returns - list -  snap objects
        """
        if not snap_shots_dao:
            snap_shots_dao = SnapShotsDAO()
        snap = snap_shots_dao.get_item_by_id(snap_id)
        if not smart_notes_dao:
            smart_notes_dao = SmartNotesDAO()
        content = {"notes": [], "book_title": ""}
        for smart_note_id in snap["smart_note_list"]:
            smart_note = smart_notes_dao.get_item_by_id(smart_note_id)
            if not content["book_title"]:
                content["book_title"] = smart_note["book_title"]
            content["notes"].append(smart_note["note_text"])
        return content
