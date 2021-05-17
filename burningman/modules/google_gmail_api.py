import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
from lxml import etree


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class Email_Reader:
    def __init__(self):
        self.service = self.login()

    def login(self):
        creds = None
        token_path = os.path.join(os.path.dirname(__file__), 'authentication', 'token.json')
        credentials_path = os.path.join(os.path.dirname(__file__), 'authentication', 'credentials.json')
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def get_all_messages(self):
        result = self.service.users().messages().list(userId='me').execute()
        messages = result.get('messages')
        decoded_messages = []
        for message in messages:
            text = self.service.users().messages().get(userId='me', id=message['id']).execute()
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = text['payload']
                headers = payload['headers']
                parts = payload.get('parts')[1]
                data = parts['body']['data']
                data = data.replace("-","+").replace("_","/")
                decoded_data = base64.b64decode(data).decode("utf-8")
                decoded_messages.append({
                    'headers': headers,
                    'data': decoded_data
                })
            except Exception as e:
                pass
        return decoded_messages
        
    def get_activation_url(self, username: str):
        messages = self.get_all_messages()
        for message in messages:
            if username in message['data']:
                dom = etree.HTML(message['data'])
                return dom.xpath('//a[@id="reset-password-link"]')[0].get('href')
        return ''
