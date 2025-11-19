from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import torch
import torch.nn.functional as F

from app.model_handler import load_model
from app.utils import (
    mp_holistic,
    decode_base64_to_rgb,
    extract_frame_keypoints,
)

# ====== CONFIG KHỚP DEMO ======
WINDOW_SIZE = 100          # số frame dùng khi train (model chịu được T khác nhau)
INPUT_FEATURES = 144       # 6 arm + 21 LH + 21 RH (mỗi cái 3D)
HIDDEN_DIM = 128
MODEL_PATH = "model/lstm_attn.pth"
SMOOTHING_ALPHA = 0.5

# 5 classes giống file demo
LABELS = [
    "bản_thân",
    "cha_mẹ",
    "nhà",
    "tên",
    "ông",
]

LABELS_DISPLAY = [
    "ban than",
    "cha me",
    "nha",
    "ten",
    "ong",
]

# ====== LOAD MODEL ======
device = "cuda" if torch.cuda.is_available() else "cpu"
model = load_model(
    MODEL_PATH,
    device=device,
    input_size=INPUT_FEATURES,
    hidden_size=HIDDEN_DIM,
    num_layers=2,
    num_classes=len(LABELS),
)

# ====== FASTAPI + CORS ======
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Cho phép mọi origin (React: localhost:5173, ngrok,...)
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class FramesPayload(BaseModel):
    data: list[str]  # list base64 (đã strip "data:image/..,")


@app.get("/")
def health_check():
    return {"message": "Backend is running!"}


@app.post("/predict")
async def predict(payload: FramesPayload):
    frames_b64 = payload.data
    if not frames_b64:
        return {"prediction": "No frames", "confidence": 0.0}

    sequence = []
    prev_arm = prev_left = prev_right = None

    # Dùng Holistic giống demo
    with mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.7,
        enable_segmentation=False,
        refine_face_landmarks=False,
    ) as holistic:
        for b64 in frames_b64:
            rgb = decode_base64_to_rgb(b64)
            results = holistic.process(rgb)
            frame_kp, prev_arm, prev_left, prev_right = extract_frame_keypoints(
                results, prev_arm, prev_left, prev_right, alpha=SMOOTHING_ALPHA
            )
            sequence.append(frame_kp)

    if len(sequence) == 0:
        return {"prediction": "No landmarks", "confidence": 0.0}

    seq_np = np.array(sequence, dtype=np.float32)  # (T, 144)
    if seq_np.ndim != 2 or seq_np.shape[1] != INPUT_FEATURES:
        return {"prediction": "Bad feature shape", "confidence": 0.0}

    tensor_inp = torch.from_numpy(seq_np).unsqueeze(0).to(device)  # (1, T, 144)

    with torch.no_grad():
        logits = model(tensor_inp)
        probs = F.softmax(logits, dim=1)[0]
        conf, idx = torch.max(probs, dim=0)

    label_idx = idx.item()
    label_display = LABELS_DISPLAY[label_idx] if 0 <= label_idx < len(LABELS_DISPLAY) else LABELS[label_idx]

    return {
        "prediction": label_display,          # React sẽ show string này
        "confidence": float(conf.item()),     # 0.0–1.0
    }
