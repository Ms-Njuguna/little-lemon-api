from django.core.mail.backends.base import BaseEmailBackend
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

class GmailApiBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        creds = Credentials(
            token=None,
            refresh_token=os.environ.get('GMAIL_REFRESH_TOKEN'),
            client_id=os.environ.get('GMAIL_CLIENT_ID'),
            client_secret=os.environ.get('GMAIL_CLIENT_SECRET'),
            token_uri='https://oauth2.googleapis.com/token',
            scopes=['https://www.googleapis.com/auth/gmail.send']
        )
        service = build('gmail', 'v1', credentials=creds)

        for message in email_messages:
            # Use HTML if available, otherwise use plain body
            content_type = 'plain'
            body_content = message.body
    
            if hasattr(message, 'alternatives') and message.alternatives:
                for content, mimetype in message.alternatives:
                    if mimetype == 'text/html':
                        body_content = content
                        content_type = 'html'
                        break

            mime_message = MIMEText(body_content, content_type)
            mime_message['to'] = ', '.join(message.to)
            mime_message['subject'] = message.subject
            raw = urlsafe_b64encode(mime_message.as_bytes()).decode()
            service.users().messages().send(userId='me', body={'raw': raw}).execute()

        return len(email_messages)