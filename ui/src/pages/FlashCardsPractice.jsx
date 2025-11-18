import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import sign1 from "../assets/sign1.png";
import sign2 from "../assets/sign2.png";
import sign3 from "../assets/sign3.png";

{/* Fetch API ở đây */}
const flashcards = [
  { id: 1, image: sign1, text: "Hello (Xin chào)" },
  { id: 2, image: sign2, text: "Thank you (Cảm ơn)" },
  { id: 3, image: sign3, text: "Goodbye (Tạm biệt)" },
];

const FlashCardsPractice = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const navigate = useNavigate();

  const handleNext = () => {
    setFlipped(false);
    setCurrentIndex((prev) => (prev + 1) % flashcards.length);
  };

  const handlePrev = () => {
    setFlipped(false);
    setCurrentIndex((prev) =>
      prev === 0 ? flashcards.length - 1 : prev - 1
    );
  };

  const currentCard = flashcards[currentIndex];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4 py-10">
      <h2 className="text-2xl font-semibold mb-8 text-gray-800">
        Flash Card {currentIndex + 1}/{flashcards.length}
      </h2>

      {/* Flash card container */}
      <div
        className="relative w-[280px] h-[360px] perspective-1000 cursor-pointer"
        onClick={() => setFlipped(!flipped)}
      >
        <motion.div
          className="absolute w-full h-full rounded-2xl shadow-xl transition-transform duration-500 transform-style-preserve-3d"
          animate={{ rotateY: flipped ? 180 : 0 }}
        >
          {/* Mặt trước */}
          <div className="absolute inset-0 bg-white rounded-2xl flex items-center justify-center p-6 backface-hidden">
            <img
              src={currentCard.image}
              alt="sign"
              className="object-contain max-h-[300px]"
            />
          </div>

          {/* Mặt sau */}
          <div
            className="absolute inset-0 bg-white rounded-2xl flex items-center justify-center text-xl font-medium text-gray-800 text-center px-6 rotateY-180 backface-hidden"
            style={{
              transform: "rotateY(180deg)",
            }}
          >
            {currentCard.text}
          </div>
        </motion.div>
      </div>

      {/* Nút chuyển */}
      <div className="flex gap-6 mt-10">
        <button
          onClick={handlePrev}
          className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold px-6 py-2 rounded-lg transition-all"
        >
          ← Back
        </button>
        <button
          onClick={handleNext}
          className="bg-[#69a79c] hover:bg-[#5e9b91] text-white font-semibold px-6 py-2 rounded-lg transition-all"
        >
          Next →
        </button>
      </div>

      {/* Quay lại */}
      <button
        onClick={() => navigate(-1)}
        className="mt-6 text-gray-500 hover:text-gray-700"
      >
        ⬅ Quay lại
      </button>
    </div>
  );
};

export default FlashCardsPractice;
