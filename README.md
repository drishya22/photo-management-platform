# AI Photo Management Platform

## Features

- Upload photos
- Connect Google Photos
- Exact duplicate detection
- Near duplicate detection
- Automatic categorization
- Face grouping
- Natural language search
- Docker deployment

---

## Architecture

```text
                    ┌─────────────────┐
                    │   Streamlit UI  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ FastAPI Backend │
                    └────────┬────────┘
                             │
      ┌──────────────────────┼──────────────────────┐
      │                      │                      │
      ▼                      ▼                      ▼

┌──────────────┐    ┌────────────────┐    ┌──────────────┐
│ Hash Service │    │ CLIP Embedding │    │ Face Service │
└──────┬───────┘    └───────┬────────┘    └──────┬───────┘
       │                    │                    │
       ▼                    ▼                    ▼

Duplicate Check      ChromaDB Vector DB      Face Groups

                             │
                             ▼

                  ┌────────────────────┐
                  │ Semantic Search    │
                  │ Engine             │
                  └────────────────────┘

                             │
                             ▼

              ┌─────────────────────────────┐
              │ Google Photos Integration   │
              │ OAuth 2.0 + Picker API      │
              └─────────────────────────────┘
```

## Setup

### Clone

git clone https://github.com/drishya22/photo-management-platform.git

### Create Environment

python -m venv venv

### Install

pip install -r requirements.txt

### Run Backend

uvicorn main:app --reload

### Run Frontend

streamlit run frontend/app.py

---
# Google Photos Integration

This project integrates with the **Google Photos Picker API** using **OAuth 2.0 Authentication**. Users can securely connect their Google Photos account, select photos through the Google Photos Picker interface, and retrieve metadata of the selected images.

---

## Setup

### 1. Create a Google Cloud Project

1. Go to the Google Cloud Console.
2. Create a new project.
3. Enable the **Google Photos Picker API**.

---

### 2. Configure OAuth Credentials

1. Navigate to **Google Auth Platform → Clients**.
2. Create an **OAuth Client ID**.
3. Select **Web Application**.
4. Add the following Authorized Redirect URI:

```text
http://localhost:8000/auth/callback
```

5. Download the OAuth credentials JSON file.

---

### 3. Add Credentials

Place the downloaded JSON file inside:

```text
secrets/client_secret.json
```

**Note:** This file is not included in the repository and must be provided by the user.

---

### 4. Configure Test Users

Since the application is in testing mode:

1. Open **Google Auth Platform → Audience**
2. Add your Google account as a **Test User**
3. Save the changes

---

## Authentication Flow

```text
User
  │
  ▼
Google OAuth 2.0 Authentication
  │
  ▼
Access Token Generation
  │
  ▼
Google Photos Picker Session Creation
  │
  ▼
User Selects Photos
  │
  ▼
Retrieve Selected Media Items
```
## Google Photos Features

- OAuth 2.0 Authentication
- Google Photos Picker API Integration
- Secure Photo Selection
- Retrieval of Selected Media Metadata
- Session-based Access Control
- Support for Importing Photos from Google Photos

---

## API Endpoints

### Connect Google Photos

```http
GET /google-photos/connect
```

Redirects the user to Google's OAuth authentication page.

---

### Authentication Callback

```http
GET /auth/callback
```

Handles OAuth authentication and stores the access token.

---

### Check Connection Status

```http
GET /google-photos/status
```

Returns the current Google Photos connection status.

---

### Create Picker Session

```http
GET /google-photos/create-session
```

Creates a Google Photos Picker session and returns:

- Session ID
- Picker URL
- Polling Configuration

---

### Retrieve Selected Media Items

```http
GET /google-photos/media-items/{session_id}
```

Returns metadata of photos selected by the user.

Example response:

```json
{
  "mediaItems": [
    {
      "id": "...",
      "createTime": "...",
      "type": "PHOTO",
      "mediaFile": {
        "filename": "IMG_20260711_214728852_HDR.jpg",
        "mimeType": "image/jpeg"
      }
    }
  ]
}
```

---

## Security Notes

- OAuth credentials are excluded from version control.
- Access tokens are generated through Google's OAuth flow.
- Users must provide their own Google Cloud OAuth credentials.
- The `client_secret.json` file should never be committed to GitHub.

---
## Docker

docker compose up --build

---

## API Endpoints

POST /upload

GET /search

GET /images

GET /faces

GET /google-photos/connect

GET /google-photos/status

---

## Tech Stack

#### FastAPI
#### Streamlit
#### ChromaDB
#### CLIP
#### Face Recognition
#### Google Photos Picker API
#### Docker
