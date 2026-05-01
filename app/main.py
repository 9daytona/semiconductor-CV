import cv2
from stream import get_frame
from detection import detect_objects
from rules import evaluate_safety
from overlay import draw_overlay

while True:
    frame = get_frame()
    # preprocessing at ingestion
    # frame = cv2.resize(frame, (640, 480))   
    # frame = cv2.GaussianBlur(frame, (5, 5), 0)
    if frame is None:
        continue

    detections = detect_objects(frame)
    print("DETECTIONS:", detections)
    tracks = detections # temporary fallback
    alerts = evaluate_safety(detections)

    output = draw_overlay(frame, detections, alerts)    #Bypassing tracking temporarily

    cv2.imshow("Safety Monitor", output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows


print("TRACKS:", tracks)

    