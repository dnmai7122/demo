import base64
import cv2
import numpy as np
import mediapipe as mp

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# 6 điểm tay / vai giống demo
POSE_LANDMARKS = [
    mp_holistic.PoseLandmark.LEFT_SHOULDER,
    mp_holistic.PoseLandmark.LEFT_ELBOW,
    mp_holistic.PoseLandmark.LEFT_WRIST,
    mp_holistic.PoseLandmark.RIGHT_SHOULDER,
    mp_holistic.PoseLandmark.RIGHT_ELBOW,
    mp_holistic.PoseLandmark.RIGHT_WRIST,
]


def decode_base64_to_rgb(b64_string: str):
    """Giải mã base64 → ảnh RGB (numpy array)"""
    img_bytes = base64.b64decode(b64_string)
    nparr = np.frombuffer(img_bytes, np.uint8)
    bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb


def extract_frame_keypoints(results, prev_arm, prev_left, prev_right, alpha=0.5):
    """
    Trích xuất keypoints từ pose (arm) và hands - GIỐNG HỆT DEMO:
    arm: 6 điểm × 3
    left hand: 21 × 3
    right hand: 21 × 3
    =>  (6 + 21 + 21) * 3 = 144 features
    """
    # --- Arm (6 landmarks) ---
    arm_points = np.zeros((6, 3))
    if results.pose_landmarks:
        pose = results.pose_landmarks.landmark
        for i, lm_idx in enumerate(POSE_LANDMARKS):
            lm = pose[lm_idx.value]
            arm_points[i] = [lm.x, lm.y, lm.z]
        if prev_arm is not None:
            arm_points = alpha * arm_points + (1 - alpha) * prev_arm
        prev_arm = arm_points
    elif prev_arm is not None:
        arm_points = prev_arm

    # --- Hands (21 landmarks × 2) ---
    def get_hand_landmarks(hand_lms, prev):
        if hand_lms:
            arr = np.array([[lm.x, lm.y, lm.z] for lm in hand_lms.landmark])
            if prev is not None:
                arr = alpha * arr + (1 - alpha) * prev
            return arr
        elif prev is not None:
            return prev
        else:
            return np.zeros((21, 3))

    left = get_hand_landmarks(results.left_hand_landmarks, prev_left)
    right = get_hand_landmarks(results.right_hand_landmarks, prev_right)
    prev_left, prev_right = left, right

    # Concatenate: arm (6×3) + left hand (21×3) + right hand (21×3) = 144 features
    frame_kp = np.concatenate([arm_points, left, right]).flatten()
    return frame_kp, prev_arm, prev_left, prev_right