import base64
import cv2
import numpy as np

def decode_base64_image(data_url):
    header, encoded = data_url.split(",", 1)
    data = base64.b64decode(encoded)
    np_arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img
