import React, { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

/* Dummy data cho chart */
const chartData = [
  { level: "Cấp 1", count: 120 },
  { level: "Cấp 2", count: 180 },
  { level: "Cấp 3", count: 90 },
  { level: "Cấp 4", count: 45 },
  { level: "Nhớ sâu", count: 10 },
];

/* Dummy topics */
const topicsData = [
  { name: "Giao tiếp sơ cấp", createdAt: "2025-10-20" },
  { name: "Giao tiếp nâng cao", createdAt: "2025-09-10" },
  { name: "Báo cáo tài chính", createdAt: "2025-08-15" },
  { name: "Ứng tuyển và Phỏng vấn", createdAt: "2025-10-10" },
  { name: "Công nghệ", createdAt: "2025-07-02" },
  { name: "Du lịch", createdAt: "2025-09-30" },
];

const Practice = () => {
  const navigate = useNavigate();
  const [showIgnoredWords, setShowIgnoredWords] = useState(false);
  const [sortOption, setSortOption] = useState("Mới nhất");
  const [showPracticePopup, setShowPracticePopup] = useState(false);

  const ignoredWords = ["Xin chào", "Cảm ơn", "Tạm biệt"];

  /* Hàm sắp xếp topic */
  const sortedTopics = useMemo(() => {
    const sorted = [...topicsData];
    if (sortOption === "Tên: A-Z") {
      sorted.sort((a, b) =>
        a.name.localeCompare(b.name, "vi", { sensitivity: "base" })
      );
    } else if (sortOption === "Tên: Z-A") {
      sorted.sort((a, b) =>
        b.name.localeCompare(a.name, "vi", { sensitivity: "base" })
      );
    } else if (sortOption === "Mới nhất") {
      sorted.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    } else if (sortOption === "Cũ nhất") {
      sorted.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
    }
    return sorted;
  }, [sortOption]);

  /* Hàm chuyển trang khi chọn phương pháp ôn tập */
  const handleSelectPractice = (type) => {
    setShowPracticePopup(false);
    if (type === "Flash Cards") navigate("/practice/flashcards");
    else if (type === "Camera Sign Practice") navigate("/practice/camera-sign");
    else if (type === "Sign Sentences") navigate("/practice/sign-sentences");
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 px-6 md:px-12 py-10 flex flex-col gap-10">
      {/* Frame 1 */}
      <section className="bg-white rounded-xl shadow-md p-8 w-full max-w-7xl mx-auto min-h-[60vh]">
        <h2 className="font-semibold text-2xl mb-5">Đã học</h2>
        <div className="flex items-center justify-between mb-3">
          <p className="text-4xl font-bold">445/24</p>
          <button
            onClick={() => setShowIgnoredWords(true)}
            className="text-gray-500 hover:text-gray-700 transition"
            title="Xem các từ bị bỏ qua"
          >
            👁️‍🗨️
          </button>
        </div>
        <p className="text-lg text-gray-500 mb-5">Cấp độ nhớ</p>
        <div className="w-full h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="level" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#69a79c" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* Frame 2 */}
      <section className="bg-[#fff2cc] rounded-xl shadow-md p-10 w-full max-w-7xl mx-auto flex flex-col items-center justify-center min-h-[40vh] text-center">
        <p className="text-xl font-medium text-gray-800 mb-5">
          Đã đến lúc ôn tập <span className="font-semibold">445 từ</span>!
        </p>
        <button
          onClick={() => setShowPracticePopup(true)}
          className="bg-[#69a79c] hover:bg-[#5e9b91] text-white text-lg font-semibold px-8 py-3 rounded-lg transition-all duration-200"
        >
          Ôn tập ngay
        </button>
      </section>

      {/* Frame 3 */}
      <section className="bg-white rounded-xl shadow-md p-8 w-full max-w-7xl mx-auto min-h-[60vh]">
        <div className="flex items-center justify-between mb-6">
          <h3 className="font-semibold text-2xl">Các chủ đề gần đây</h3>
          <div className="relative">
            <select
              value={sortOption}
              onChange={(e) => setSortOption(e.target.value)}
              className="border border-gray-300 rounded-md text-base px-3 py-2 focus:outline-none"
            >
              <option>Mới nhất</option>
              <option>Cũ nhất</option>
              <option>Tên: A-Z</option>
              <option>Tên: Z-A</option>
            </select>
          </div>
        </div>

        <ul className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {sortedTopics.map((topic, i) => (
            <li
              key={i}
              className="bg-gray-100 hover:bg-gray-200 rounded-lg px-5 py-4 cursor-pointer flex justify-between items-center transition"
              onClick={() =>
                navigate(`/topic/${encodeURIComponent(topic.name)}`)
              }
            >
              <span className="text-lg">{topic.name}</span>
              <span className="text-gray-400 text-xl">⋮</span>
            </li>
          ))}
        </ul>
      </section>

      {/* Popup các từ bị bỏ qua */}
      {showIgnoredWords && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div
            className="absolute inset-0 bg-black bg-opacity-40"
            onClick={() => setShowIgnoredWords(false)}
          ></div>
          <div className="relative bg-white rounded-xl shadow-lg p-6 w-80 text-center z-10">
            <h4 className="font-semibold mb-3 text-lg">Các từ bị bỏ qua</h4>
            <ul className="mb-4">
              {ignoredWords.map((word, idx) => (
                <li key={idx} className="py-1 border-b last:border-none">
                  {word}
                </li>
              ))}
            </ul>
            <button
              onClick={() => setShowIgnoredWords(false)}
              className="bg-[#69a79c] hover:bg-[#5e9b91] text-white px-4 py-2 rounded-lg text-sm transition-all duration-200"
            >
              Đóng
            </button>
          </div>
        </div>
      )}

      {/* ✅ Popup chọn phương pháp ôn tập */}
      {showPracticePopup && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div
            className="absolute inset-0 bg-black bg-opacity-40"
            onClick={() => setShowPracticePopup(false)}
          ></div>

          <div className="relative bg-white rounded-xl shadow-lg p-8 w-[320px] text-center z-10">
            <h4 className="text-xl font-semibold mb-6 text-gray-800">
              Chọn phương pháp ôn tập
            </h4>
            <div className="flex flex-col gap-4">
              <button
                onClick={() => handleSelectPractice("Flash Cards")}
                className="bg-indigo-500 hover:bg-indigo-600 text-white py-2 rounded-lg font-medium transition"
              >
                Flash Cards
              </button>
              <button
                onClick={() => handleSelectPractice("Camera Sign Practice")}
                className="bg-pink-500 hover:bg-pink-600 text-white py-2 rounded-lg font-medium transition"
              >
                Camera Sign Practice
              </button>
              <button
                onClick={() => handleSelectPractice("Sign Sentences")}
                className="bg-green-500 hover:bg-green-600 text-white py-2 rounded-lg font-medium transition"
              >
                Sign Sentences
              </button>
            </div>
            <button
              onClick={() => setShowPracticePopup(false)}
              className="mt-6 text-gray-500 hover:text-gray-700 text-sm"
            >
              Hủy
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Practice;
