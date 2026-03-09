def classify(measurements):
    required_keys = ["width", "height", "jaw_width", "cheek_width", "forehead_width", "chin_width"]
    if not all(key in measurements for key in required_keys) or any(measurements[key] == 0 for key in required_keys):
        print("Classifier: Missing or zero values → unknown")
        return "unknown"
    
    ratio = measurements["height"] / measurements["width"]
    jaw_cheek_ratio = measurements["jaw_width"] / measurements["cheek_width"]
    forehead_ratio = measurements["forehead_width"] / measurements["width"]
    chin_forehead_ratio = measurements["chin_width"] / measurements["forehead_width"]
    
    print(f"Debug Ratios → h/w={ratio:.3f} | jaw/cheek={jaw_cheek_ratio:.3f} | forehead/w={forehead_ratio:.3f} | chin/forehead={chin_forehead_ratio:.3f}")

    # Softened logic with buffers (high-standard approach)
    if ratio > 1.60:
        return "oblong"
    elif ratio > 1.50 and forehead_ratio > 0.78:
        return "rectangle"
    elif 1.25 <= ratio <= 1.50 and jaw_cheek_ratio < 1.12 and chin_forehead_ratio > 0.82:
        return "oval"
    elif ratio < 1.12 and jaw_cheek_ratio > 0.95:
        return "round"
    elif ratio < 1.32 and jaw_cheek_ratio > 1.08:
        return "square"
    elif forehead_ratio > 0.98 and chin_forehead_ratio < 0.72:
        return "heart"
    elif measurements["cheek_width"] > measurements["forehead_width"] and chin_forehead_ratio < 0.82:
        return "diamond"
    elif measurements["jaw_width"] > measurements["forehead_width"] and chin_forehead_ratio > 0.88:
        return "triangle"
    else:
        return "unknown"