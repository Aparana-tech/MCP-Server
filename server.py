import os
import base64
from email.message import EmailMessage

from mcp.server.fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Initialize FastMCP server
port = os.environ.get("PORT")
if port:
    mcp = FastMCP("Gmail and Google Docs Server", host="0.0.0.0", port=int(port))
else:
    mcp = FastMCP("Gmail and Google Docs Server")

# Scopes required for Gmail and Google Docs
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/documents'
]

def get_google_credentials():
    """Helper to get Google OAuth credentials from token.json."""
    data_dir = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(data_dir, 'token.json')
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save the refreshed credentials
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        else:
            raise RuntimeError(
                f"Valid credentials not found. Please run 'python auth_setup.py' "
                f"to generate token.json in {data_dir} first."
            )
    return creds

@mcp.tool()
def send_gmail(to: str, subject: str, body: str) -> str:
    """
    Sends an email using the authenticated user's Gmail account.
    
    Args:
        to: The email address of the recipient.
        subject: The subject of the email.
        body: The plain text body of the email.
    """
    try:
        creds = get_google_credentials()
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()
        message.set_content(body)
        message['To'] = to
        message['From'] = 'me'
        message['Subject'] = subject

        # Encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        # Send the message
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        return f"Message sent successfully! Message Id: {send_message['id']}"

    except HttpError as error:
        return f"An error occurred: {error}"
    except Exception as e:
        return f"Failed to send email: {e}"

@mcp.tool()
def append_to_doc(document_id_or_path: str, content_to_append: str) -> str:
    """
    Appends text to a Google Doc or a local text file.
    
    Args:
        document_id_or_path: The Google Docs ID (e.g., from the URL) OR an absolute path to a local file.
        content_to_append: The text to append.
    """
    # Check if it's a local file path
    if os.path.isabs(document_id_or_path) or '/' in document_id_or_path or '\\' in document_id_or_path:
        try:
            with open(document_id_or_path, 'a') as f:
                f.write("\n" + content_to_append)
            return f"Successfully appended to local file: {document_id_or_path}"
        except Exception as e:
            return f"Failed to append to local file: {e}"

    # Otherwise assume it's a Google Doc ID
    try:
        creds = get_google_credentials()
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=document_id_or_path).execute()
        
        # Find the end index of the document
        content = document.get('body').get('content')
        end_index = content[-1].get('endIndex') - 1 # Insert right before the final newline

        requests = [
            {
                'insertText': {
                    'location': {
                        'index': end_index,
                    },
                    'text': "\n" + content_to_append
                }
            }
        ]

        result = service.documents().batchUpdate(
            documentId=document_id_or_path, body={'requests': requests}).execute()

        return f"Successfully appended text to Google Doc (ID: {document_id_or_path})."
    
    except HttpError as error:
        return f"An error occurred with Google Docs API: {error}"
    except Exception as e:
        return f"Failed to append to document: {e}"

if __name__ == "__main__":
    # Start the FastMCP server
    if port:
        # Running in the cloud (Railway) -> use SSE
        mcp.run(transport="sse")
    else:
        # Running locally -> use stdio
        mcp.run()
