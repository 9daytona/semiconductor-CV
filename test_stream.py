import cv2
URL = "http://172.20.10.4:8080/video"

cap = cv2.VideoCapture(URL)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Stream failed")
        continue
    cv2.imshow("TEST Stream", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
