from ultralytics import YOLO

_model=YOLO("yolov8n.pt")



# Add this to detect.py, replacing RELEVANT_CLASSES

SHAPE_CATEGORY_MAP = {
    # Cylindrical
    "bottle": "cylindrical",
    "vase": "cylindrical",
    "cup": "cylindrical",

    # Box-like
    "book": "box",
    "laptop": "box",
    "cell phone": "box",
    "keyboard": "box",

    # Spherical
    "sports ball": "spherical",
    "apple": "spherical",
    "orange": "spherical",

    # Irregular
    "banana": "irregular",
    "remote": "irregular",
    "scissors": "irregular",
    "toothbrush": "irregular",
    "bowl": "irregular",
}

RELEVANT_CLASSES = set(SHAPE_CATEGORY_MAP.keys())

def detect_object(image_path, confidence_threshold=0.08, exclude_bbox=None):
    """
    exclude_bbox: optional (x1, y1, x2, y2) region to ignore detections
    within (e.g. the marker-display device's own bounding box), so the
    marker's screen/device isn't mistaken for the target object.
    """
    results = _model(image_path, verbose=False)[0]

    best_detection = None
    best_confidence = 0

    for box in results.boxes:
        class_id = int(box.cls[0])
        class_name = _model.names[class_id]
        confidence = float(box.conf[0])

        if class_name not in RELEVANT_CLASSES or confidence < confidence_threshold:
            continue

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        if exclude_bbox is not None:
            ex1, ey1, ex2, ey2 = exclude_bbox
            # Skip if this detection's center falls inside the excluded region
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            if ex1 <= cx <= ex2 and ey1 <= cy <= ey2:
                continue

        if confidence > best_confidence:
            best_confidence = confidence
            best_detection = {
                "class_name": class_name,
                "shape_category": SHAPE_CATEGORY_MAP[class_name],
                "confidence": confidence,
                "bbox": (x1, y1, x2, y2)
            }

    return best_detection