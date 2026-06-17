# Railway Deployment Guide

This guide explains how to deploy the Gmail & Google Docs MCP Server to [Railway](https://railway.app/) for 24/7 cloud hosting.

Because this server uses Server-Sent Events (SSE) when deployed to the cloud, it can be accessed remotely via a secure URL instead of running locally on your machine.

## Prerequisites
- A GitHub account
- A Railway account
- Your `credentials.json` file from Google Cloud Console

---

## Step-by-Step Deployment

### 1. Push to GitHub
Commit this entire folder to a private GitHub repository. Railway will use this repository to build and deploy your Docker container automatically.

### 2. Deploy on Railway
1. Go to your Railway dashboard.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select your repository and wait for the initial build to start.

### 3. Configure Persistent Volume
Since Google OAuth requires saving a `token.json` file, we need a persistent volume so you don't have to re-authenticate every time Railway restarts your server.

1. In your Railway project dashboard, click on your deployed service.
2. Go to **Settings** -> **Volumes**.
3. Click **Add Volume**.
4. Set the Mount Path to `/app/data`.

### 4. Authenticate in Production
Your initial deploy will likely fail because it cannot find the `credentials.json` and `token.json` files. You need to provide them to the persistent volume.

1. Go to the **Terminal** tab of your service in the Railway dashboard.
2. Navigate to your persistent data directory by running:
   ```bash
   cd /app/data
   ```
3. Upload or create your `credentials.json` here. For example, run:
   ```bash
   cat > credentials.json
   ```
   Paste your JSON contents, press `Enter`, then press `Ctrl+D` to save.
4. Run the authentication setup script:
   ```bash
   python3 /app/auth_setup.py
   ```
5. The terminal will provide a URL. Follow the link, log in with your Google account, and grant the necessary permissions.
6. Once authenticated, a `token.json` file will automatically be saved to `/app/data`.
7. Restart your Railway service from the dashboard so it boots up correctly!

### 5. Connect Your AI Client
Instead of using a local Python command, you must configure your AI Client (Cursor, Claude Desktop, etc.) to connect via Server-Sent Events (SSE).

Find the public URL provided by Railway for your service (e.g., `https://your-app.up.railway.app`).

**For Claude Desktop**, update your config to use an SSE connection (refer to the MCP documentation for exact SSE config syntax for your client).
