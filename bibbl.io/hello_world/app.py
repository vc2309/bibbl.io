import json
from dao import NotesDAO
from models import Note
from engine import SmartNoteEngine
# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    dao  = NotesDAO()
    print(dao)
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }

notes_dao = NotesDAO()
smart_note_engine = SmartNoteEngine()
def generate_smart_notes(upload_uri : str) -> None :
    """
    Collect all Notes corresponding to the imported file at `upload_uri` and generate and store SmartNote objects from these Notes.
    
    all_notes = notes_dao.get_notes_for_uri(upload_uri)
    smart_notes = smart_note_engine.generate(all_notes)
    for smart_note in smart_notes:
        smart_notes.dao.write_smart_note(smart_note)
    """
    records = notes_dao.get_notes_by_upload_uri()
    notes = [Note.create_note_from_db_item(record) for record in records]
    smart_notes = smart_note_engine.generate_smart_notes(notes)
    print(smart_notes)