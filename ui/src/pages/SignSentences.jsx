import React from "react";
import { useNavigate } from "react-router-dom";

const SignSentences = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-green-50 flex flex-col items-center justify-center text-center px-6">
      <h1 className="text-3xl font-bold text-green-600 mb-4">
        Sign Sentences
      </h1>
      <p className="text-gray-600 mb-8 max-w-md">
        Luyện tập ký hiệu theo câu! Giúp bạn nắm vững ngữ pháp 
        và diễn đạt trôi chảy trong ngôn ngữ ký hiệu.
      </p>

      <button
        onClick={() => navigate(-1)}
        className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-medium transition"
      >
        ⬅ Quay lại
      </button>
    </div>
  );
};

export default SignSentences;
