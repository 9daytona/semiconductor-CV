import torch
import torchvision
import numpy as np
import cv2
import os

from torchvision.models.feature_extraction import create_feature_extractor
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.transforms import functional as F

class FasterRCNNDetector:
    def __init__(self, num_classes, checkpoint_path=None, device="cuda", score_threshold=0.5):

        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.score_threshold = score_threshold

        
        # 1. RegNetX-040 backbone 
        backbone_model = torchvision.models.regnet_x_400mf(weights="DEFAULT")

        backbone = create_feature_extractor(
            backbone_model,
            return_nodes={"trunk_output": "0"}
        )

        backbone.out_channels = 400

        
        # 2. Custom Anchor Generator (CRITICAL)
        anchor_generator = AnchorGenerator(
            sizes=((16, 32, 64, 128, 256),),
            aspect_ratios=((0.5, 1.0, 2.0),)
        )

        
        # 3. Build Faster R-CNN
        self.model = FasterRCNN(
            backbone=backbone,
            num_classes=num_classes,
            rpn_anchor_generator=anchor_generator
        )

        
        # 4. Load weights (safe)
        if checkpoint_path and os.path.exists(checkpoint_path):
            print(f"[INFO] Loading checkpoint: {checkpoint_path}")
            state_dict = torch.load(checkpoint_path, map_location=self.device)
            self.model.load_state_dict(state_dict, strict=False)
        else:
            print(f"[WARN] Checkpoint not found. Using pretrained backbone only.")

        self.model.to(self.device)
        self.model.eval()

    
    # Preprocess
    def _preprocess(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # resize for performance (CRITICAL)
        frame = cv2.resize(frame, (640, 384))

        return F.to_tensor(frame).to(self.device)

    
    # Inference
    def predict(self, frame):
        tensor = self._preprocess(frame)

        with torch.no_grad():
            outputs = self.model([tensor])[0]

        boxes = outputs["boxes"].detach().cpu().numpy()
        scores = outputs["scores"].detach().cpu().numpy()
        labels = outputs["labels"].detach().cpu().numpy()

        keep = scores >= self.score_threshold

        return [{
            "boxes": boxes[keep],
            "scores": scores[keep],
            "classes": labels[keep]
        }]
    