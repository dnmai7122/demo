// CameraSignPractice.jsx
import React, { useEffect, useRef, useState } from "react";
import AaImg from "../assets/Aa.png";
import BbImg from "../assets/Bb.png";
import JjImg from "../assets/Jj.png";

// DATA
const SIGN_DETAILS = {
  ông: "tay phải khép nhẹ, lòng bàn tay hướng vào trong, chạm nhẹ vào trán.",
  bà: "tay phải khép nhẹ, lòng bàn tay hướng vào trong, chạm nhẹ vào má.",
  cha: "tay phải khum nhẹ, lòng bàn tay hướng vào trong, chạm má phải.",
  mẹ: "tay phải khum nhẹ, lòng bàn tay hướng vào trong, chạm má trái.",
  "bé trai":
    "tay phải tạo chữ U, lòng bàn tay hướng vào trong, chạm nhẹ cằm, gập ngón xuống.",
  "bé gái": "ngón trỏ và cái chạm nhẹ vào tai phải.",
  ăn: "tay phải khum như cầm thìa, đưa từ trước miệng vào.",
  uống: "tay khum như cầm ly, đưa lên miệng và nghiêng nhẹ.",
};

// SIGN LIST
const handSigns = [
  { label: "ông", img: AaImg },
  { label: "bà", img: BbImg },
  { label: "bé trai", img: JjImg },
];

// ĐÁNH GIÁ GIẢ LẬP
function evaluateSign(groundTruth, modelOutput) {
  if (groundTruth === modelOutput) return `Kết luận: Dự đoán chính xác ✔`;

  return `
Kết luận: sai – mô hình dự đoán "${modelOutput}"
Động tác đúng: ${SIGN_DETAILS[groundTruth] || ""}
  `;
}

export default function CameraSignPractice() {
  const [current, setCurrent] = useState(0);
  const [feedback, setFeedback] = useState("");
  const videoRef = useRef(null);

  // CAMERA
  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
      if (videoRef.current) videoRef.current.srcObject = stream;
    });

    return () => {
      if (videoRef.current?.srcObject) {
        videoRef.current.srcObject.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  // GIẢ MODEL
  const fakeModelPredict = () => {
    const keys = Object.keys(SIGN_DETAILS);
    return keys[Math.floor(Math.random() * keys.length)];
  };

  return (
    <div className="w-full min-h-screen bg-gray-100 flex justify-center p-6">

      {/* CARD KHÔNG ÉP CHIỀU CAO */}
      <div className="w-full max-w-[900px] bg-white rounded-2xl shadow-xl p-6 flex flex-col gap-6">

        {/* TITLE */}
        <h1 className="text-3xl font-bold text-center">Camera Sign Practice</h1>

        {/* IMAGE + SKIP */}
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-4">
            <img
              src={handSigns[current].img}
              alt={handSigns[current].label}
              className="w-24 h-24 border-4 border-green-500 rounded-xl"
            />
            <p className="text-2xl font-semibold">{handSigns[current].label}</p>
          </div>

          <button
            onClick={() => {
              setFeedback("");
              setCurrent((c) => (c + 1) % handSigns.length);
            }}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl"
          >
            Skip
          </button>
        </div>

        {/* CAMERA — auto scale theo container */}
        <div className="w-full flex justify-center">
          <video
            ref={videoRef}
            autoPlay
            muted
            playsInline
            className="w-full max-w-[700px] rounded-xl border-4 border-gray-300 object-cover aspect-video"
          />
        </div>

        {/* CHECK BUTTON */}
        <button
          onClick={() => {
            const gt = handSigns[current].label;
            const predicted = fakeModelPredict();
            setFeedback(evaluateSign(gt, predicted));
          }}
          className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl text-lg font-semibold self-center"
        >
          Kiểm tra động tác
        </button>

        {/* FEEDBACK */}
        {feedback && (
          <div className="bg-yellow-50 border border-yellow-300 p-4 rounded-lg whitespace-pre-line text-gray-800 text-lg">
            {feedback}
          </div>
        )}
      </div>
    </div>
  );
}
