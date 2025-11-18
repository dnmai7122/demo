import cv2
import numpy as np
import mediapipe as mp
import torch
from pathlib import Path

# LSTM model class placeholder 
class LSTMModel(torch.nn.Module):
    def __init__(self, input_size=63, hidden_size=128, output_size=10):  # thay output_size nếu cần
        super().__init__()
        self.lstm = torch.nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = torch.nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]  
        out = self.fc(out)
        return out

# Load model + mediapipe 
MODEL_PATH = Path(__file__).parent.parent / "model/lstm_attn.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = LSTMModel()
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# Hàm extract keypoints
def extract_frame_keypoints(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    keypoints = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                keypoints.extend([lm.x, lm.y, lm.z])
    # nếu không có hand, trả về vector zeros
    if len(keypoints) == 0:
        keypoints = [0] * 63  
    return keypoints

# predict từ frame numpy
def predict_from_frame(frame):
    keypoints = extract_frame_keypoints(frame)
    # tạo batch 1 và sequence length 1
    x = torch.tensor(keypoints, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(x)
        probs = torch.nn.functional.softmax(logits, dim=1)
        conf, idx = torch.max(probs, dim=1)
    # label placeholder, thay bằng nhãn thật
    label_map = {0: "Gesture1", 1: "Gesture2", 2: "Gesture3", 3:"Gesture4", 4:"Gesture5",
                 5:"Gesture6", 6:"Gesture7", 7:"Gesture8", 8:"Gesture9", 9:"Gesture10"}
    label = label_map.get(int(idx.item()), "Unknown")
    return {"label": label, "confidence": float(conf.item())}
