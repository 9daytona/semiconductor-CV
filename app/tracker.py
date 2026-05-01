import supervision as sv

tracker = sv.ByteTrack()

def track_objects(detections):
    # tracker format (converted from detections)
    #  required elaboration HERE

    # for simplicity, assign IDs manually and skip library? 
    return tracker.update(detections)