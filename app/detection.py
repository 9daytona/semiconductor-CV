
from detector.fasterrcnn_adapter import FasterRCNNDetector
import yaml

with open("config/config.yaml") as f:
    cfg = yaml.safe_load(f)

model = FasterRCNNDetector(
    num_classes=cfg["model"]["num_classes"],
    checkpoint_path=cfg["model"]["checkpoint"],
    score_threshold=cfg["model"]["score_threshold"],
    device="cuda"
)

def detect_objects(frame):
    results = model.predict(frame)

    return results