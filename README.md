# File Storage Service

This service handles the upload and retrieval of images, videos and documents used in other RHP frontend services.

Functional Requirements:

1. POST - Upload FILE.
2. PATCH - Change File
3. GET - RETRIEVE FILE

Non Functional Requirements:

1. API Requests To Each Endpoint Must Be Authenticated.
2. Fast Response Time.

---
# How to use the Api

This is a general file storage api system built with Python FastAPI, Cloudinary and Sqlite db.

## Requirements
- Python 3.8 >=
- Cloudinary Account

## Installations
- pip install -r requirements.txt

## Running the application
- uvicorn main:app --reload

## Endpoints
- /upload/ - POST :- file
- /files/ - GET
- /files/{file_id} - GET
