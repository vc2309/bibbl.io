import boto3
from bs4 import BeautifulSoup
import uuid
from datetime import date, timedelta
from collections import Counter

# from dao.s3_dao import S3Dao # how is this working with lamdba
from ..dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO


class RawNoteEngine(object):
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
        soup = BeautifulSoup(file_body, "html.parser")
        title = soup.find("div", {"class": "bookTitle"}).text
        authors = soup.find("div", {"class": "authors"}).text
        print("Title:", title)
        print("Authors:", authors)
        parsed = soup.find_all(
            True, {"class": ["sectionHeading", "noteHeading", "noteText"]}
        )
        # return parsed
        current_section_heading = ""
        current_note_heading = ""
        parsed_notes = []
        for item in parsed:
            if item.has_attr("class"):
                if item["class"][0] == "sectionHeading":
                    current_section_heading = item.text
                elif item["class"][0] == "noteHeading":
                    current_note_heading = item.text
                elif item["class"][0] == "noteText":
                    # hack to exclude next higlight being included in text
                    note_text = item.text[: (item.text.find("Highlight ("))]
                    obj = {
                        "note_id": str(uuid.uuid1()),
                        "user_id": userid,
                        "s3_upload_bucket": bucket_name,
                        "s3_upload_object": object_key,
                        "book_title": title,
                        "book_author": authors,
                        "note_chapter": current_section_heading,
                        "note_type_and_location": current_note_heading,
                        "note_text": note_text,
                    }
                    parsed_notes.append(obj)
        return parsed_notes
