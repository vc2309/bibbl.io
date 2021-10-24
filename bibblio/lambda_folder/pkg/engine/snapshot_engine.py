from datetime import date, timedelta, datetime
from typing import List
import uuid
from ..dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO, UserDAO


class SnapShotEngine(object):
    def __init__(self) -> None:
        super().__init__()

    def _get_latest_date(self, user_id):
        snap_shot_dao = SnapShotsDAO()
        today = date.today()
        # TODO: make status an enum to avoid string compare
        # NOTE: should we store the latest potential snap in the user table ?
        # NOTE: in snap table, we can only put pending snaps and create a separate table for old snaps ?
        existing_user_snaps = snap_shot_dao.get_snapshots_by_user_id(user_id)
        if not existing_user_snaps:
            return today
        print(existing_user_snaps)
        pending_user_snaps = list(
            filter(
                lambda x: (x.get("delivery_status") == "Pending"), existing_user_snaps
            )
        )
        if not pending_user_snaps:
            return today
        pending_dates = list(
            map(
                lambda x: datetime.strptime(x["delivery_date"], "%Y-%m-%d"),
                pending_user_snaps,
            )
        )
        latest_date = max(pending_dates).date()
        return latest_date + timedelta(days=1)

    def _get_chunk_size(self, user_id):
        user_dao = UserDAO()
        try:
            chunk_size = 3  # TO DO : Make this configurable by user
            return chunk_size
        except:
            return 1

    def _send_smart_note_update(self, smart_id_2_snap_id):
        smart_note_dao = SmartNotesDAO()
        for smart_id, snap_id in smart_id_2_snap_id.items():
            smart_note_dao.update_snap_id(smart_id, snap_id)

    def create_snaps(self, smart_notes: List, user_id="") -> List:
        """
        Create and return a list of Snapshots given the `smart_notes`
        """

        if not user_id:
            user_id = smart_notes[0]["user_id"]
        chunk_size = self._get_chunk_size(user_id)
        latest_date = self._get_latest_date(user_id)
        smart_note_chunks = [
            smart_notes[x : x + chunk_size]
            for x in range(0, len(smart_notes), chunk_size)
        ]
        print("len smart_note_chunks", len(smart_note_chunks))

        final_snapshots = []
        smart_id_2_snap_id = {}
        for i, snap_content in enumerate(smart_note_chunks):
            snap_shot_id = str(uuid.uuid1())
            for smart_note in snap_content:
                smart_id_2_snap_id[smart_note["smart_note_id"]] = snap_shot_id
            snap_obj = {
                "snap_shot_id": snap_shot_id,
                "user_id": user_id,
                "smart_note_list": [x["smart_note_id"] for x in snap_content],
                "delivery_date": str(latest_date + timedelta(days=i)),
                "delivery_status": "Pending",
            }
            print(snap_obj)
            final_snapshots.append(snap_obj)
        self._send_smart_note_update(smart_id_2_snap_id)
        return final_snapshots

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
