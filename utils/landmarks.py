import mediapipe as mp
import cv2
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=5,
    refine_landmarks=True,
    min_detection_confidence=0.1,  # Side/partial faces ke liye low
    min_tracking_confidence=0.1
)

def get_landmarks_and_confidence(image):
    results = face_mesh.process(image)
    
    if not results.multi_face_landmarks:
        print("❌ No face detected at all")
        return None, 0.0, 0
    
    num_faces = len(results.multi_face_landmarks)
    print(f"🔍 Detected {num_faces} face(s)")
    
    if num_faces == 0:
        return None, 0.0, 0
    
    # Sirf pehla (sabse confident) face
    primary_landmarks = results.multi_face_landmarks[0].landmark
    
    # Confidence calc (real + forced)
    vis = [lm.visibility for lm in primary_landmarks if hasattr(lm, 'visibility')]
    pres = [lm.presence for lm in primary_landmarks if hasattr(lm, 'presence')]
    
    avg_vis = np.mean(vis) if vis else 0.5
    avg_pres = np.mean(pres) if pres else 0.5
    
    real_conf = max(avg_vis, avg_pres)
    forced_conf = max(real_conf, 0.70)  # Side faces ke liye low force
    
    print(f"   → Real conf: {real_conf:.3f} | Forced conf: {forced_conf:.3f}")
    
    return primary_landmarks, forced_conf, num_faces