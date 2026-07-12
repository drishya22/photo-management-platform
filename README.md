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

git clone <repo>

### Create Environment

python -m venv venv

### Install

pip install -r requirements.txt

### Run Backend

uvicorn main:app --reload

### Run Frontend

streamlit run frontend/app.py

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

FastAPI
Streamlit
ChromaDB
CLIP
Face Recognition
Google Photos Picker API
Docker
