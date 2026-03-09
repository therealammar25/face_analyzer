def calculate_score(face_shape, measurements, preferences, symmetry):
    # Sub-scores (0-100) - Updated for new shapes
    face_shape_score = 80  # Default
    if face_shape == "oval":
        face_shape_score = 90
    elif face_shape == "round":
        face_shape_score = 60
    elif face_shape == "square":
        face_shape_score = 70
    elif face_shape == "rectangle":
        face_shape_score = 75
    elif face_shape == "heart":
        face_shape_score = 85  # Versatile
    elif face_shape == "diamond":
        face_shape_score = 80
    elif face_shape == "oblong":
        face_shape_score = 70
    elif face_shape == "triangle":
        face_shape_score = 65  # More angular
    elif face_shape == "unknown":
        face_shape_score = 50
    
    preference_score = 50
    if preferences["styleType"] == "modern":
        preference_score += 20
    elif preferences["styleType"] == "classic":
        preference_score += 10
    elif preferences["styleType"] == "casual":
        preference_score += 15
    
    # Updated hair lengths with more options and shape-specific logic
    hair = preferences["hairLength"]
    if hair == "very_short":
        preference_score += 15 if face_shape in ["square", "diamond"] else -5  # Good for angular
    elif hair == "short":
        preference_score += 10 if face_shape != "round" else -10
    elif hair == "medium" or hair == "shoulder":  # shoulder as alias for medium-long
        preference_score += 15 if face_shape in ["oval", "heart"] else 5
    elif hair == "long":
        preference_score += 10 if face_shape == "oval" else -5
    elif hair == "very_long":
        preference_score += 5 if face_shape in ["oblong", "triangle"] else -10  # Can elongate
    
    if preferences["maintenance"] == "low":
        preference_score += 10
    elif preferences["maintenance"] == "medium":
        preference_score += 5
    elif preferences["maintenance"] == "high":
        preference_score -= 5 if face_shape == "square" else 0
    
    preference_score = max(0, min(preference_score, 100))
    
    symmetry_score = symmetry * 100  # 0-100
    
    # Spec formula
    compatibility_score = (face_shape_score + preference_score + symmetry_score) / 3
    return round(compatibility_score)