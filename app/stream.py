import cv2
import time

PHONE_STREAM_URL = "http://172.20.10.4:8080/video"

cap = None
fail_count = 0
MAX_FAILS = 10


def connect_stream():
    cap = cv2.VideoCapture(PHONE_STREAM_URL, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap


cap = connect_stream()


def get_frame():
    global cap, fail_count

    if cap is None or not cap.isOpened():
        print("[WARN] Reconnecting stream...")
        cap = connect_stream()
        time.sleep(1)

    # CRITICAL: flush buffer

    for _ in range(5):
        cap.grab()

    ret, frame = cap.read()

    if not ret or frame is None:
        fail_count += 1
        print(f"[WARN] Frame failed ({fail_count})")

        if fail_count > MAX_FAILS:
            print("[ERROR] Restarting stream connection...")
            cap.release()
            time.sleep(2)
            cap = connect_stream()
            fail_count = 0

        return None

    fail_count = 0
    return frame