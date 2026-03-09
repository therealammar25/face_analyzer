from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
import json
import os
import uuid
import mediapipe as mp

from utils.landmarks import get_landmarks_and_confidence
from utils.measurements import calculate
from utils.classifier import classify
from utils.symmetry import calculate_symmetry
from face_analyzer import calculate_score

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
os.makedirs("uploads", exist_ok=True)

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

@app.post("/analyze-face")
async def analyze_face(
    image: UploadFile = File(...),
    preferences: str = Form(...)
):
    original_filename = f"{uuid.uuid4()}_{image.filename}"
    original_path = os.path.join("uploads", original_filename)
    
    try:
        contents = await image.read()
        with open(original_path, "wb") as f:
            f.write(contents)
        print(f"✅ Original saved: {original_path}")

        # Preferences
        prefs = json.loads(preferences)
        valid_styles = ["modern", "classic", "casual"]
        valid_hairs = ["very_short", "short", "medium", "shoulder", "long", "very_long"]
        valid_maint = ["low", "medium", "high"]
        if prefs.get("styleType") not in valid_styles or prefs.get("hairLength") not in valid_hairs or prefs.get("maintenance") not in valid_maint:
            raise ValueError("Invalid preferences")

        # Load image
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("Invalid image format")

        # Format handling
        if len(img.shape) == 2:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # ====================== IMPROVED DETECTION FOR SIDE/PARTIAL FACES ======================
        # Pehle normal try
        landmarks, confidence, num_faces = get_landmarks_and_confidence(img_rgb)
        print(f"🔍 Faces detected: {num_faces} | Confidence: {confidence:.3f}")

        # Agar fail ho to soft crop + retry
        if landmarks is None or confidence < 0.50:
            print("⚠️ Low confidence on full image → trying cropped version")
            h, w = img_rgb.shape[:2]
            crop_img = img_rgb[int(h*0.05):int(h*0.95), int(w*0.05):int(w*0.95)]  # Soft crop (5% margin)
            landmarks, confidence, num_faces = get_landmarks_and_confidence(crop_img)
            print(f"   Cropped retry → Faces: {num_faces} | Conf: {confidence:.3f}")
            if landmarks:
                img_rgb = crop_img  # Use cropped for drawing

        # Multiple faces check
        if num_faces > 1:
            raise ValueError("More than 1 face detected. Please upload a photo with ONLY ONE person.")

        # Final check
        if landmarks is None:
            raise ValueError("No face detected or face is too partial/side-cut. Please upload a clear, frontal photo with full face visible.")

        print(f"✅ Face detected successfully! Confidence: {confidence:.2f}")

       

        # ====================== Analysis ======================
        measurements = calculate(landmarks)
        face_shape = classify(measurements)
        symmetry = calculate_symmetry(landmarks)
        score = calculate_score(face_shape, measurements, prefs, symmetry)
        ratio = measurements["height"] / measurements["width"]

        # Draw green mesh
        img_draw = img_rgb.copy()
        landmark_list = type('FakeLandmarkList', (), {'landmark': landmarks})()
        mp_drawing.draw_landmarks(
            image=img_draw,
            landmark_list=landmark_list,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)
        )

        processed_filename = f"processed_{original_filename}.png"
        processed_path = os.path.join("uploads", processed_filename)
        cv2.imwrite(processed_path, cv2.cvtColor(img_draw, cv2.COLOR_RGB2BGR))

        return {
            "faceShape": face_shape,
            "faceRatio": round(ratio, 3),
            "confidence": round(confidence, 2),
            "symmetryScore": symmetry,
            "compatibilityScore": score,
            "measurements": {k: round(v, 4) for k, v in measurements.items()},
            "original_image_url": f"/uploads/{original_filename}",
            "processed_image_url": f"/uploads/{processed_filename}"
        }

    except ValueError as ve:
        print(f"ValueError: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")