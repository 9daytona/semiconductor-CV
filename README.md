# semiconductor-CV
AI/ML Camera vision (CV) for safety and operational compliance in the Semiconductor 


semiconductor-safety-cv/
│
├── app/
│   ├── main.py              # CV pipeline
│   ├── stream.py            # video capture utilities
│   ├── detection.py         # YOLO inference wrapper
│   ├── rules.py             # proximity + safety logic
│   ├── yolov8n.pt           # model weights (or downloaded at runtime)
│   └── overlay.py           # drawing boxes + alerts
│
├── server/
│   └── server.py            # Flask alert server
│
│
├── config/
│   └── config.yaml          # thresholds, stream URL
│
│
├── yolov8n.pt           # model weights (or downloaded at runtime)
├── requirements.txt
└── README.md