from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from .model_handler import predict_from_frame
from .utils import decode_base64_image

app = FastAPI()

# Cho phép frontend React localhost truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    image_base64: str

@app.post("/predict")
async def predict_image(request: PredictRequest):
    try:
        frame = decode_base64_image(request.image_base64)
        result = predict_from_frame(frame)  # gọi model
        return result
    except Exception as e:
        return {"error": str(e)}
