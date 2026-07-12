from google_auth_oauthlib.flow import Flow
import requests

CLIENT_SECRET_FILE="secrets/client_secret.json"

SCOPES=[
    "https://www.googleapis.com/auth/photospicker.mediaitems.readonly"
]

def create_flow():
    flow=Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/auth/callback"
    )
    return flow



def create_picker_session(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        "https://photospicker.googleapis.com/v1/sessions",
        headers=headers,
        json={}
    )

    return response.json()

def get_session(token, session_id):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"https://photospicker.googleapis.com/v1/sessions/{session_id}",
        headers=headers
    )

    return response.json()

def list_media_items(token, session_id):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        "https://photospicker.googleapis.com/v1/mediaItems",
        headers=headers,
        params={
            "sessionId": session_id
        }
    )

    return response.json()