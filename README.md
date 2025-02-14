# Gmail API Email Extractor

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
>>>>>>> b1820f1 (Initial commit: Gmail API Email Fetcher)
