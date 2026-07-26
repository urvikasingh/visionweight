from torch.compiler import nested_compile_region
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

def detect_object(image_path, confidence_threshold=0.35):
    """
    Runs YOLOv8 on the image and returns the highest-confidence
    detection that matches our relevant household object classes.

    Returns a dict: {class_name, shape_category, confidence, bbox (x1,y1,x2,y2)}
    or None if nothing relevant was detected.
    """
    results = _model(image_path, verbose=False)[0]

    best_detection = None
    best_confidence = 0

    for box in results.boxes:
        class_id = int(box.cls[0])
        class_name = _model.names[class_id]
        confidence = float(box.conf[0])

        if class_name in RELEVANT_CLASSES and confidence >= confidence_threshold:
            if confidence > best_confidence:
                best_confidence = confidence
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                best_detection = {
                    "class_name": class_name,
                    "shape_category": SHAPE_CATEGORY_MAP[class_name],
                    "confidence": confidence,
                    "bbox": (x1, y1, x2, y2)
                }

    return best_detection