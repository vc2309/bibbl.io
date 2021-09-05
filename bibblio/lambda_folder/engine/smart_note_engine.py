from lambda_folder.dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO
import uuid
class SmartNoteEngine(object):
    def __init__(self) -> None:
        super().__init__()
    def parse_raw_notes(self, object_key, raw_notes_dao = None):
        """
        Gets raw notes from dynamodb and parses to smart notes
        params - object_key - string -  s3 object key
        params - raw_notes_dao - RawNotesDAO - object for accessing raw notes
        returns - list -  smart note objects
        """
        print("Parsing Raw Notes")
        if not raw_notes_dao: raw_notes_dao = RawNotesDAO()
        raw_notes = raw_notes_dao.get_item_by_index('s3_upload_object', object_key)
        smart_notes = []
        for note in raw_notes:
            obj = {
            'smart_note_id' : str(uuid.uuid1()),
            'raw_note_id' : note['note_id'],
            'user_id' : note['user_id'],
            's3_upload_bucket' : note['s3_upload_bucket'],
            's3_upload_object' : note['s3_upload_object'],
            'book_title' : note['book_title'].replace('\n',''),
            'book_author': note['book_author'].replace('\n',''),
            'note_chapter': note['note_chapter'].replace('\n',''),
            'note_type_and_location': note['note_type_and_location'],
            'note_text': note['note_text'].replace('\n',''),
            'snap_id': '',
            'last_added': ''
            }
            smart_notes.append(obj)
        return smart_notes
