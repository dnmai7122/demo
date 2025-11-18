import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

const chartData = [
  { level: "Cấp 1", count: 120 },
  { level: "Cấp 2", count: 180 },
  { level: "Cấp 3", count: 90 },
  { level: "Cấp 4", count: 45 },
  { level: "Nhớ sâu", count: 10 },
];

const TopicDetail = () => {
  const { topicName } = useParams();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 px-10 py-10 flex flex-col gap-10">
      <div className="flex items-center justify-between w-full max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold">{decodeURIComponent(topicName)}</h1>
        <button
          onClick={() => navigate(-1)}
          className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg transition"
        >
          ← Quay lại
        </button>
      </div>

      {/* Frame 1 */}
      <section className="bg-white rounded-xl shadow-md p-8 w-full max-w-6xl mx-auto min-h-[60vh]">
        <h2 className="font-semibold text-2xl mb-5">Đã học</h2>
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
      <section className="bg-[#fff2cc] rounded-xl shadow-md p-10 w-full max-w-6xl mx-auto flex flex-col items-center justify-center min-h-[40vh] text-center">
        <p className="text-xl font-medium text-gray-800 mb-5">
          Ôn tập chủ đề <span className="font-semibold">{decodeURIComponent(topicName)}</span>
        </p>
        <button className="bg-[#69a79c] hover:bg-[#5e9b91] text-white text-lg font-semibold px-8 py-3 rounded-lg transition-all duration-200">
          Ôn tập ngay
        </button>
      </section>
    </div>
  );
};

export default TopicDetail;
