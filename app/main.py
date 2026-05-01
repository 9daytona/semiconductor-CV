import cv2
import numpy as np
from ultralytics import YOLO
import time

#  CONFIG 
PHONE_STREAM_URL = "http://172.20.10.4:8080/video"  # change this
DIST_THRESHOLD = 150  # pixel distance threshold for alert
MODEL_PATH = "yolov8n.pt"  # small model for speed

#  LOAD MODEL 
model = YOLO(MODEL_PATH)

#  VIDEO STREAM 
cap = cv2.VideoCapture(PHONE_STREAM_URL)

if not cap.isOpened():
    print("Error: Cannot open stream")
    exit()

def compute_distance(box1, box2):
    x1, y1, x2, y2 = box1
    x1b, y1b, x2b, y2b = box2

    cx1, cy1 = (x1+x2)//2, (y1+y2)//2
    cx2, cy2 = (x1b+x2b)//2, (y1b+y2b)//2

    return np.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize for speed
    frame = cv2.resize(frame, (640, 480))

    #  INFERENCE 
    results = model(frame)[0]

    persons = []
    vehicles = []

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        label = model.names[cls]

        # Simple mapping
        if label == "person":
            persons.append((x1, y1, x2, y2))
        elif label in ["car", "truck", "bus"]:
            vehicles.append((x1, y1, x2, y2))

        # Draw box
        color = (0, 255, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    #  PROXIMITY ALERT 
    alert_triggered = False

    for p in persons:
        for v in vehicles:
            dist = compute_distance(p, v)
            if dist < DIST_THRESHOLD:
                alert_triggered = True

                # Draw alert line
                px, py = (p[0]+p[2])//2, (p[1]+p[3])//2
                vx, vy = (v[0]+v[2])//2, (v[1]+v[3])//2

                cv2.line(frame, (px, py), (vx, vy), (0, 0, 255), 2)

                cv2.putText(frame, f"ALERT! Dist={int(dist)}",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)

    #  DISPLAY 
    cv2.imshow("Safety Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()