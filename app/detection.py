from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_objects(frame):
    results = model(frame)[0]

    detections = []

    for box in results.boxes:
       cls = int(box.cls[0])
       conf = float(box.conf[0])
       x1,y1,x2,y2 = map(int, box.xyxy[0])

       detections.append({
         "bbox":(x1,y1,x2,y2),
         "class": model.names[cls],
         "conf": conf
       })

    return detections