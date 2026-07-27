from pipeline.detect import detect_object
from pipeline.volume import estimate_volume

image_path = "data/sample_images/card_bottle.jpeg"

detection = detect_object(image_path)
print("Detection:", detection)

# Measured with ruler:
width_mm = 70
height_mm = 200

if detection:
    volume_result = estimate_volume(detection["shape_category"], width_mm, height_mm)
    print("Volume:", volume_result)
else:
    print("Detection failed")