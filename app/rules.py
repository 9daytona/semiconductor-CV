import numpy as np

DIST_THRESHOLD = 150 

def compute_distance(a, b):
    ax, ay = (a[0]+a[2])//2, (a[1]+a[3])//2
    bx, by = (b[0]+b[2])//2, (b[1]+b[3])//2
    return np.sqrt((ax-bx)**2 + (ay-by)**2)

def evaluate_safety(tracks):
    alerts = [] 
    if not tracks:
        return []

    persons = [t for t in tracks if t["class"] == "person"]
    vehicles = [t for t in tracks if t["class"] in ["car","truck"]]
    
    for p in persons:
        for v in vehicles:
            dist = compute_distance(p["bbox"], v["bbox"])
            if dist < DIST_THRESHOLD:
                alerts.append({"type": "proximity",
                               "distance": dist, 
                               "person": p, 
                               "vehicle": v
                               })
    
    return alerts