import math

BOX_DEPTH_RATIO = 0.4
IRREGULAR_DEPTH_RATIO = 0.5
IRREGULAR_FILL_FACTOR = 0.6


def estimate_volume(shape_category, width_mm, height_mm, depth_mm=None):
    """
    Takes manually measured width and height (mm), plus the detected
    shape category, and returns estimated volume.

    depth_mm: optional. If provided (e.g. ruler-measured thickness for
    a box-shaped object), it's used directly instead of the ratio
    assumption - this is more accurate whenever the real depth is known.
    """
    shape = shape_category

    if shape == "cylindrical":
        diameter_mm = min(width_mm, height_mm)
        length_mm = max(width_mm, height_mm)
        radius_mm = diameter_mm / 2
        final_depth_mm = diameter_mm
        volume_mm3 = math.pi * (radius_mm ** 2) * length_mm
        depth_method = "exact (circular cross-section, orientation-independent)"

    elif shape == "spherical":
        radius_mm = width_mm / 2
        final_depth_mm = width_mm
        volume_mm3 = (4 / 3) * math.pi * (radius_mm ** 3)
        depth_method = "exact (circular cross-section)"

    elif shape == "box":
        if depth_mm is not None:
            final_depth_mm = depth_mm
            depth_method = "measured (ruler input)"
        else:
            final_depth_mm = width_mm * BOX_DEPTH_RATIO
            depth_method = f"estimated (ratio={BOX_DEPTH_RATIO})"
        volume_mm3 = width_mm * height_mm * final_depth_mm

    elif shape == "irregular":
        if depth_mm is not None:
            final_depth_mm = depth_mm
            depth_method = "measured (ruler input)"
        else:
            final_depth_mm = width_mm * IRREGULAR_DEPTH_RATIO
            depth_method = f"estimated (ratio={IRREGULAR_DEPTH_RATIO})"
        volume_mm3 = width_mm * height_mm * final_depth_mm * IRREGULAR_FILL_FACTOR

    else:
        raise ValueError(f"Unknown shape_category: '{shape}'")

    return {
        "width_mm": round(width_mm, 1),
        "height_mm": round(height_mm, 1),
        "depth_mm": round(final_depth_mm, 1),
        "volume_mm3": round(volume_mm3, 1),
        "depth_method": depth_method
    }


def estimate_volume_from_pixels(shape_category, bbox, pixels_per_mm, depth_mm=None):
    """
    Same as estimate_volume, but computes width/height automatically
    from the object's pixel bounding box and the marker's pixels_per_mm,
    instead of requiring manual ruler input.
    """
    x1, y1, x2, y2 = bbox
    width_mm = abs(x2 - x1) / pixels_per_mm
    height_mm = abs(y2 - y1) / pixels_per_mm
    return estimate_volume(shape_category, width_mm, height_mm, depth_mm)