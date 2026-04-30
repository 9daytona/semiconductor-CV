# semiconductor-CV
AI/ML Camera vision (CV) for safety and operational compliance in the Semiconductor 


semiconductor-safety-cv/
│
├── app/
│   ├── main.py              # CV pipeline
│   ├── stream.py            # video capture utilities
│   ├── detection.py         # YOLO inference wrapper
│   ├── rules.py             # proximity + safety logic
│   ├── overlay.py           # drawing boxes + alerts
│   └── agent.py             # evaluation agent
│
├── server/
│   └── server.py            # Flask alert server
│
├── models/
│   └── yolov8n.pt           # model weights (or downloaded at runtime)
│
├── config/
│   └── config.yaml          # thresholds, stream URL
│
├── scripts/
│   └── run.sh               # run pipeline
│
├── requirements.txt
├── README.md
└── .devcontainer/
    ├── devcontainer.json
    └── Dockerfile