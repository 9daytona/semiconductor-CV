import cv2


class Overlay:
    def __init__(self, class_names=None):
        """
        class_names: dict {id: name}
        """
        self.class_names = class_names or {}

    def _label(self, cls_id):
        return self.class_names.get(int(cls_id), str(cls_id))


    # MAIN Faster R-CNN / YOLO-compatible renderer
    def draw_detections(self, frame, results):
        """
        results format:
        {
            "boxes": [N,4],
            "scores": [N],
            "classes": [N]
        }
        """

        if results is None:
            return frame

        for box, score, cls in zip(
            results["boxes"],
            results["scores"],
            results["classes"]
        ):
            x1, y1, x2, y2 = map(int, box)

            label = self._label(cls)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{label}:{score:.2f}",
                (x1, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        return frame

    # RULES / ALERT LAYER
    def draw_alerts(self, frame, alerts):
        """
        alerts format:
        [
          {"message": str, "severity": "high|medium|low"}
        ]
        """

        if not alerts:
            return frame

        # Single consolidated alert banner (avoid spam overlay)
        cv2.putText(
            frame,
            "ALERT: COMPLIANCE VIOLATION",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            3
        )

        # Optional detailed alerts
        y = 90
        for a in alerts:
            cv2.putText(
                frame,
                a.get("message", ""),
                (30, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )
            y += 25

        return frame