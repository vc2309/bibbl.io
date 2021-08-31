import boto3
from bs4 import BeautifulSoup
import uuid
from datetime import date, timedelta
from collections import Counter
# from dao.s3_dao import S3Dao # how is this working with lamdba

class NoteEngine(object):
    """
    Fabricates Rawnotes objects from s3 file
    """
    def __init__(self) -> None:
        super().__init__()

class RawNoteEngine(NoteEngine):
    def __init__(self) -> None:
        super().__init__()
    def parse_kindle_file(self, bucket_name, object_key, userid, s3_dao):
        """
        Gets Kindle File from s3 and parses the same
        params - bucket_name - string - s3 bucket name
        params - object_key - string - s3 object key
        params - userid - string - user id of this kindle file
        params - s3_dao - S3Dao - object for accessing s3
        returns - list - raw note objects
        """
        print("Parsing Kindle File")
        file_body = s3_dao.get_kindle_file(bucket_name, object_key)
        soup = BeautifulSoup(file_body, 'html.parser')
        title = soup.find("div", {"class": "bookTitle"}).text
        authors = soup.find("div", {"class": "authors"}).text
        print('Title:', title)
        print('Authors:', authors)
        parsed = soup.find_all(True, {'class':['sectionHeading', 'noteHeading', 'noteText']})
        # return parsed
        current_section_heading = ''
        current_note_heading = ''
        parsed_notes = []
        for item in parsed:
            if item.has_attr('class'):
                if item['class'][0] == 'sectionHeading': current_section_heading = item.text
                elif item['class'][0] == 'noteHeading': current_note_heading = item.text
                elif item['class'][0] == 'noteText':
                    # hack to exclude next higlight being included in text
                    note_text = item.text[:(item.text.find("Highlight ("))]
                    obj = {
                    'note_id' : str(uuid.uuid1()),
                    'user_id' : userid,
                    's3_upload_bucket' : bucket_name,
                    's3_upload_object' : object_key,
                    'book_title' : title,
                    'book_author': authors,
                    'note_chapter': current_section_heading,
                    'note_type_and_location': current_note_heading,
                    'note_text': note_text
                    }
                    parsed_notes.append(obj)
        return parsed_notes

class SmartNoteEngine(NoteEngine):
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

class SnapShotEngine(NoteEngine):
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
