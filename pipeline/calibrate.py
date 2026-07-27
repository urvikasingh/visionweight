import cv2

MARKER_SIZE_MM = 55.0

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
ARUCO_PARAMS = cv2.aruco.DetectorParameters()
DETECTOR = cv2.aruco.ArucoDetector(ARUCO_DICT, ARUCO_PARAMS)


def get_pixels_per_mm(image_path):
    """
    Automatically detects the ArUco marker in the image and computes
    pixels_per_mm from its known real-world size. Also returns the
    marker's own bounding box, so the caller can exclude it from
    object detection (avoids the marker's display device being
    mistaken for the target object).
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = DETECTOR.detectMarkers(gray)

    if ids is None or len(corners) == 0:
        return None

    marker_corners = corners[0][0]

    side_lengths = [
        ((marker_corners[i][0] - marker_corners[(i + 1) % 4][0]) ** 2 +
         (marker_corners[i][1] - marker_corners[(i + 1) % 4][1]) ** 2) ** 0.5
        for i in range(4)
    ]
    avg_side_px = sum(side_lengths) / len(side_lengths)

    pixels_per_mm = avg_side_px / MARKER_SIZE_MM

    xs = [p[0] for p in marker_corners]
    ys = [p[1] for p in marker_corners]
    marker_bbox = (min(xs), min(ys), max(xs), max(ys))

    return {"pixels_per_mm": pixels_per_mm, "marker_id": int(ids[0][0]), "marker_bbox": marker_bbox}