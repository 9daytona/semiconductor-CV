import cv2
from stream import get_frame
from detection import detect_objects
from rules import evaluate_safety
from overlay import Overlay


overlay = Overlay(class_names={
    0: "background",
    1: "person",
    2: "gloves",
    3: "mask",
    4: "wafer"
})

while True:
    frame = get_frame()
    if frame is None:
        continue
    # frame = cv2.resize(frame, (640, 480))  # Optional preprocessing
    # frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Faster R-CNN detection
    results = detect_objects(frame)

    if not results:
        continue

    results = results[0] 

    # Rules engine
    alerts = evaluate_safety(results)


    # Overlay rendering 
    frame = overlay.draw_detections(frame, results)
    frame = overlay.draw_alerts(frame, alerts)

    # Display
    cv2.imshow("Safety Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

    