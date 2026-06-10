from ultralytics import YOLO

# Load model sekali saja
model = YOLO("model/best.pt")

def detect_image(image_path):

    results = model(image_path)

    result_image = results[0].plot()

    detections = []

    for box in results[0].boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        class_name = model.names[class_id]

        detections.append({
            "class": class_name,
            "confidence": confidence
        })

    return result_image, detections