from ultralytics import YOLO

model = YOLO("yolov8n.pt")
results = model("data/sample_images/card_bottle.jpeg", conf=0.05, verbose=False)[0]

print(f"Total detections at conf=0.05: {len(results.boxes)}")
for box in results.boxes:
    class_id = int(box.cls[0])
    print(f"{model.names[class_id]}: {float(box.conf[0]):.3f}")