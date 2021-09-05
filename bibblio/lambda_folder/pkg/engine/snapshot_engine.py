from datetime import date, timedelta
import uuid
from ..dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO

class SnapShotEngine(object):
    def __init__(self) -> None:
        super().__init__()

    def create_snaps(self, object_key, smart_notes_dao = None):
        """
        Gets smart notes from dynamodb and creates snaps
        params - object_key - string -  s3 object key
        params - smart_notes_dao - SmartNotesDAO - object for accessing smart_notes
        returns - list -  snap objects
        """
        if not smart_notes_dao: smart_notes_dao = SmartNotesDAO()
        smart_notes = smart_notes_dao.get_item_by_index('s3_upload_object', object_key)
        print('len smart notes', len(smart_notes))
        chunks = [smart_notes[x:x+5] for x in range(0, len(smart_notes), 5)]
        print('len chunks', len(chunks))
        snapshots = []
        today = date.today()
        for i, item in enumerate(chunks):
            obj = {
                'snap_shot_id' : str(uuid.uuid1()),
                'user_id' : item[0]['user_id'],
                'smart_note_list' : [x['smart_note_id'] for x in item],
                'delivery_date' : str(today + timedelta(days=i)),
                'status' : 'Pending_Delivery'
            }
            print(obj)
            snapshots.append(obj)
        return snapshots

    def get_snap_content_by_snap_id(self, snap_id, snap_shots_dao = None, smart_notes_dao = None):
        """
        Gets snap from dynamodb, get smart notes in snap, create final
        snap content
        params - snap_id - string -  snap object id
        params - snap_shots_dao - SnapShotsDAO - object for accessing snapshots
        params - smart_notes_dao - SmartNotesDAO - object for accessing smart notes
        returns - list -  snap objects
        """
        if not snap_shots_dao: snap_shots_dao = SnapShotsDAO()
        snap = snap_shots_dao.get_item_by_id(snap_id)
        if not smart_notes_dao: smart_notes_dao  = SmartNotesDAO()
        content = {'notes':[], 'book_title': ''}
        for smart_note_id in snap['smart_note_list']:
            smart_note = smart_notes_dao.get_item_by_id(smart_note_id)
            if not content['book_title']: content['book_title'] = smart_note['book_title']
            content['notes'].append(smart_note['note_text'])
        return content