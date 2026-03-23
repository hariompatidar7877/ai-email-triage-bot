import os
import base64
from email import message_from_bytes

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate_gmail():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    return service


def get_unread_emails():

    print("Connecting to Gmail...")

    service = authenticate_gmail()

    print("Fetching messages...")

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],   # changed from UNREAD to INBOX
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    print("Messages found:", len(messages))

    email_texts = []

    for msg in messages:

        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="raw"
        ).execute()

        raw_msg = base64.urlsafe_b64decode(msg_data["raw"])

        mime_msg = message_from_bytes(raw_msg)

        if mime_msg.is_multipart():

            for part in mime_msg.walk():

                if part.get_content_type() == "text/plain":

                    email_texts.append(
                        part.get_payload(decode=True).decode(errors="ignore")
                    )

        else:

            email_texts.append(
                mime_msg.get_payload(decode=True).decode(errors="ignore")
            )

    print("Emails extracted:", len(email_texts))

    return email_texts