# Gmail & Google Docs MCP Server

This Model Context Protocol (MCP) server allows AI assistants to:
1. Send emails via your Gmail account.
2. Append text to your Google Docs or local files.

## Setup Instructions

### 1. Install Dependencies

In this directory, install the required Python packages:

```bash
pip3 install -r requirements.txt
```

### 2. Get Google OAuth Credentials

To use the Google APIs, you need to create a project in Google Cloud Console and download an OAuth client ID:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the following APIs for your project:
   - **Gmail API**
   - **Google Docs API**
4. Go to **APIs & Services > OAuth consent screen**. Configure the consent screen (choose "External" if you are a regular Gmail user, or "Internal" if you are on Google Workspace). You must add your email as a test user if the app is in Testing mode.
5. Go to **APIs & Services > Credentials**.
6. Click **Create Credentials** > **OAuth client ID**.
7. Choose **Desktop app** as the application type.
8. Click **Create** and then download the JSON file.
9. Rename the downloaded file to `credentials.json` and place it in this directory (`/Users/aparanaraghuvanshi/Mcp server/gmail-docs-mcp`).

### 3. Generate the Token

Before the MCP server can run headless, you need to authenticate once:

```bash
python3 auth_setup.py
```

This will open a browser window asking you to log into your Google account and grant permissions. Once completed, a `token.json` file will be created in this directory.

### 4. Configuring your AI Client (Claude Desktop / Cursor)

#### For Claude Desktop
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gmail-docs": {
      "command": "python3",
      "args": ["/Users/aparanaraghuvanshi/Mcp server/gmail-docs-mcp/server.py"]
    }
  }
}
```
*(Make sure to replace `python` with the absolute path to your python executable if you are using a virtual environment).*

#### For Cursor
Go to Cursor Settings > Features > MCP, and add a new MCP server:
- **Type**: `command`
- **Name**: `gmail-docs-mcp`
- **Command**: `python3 "/Users/aparanaraghuvanshi/Mcp server/gmail-docs-mcp/server.py"`

## Deployment (Railway)

To host this MCP Server in the cloud 24/7, you can deploy it to [Railway](https://railway.app/).

1. **Push to GitHub**: Commit this entire folder to a private GitHub repository.
2. **Deploy on Railway**: 
   - Go to Railway, click **New Project** -> **Deploy from GitHub repo**.
   - Select your repository.
3. **Configure Persistent Volume**:
   - In your Railway project, go to **Settings** -> **Volumes**.
   - Click **Add Volume** and set the Mount Path to `/app/data`.
4. **Authenticate in Production**:
   - Your initial deploy will fail because `credentials.json` is missing.
   - Go to the **Terminal** tab of your service in the Railway dashboard.
   - Run `cd /app/data`.
   - Upload or create your `credentials.json` here (e.g. `cat > credentials.json` and paste your JSON, then press `Ctrl+D`).
   - Run `python3 /app/auth_setup.py`. Follow the link to authenticate.
   - A `token.json` will be saved to `/app/data`.
5. **Connect Client to Cloud**:
   Instead of using a local command, configure your AI Client (Cursor/Claude) to connect via Server-Sent Events (SSE) using the URL provided by Railway (e.g., `https://your-app.up.railway.app/sse`).

## Usage

Once connected, your AI assistant will have access to:
- `send_gmail(to, subject, body)`
- `append_to_doc(document_id_or_path, content_to_append)`
