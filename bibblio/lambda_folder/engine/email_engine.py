import boto3
import os
from botocore.exceptions import ClientError

SENDER = "yashvardhannevatia@icloud.com"
AWS_REGION = "eu-west-2"
SUBJECT = "Bibblio - In case you forgot"
CHARSET = "UTF-8"


class EmailEngine():
    """
    Provide a wrapper around the DynamoDB API to fetch Notes from the given table
    """
    def __init__(self) -> None:
        self.client = boto3.client('ses',region_name=AWS_REGION)
    def send_email(self, email_id, content):
        BODY_TEXT = self.format_content(content)
        try:
            response = self.client.send_email(
                Destination={'ToAddresses': [email_id]},
                Message={
                    'Body': {
                        # 'Html': {'Charset': CHARSET,'Data': BODY_HTML,},
                        'Text': {'Charset': CHARSET,'Data': BODY_TEXT,},
                    },
                    'Subject': {'Charset': CHARSET,'Data': SUBJECT,},
                },
                Source=SENDER,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
    def format_content(self, content):
        text = ''
        text += 'Book Title: ' + content['book_title'] + "\n"
        for i, note in enumerate(content['notes']):
            text += str(i+1) + ". " + note + "\n"
        return (text)
