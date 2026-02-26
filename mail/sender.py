import base64
import mimetypes
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os, pickle

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CREDS_FILE = r"C:\Users\Sanya\OneDrive\Document\projects\AutoOutreach-AI\mail\GMailCreds.json"

def get_gmail_service():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)

FIXED_SENDER = "guptasanya366@gmail.com"

def gmail_send_with_attachment(
    body_text: str,
    file_path: str,
    receiver_mail: str,
    subject: str,
):
    try:
        service = get_gmail_service()

        message = EmailMessage()
        message["To"] = receiver_mail
        message["From"] = FIXED_SENDER
        message["Subject"] = subject
        message.set_content(body_text)

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"
        maintype, subtype = mime_type.split("/")

        with open(file_path, "rb") as f:
            message.add_attachment(
                f.read(),
                maintype=maintype,
                subtype=subtype,
                filename=os.path.basename(file_path),
            )

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        send_body = {"raw": encoded_message}

        sent = (
            service.users()
            .messages()
            .send(userId="me", body=send_body)
            .execute()
        )

        return sent["id"]

    except HttpError as e:
        raise RuntimeError(f"Gmail API error: {e}")
    
def gmail_send_without_attachment(
    body_text: str,
    receiver_mail: str,
    subject: str,
):
    service = get_gmail_service()

    message = EmailMessage()
    message["To"] = receiver_mail
    message["From"] = FIXED_SENDER
    message["Subject"] = subject
    message.set_content(body_text)

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    send_body = {"raw": encoded_message}

    sent = (
        service.users()
        .messages()
        .send(userId="me", body=send_body)
        .execute()
    )

    return sent["id"]

'''
gmail_send_without_attachment(
    body_text="Demo mail 2",
    receiver_mail="guptasanya366@gmail.com",
    subject="demo auto mail",
)
'''

gmail_send_with_attachment(
    body_text="Demo mail with attachment",
    file_path=r"C:\Users\Sanya\Downloads\TOC tutorial sheet 4.pdf",
    receiver_mail="guptasanya366@gmail.com",
    subject="nun much",
)