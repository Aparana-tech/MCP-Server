import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/documents'
]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    data_dir = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(data_dir, 'token.json')
    creds_path = os.path.join(data_dir, 'credentials.json')

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"Error: {creds_path} not found!")
                print("Please download your OAuth 2.0 Client ID credentials from Google Cloud Console")
                print(f"and save it as 'credentials.json' in {data_dir}.")
                return
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            
    print("Authentication successful! token.json has been created or updated.")

if __name__ == '__main__':
    main()
