# Face Preference Analyzer

Face Preference Analyzer is an AI-powered backend system that analyzes a user's face image along with style preferences to determine facial shape, measurements, symmetry, and compatibility score.

This backend is designed to integrate with a React Native mobile application and provides results through a REST API built with FastAPI.

---

## Project Overview

The Face Preference Analyzer uses computer vision and AI techniques to detect facial landmarks and analyze facial structure.

The system performs the following tasks:

- Face detection
- Facial landmark extraction
- Face shape classification
- Facial measurements
- Symmetry analysis
- Compatibility score calculation

---

## Features

- Face detection using MediaPipe Face Mesh
- Extraction of 468 facial landmarks
- Automatic face shape classification
- Accurate facial measurement calculations
- Symmetry score analysis
- Compatibility score calculation (0–100)
- Image processing and landmark visualization
- REST API built with FastAPI
- Swagger UI for API testing
- Error handling for invalid images or missing faces

---

## Tech Stack

### Programming Language
- Python 3.x

### Backend Framework
- FastAPI

### Server
- Uvicorn

### Computer Vision
- MediaPipe Face Mesh

### Image Processing
- OpenCV
- NumPy
- Pillow

### Visualization (Optional)
- Matplotlib

### Containerization (Optional)
- Docker

---

## Project Structure

face_backend/

main.py  
FastAPI application and API endpoints

face_analyzer.py  
Core face analysis logic

requirements.txt  
Project dependencies

Dockerfile  
Docker configuration (optional)

uploads/  
Stores uploaded and processed images

utils/

landmarks.py  
MediaPipe face detection

measurements.py  
Facial distance calculations

classifier.py  
Face shape classification

symmetry.py  
Symmetry score calculation

---

## Installation

Clone the repository:

git clone https://github.com/your-username/face-preference-analyzer.git

Go to project folder:

cd face_backend

---

## Create Virtual Environment

python -m venv venv

Activate environment:

### Windows

venv\Scripts\activate

### Linux / macOS

source venv/bin/activate

---

## Install Dependencies

pip install -r requirements.txt

Or install manually:

pip install fastapi uvicorn opencv-python mediapipe numpy pillow matplotlib python-multipart

---

## Running the Server

Start the FastAPI server:

uvicorn main:app --reload

Server will run at:

http://127.0.0.1:8000

---

## API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

---

## API Endpoint

POST /analyze-face

### Request Parameters

file: face image (jpg/png)

preferences: JSON

Example:

{"styleType":"modern","hairLength":"medium","maintenance":"high"}

---

## Example Response

{
  "faceShape": "oval",
  "faceRatio": 1.45,
  "confidence": 0.92,
  "symmetryScore": 87,
  "compatibilityScore": 91,
  "measurements": {},
  "original_image_path": "/uploads/original_123.jpg",
  "processed_image_path": "/uploads/processed_123.jpg"
}

---

## Deployment

The backend can be deployed using:

- Render
- Railway
- Docker

---

## Results

After processing the image, the system provides:

- Detected face shape
- Facial measurements
- Symmetry score
- Compatibility score

Processed images also contain visualized facial landmarks.

---

## Contributing

Pull requests are welcome.

For major changes, please open an issue first to discuss what you would like to change.

---


## Author

Ammar Bin Yasir  
AI Backend Developer