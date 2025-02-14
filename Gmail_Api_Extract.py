from __future__ import print_function
import os
import base64
import json
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the required Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate and return the Gmail API service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def extract_emails(service, max_results=10):
    """Extract emails from Gmail inbox."""
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    email_data = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
        
        parts = payload.get('parts', [])
        body = ''
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
        
        email_data.append({
            'sender': sender,
            'subject': subject,
            'body': body
        })
    
    return email_data

if __name__ == '__main__':
    gmail_service = authenticate_gmail()
    emails = extract_emails(gmail_service)
    
    print(json.dumps(emails, indent=4))

# Create a README.md file
readme_content = """# Gmail API Email Extractor

This project is a **Python script** that connects to the **Gmail API** to extract and display emails from your inbox. It uses **OAuth2 authentication** and retrieves email details such as the sender, subject, and body.

## Features
- Authenticate using **OAuth 2.0** with Google API.
- Fetch emails from your **Gmail inbox**.
- Extract **sender, subject, and body**.
- Output emails in **JSON format**.

## Prerequisites
- **Python 3.7+**
- Google Cloud account with **Gmail API enabled**
- `credentials.json` file (OAuth 2.0 credentials)
- Required Python libraries (see installation below)

## Installation

### Step 1: Clone this Repository
```sh
git clone https://github.com/your-username/gmail-api-extract.git
cd gmail-api-extract
```

### Step 2: Install Dependencies
```sh
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 3: Setup Credentials
1. Go to **Google Cloud Console** → Enable **Gmail API**.
2. Generate OAuth 2.0 credentials and download `credentials.json`.
3. Place `credentials.json` in the project folder.

### Step 4: Run the Script
```sh
python gmail_api_extract.py
```

On first run, a browser window will open asking for **Google authentication**.

## Output Example
```json
[
    {
        "sender": "example@gmail.com",
        "subject": "Meeting Reminder",
        "body": "Don't forget our meeting at 3 PM."
    },
    {
        "sender": "noreply@google.com",
        "subject": "Security Alert",
        "body": "Your account was accessed from a new device."
    }
]
```

## License
This project is **MIT Licensed**.
"""

with open("README.md", "w", encoding="utf-8") as readme_file:
    readme_file.write(readme_content)

