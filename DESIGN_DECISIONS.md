# Design Decisions

## Backend
FastAPI was chosen for high performance and simple REST API development.

## Vector Search
ChromaDB was selected because it is lightweight and easy to integrate for local vector search.

## Image Embeddings
CLIP embeddings are used because they support both image and text representations in the same vector space.

## Duplicate Detection
Two-stage approach:

1. SHA-256 hashing for exact duplicates
2. CLIP embedding similarity for near duplicates

## Face Recognition
Face encodings are generated using face_recognition and grouped using cosine similarity.

## Google Photos Integration
Google OAuth 2.0 and Google Photos Picker API are used for secure photo import.

## Frontend
Streamlit was selected for rapid UI development.