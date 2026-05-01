import cv2
def draw_overlay(frame, detections, alerts):
    for d in detections:
        x1,y1,x2,y2 = d["bbox"]
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(frame, d["class"],
                    (x1,y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0,255, 0),
                    2)

        if alerts:
            cv2.putText(frame, 
                        "ALERT!!!!!",
                        (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0,0,255), 3)
            
    return frame