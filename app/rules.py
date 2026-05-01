import numpy as np

DIST_THRESHOLD = 150 

# Class mapping
CLASS_MAP = {
    0: "background",
    1: "person",
    2: "gloves",
    3: "mask",
    4: "wafer",
    5: "car",
    6: "truck"
}

def compute_distance(box_a, box_b):
    ax, ay = (box_a[0] + box_a[2]) // 2, (box_a[1] + box_a[3]) // 2
    bx, by = (box_b[0] + box_b[2]) // 2, (box_b[1] + box_b[3]) // 2

    return np.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

def evaluate_safety(results):
    """
    results format:
    {
        "boxes": [N,4],
        "scores": [N],
        "classes": [N]
    }
    """

    alerts = []

    if results is None or len(results["boxes"]) == 0:
        return alerts


    # Convert to internal objects
    objects = []

    for box, cls_id, score in zip(
        results["boxes"],
        results["classes"],
        results["scores"]
    ):
        label = CLASS_MAP.get(int(cls_id), str(cls_id))

        objects.append({
            "bbox": box,
            "class": label,
            "score": float(score)
        })


    # Split classes
    persons = [o for o in objects if o["class"] == "person"]
    vehicles = [o for o in objects if o["class"] in ["car", "truck"]]


    # Distance rule
    for p in persons:
        for v in vehicles:
            dist = compute_distance(p["bbox"], v["bbox"])

            if dist < DIST_THRESHOLD:
                alerts.append({
                    "message": f"Person too close to vehicle ({int(dist)}px)",
                    "severity": "high",
                    "distance": float(dist),
                    "person": p,
                    "vehicle": v
                })

    return alerts
    
