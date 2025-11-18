import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ChevronRight, MessageSquarePlus, MoreHorizontal } from "lucide-react";
import ava from "../assets/ava.png";

const discussions = [
  {
    id: 1,
    title: "Học bảng chữ cái ngôn ngữ ký hiệu Việt Nam",
    author: "Ngọc Mai",
    date: "07-20-2025 06:14 PM",
    replies: 5,
    views: 325,
    pinned: true,
    latestPost: {
      author: "An Nguyễn",
      date: "1 giờ trước",
    },
  },
  {
    id: 2,
    title: "Làm sao để luyện phản xạ giao tiếp bằng ký hiệu?",
    author: "Minh Tú",
    date: "07-10-2025 09:52 AM",
    replies: 12,
    views: 842,
    latestPost: {
      author: "Thanh Thảo",
      date: "15 phút trước",
    },
  },
  {
    id: 3,
    title: "Chia sẻ video học ký hiệu chủ đề Gia đình",
    author: "Phương Anh",
    date: "3 giờ trước",
    replies: 3,
    views: 121,
    latestPost: {
      author: "Quốc Bảo",
      date: "2 phút trước",
    },
  },
  {
    id: 4,
    title: "Ký hiệu cho các nghề nghiệp thường gặp",
    author: "Hà Linh",
    date: "10-10-2025 12:32 PM",
    replies: 8,
    views: 224,
    latestPost: {
      author: "Lộc Trần",
      date: "30 phút trước",
    },
  },
  {
    id: 5,
    title: "Mẹo nhớ nhanh các ký hiệu bằng hình ảnh",
    author: "Thu Hằng",
    date: "1 ngày trước",
    replies: 6,
    views: 180,
    latestPost: {
      author: "Duy Khang",
      date: "10 phút trước",
    },
  },
];

const DiscussionDetail = () => {
  const { type } = useParams();
  const navigate = useNavigate();

  return (
    <div className="bg-gray-50 min-h-screen text-gray-800 px-5 md:px-16 py-10">
      {/* ✅ Breadcrumb */}
      <div className="text-sm text-gray-600 flex items-center space-x-1 mb-6">
        <span className="hover:underline cursor-pointer" onClick={() => navigate("/")}>
          Trang chủ
        </span>
        <ChevronRight className="w-4 h-4" />
        <span className="hover:underline cursor-pointer" onClick={() => navigate("/community")}>
          Diễn đàn
        </span>
        <ChevronRight className="w-4 h-4" />
        <span className="font-medium text-gray-900">Học ngôn ngữ ký hiệu</span>
      </div>

      {/* Title */}
      <h1 className="text-4xl font-semibold mb-6 capitalize">Chủ đề: {type}</h1>

      {/* Header Buttons */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-medium">Tham gia thảo luận</h2>
        <div className="flex items-center space-x-3">
          <button className="bg-[#176d6d] text-white px-4 py-2 rounded-md flex items-center gap-2 hover:bg-[#0f5555] transition">
            <MessageSquarePlus size={18} />
            Bài đăng mới
          </button>
          <button className="bg-gray-100 border px-3 py-2 rounded-md flex items-center gap-1 hover:bg-gray-200 transition">
            <MoreHorizontal size={18} />
            <span>Tùy chọn</span>
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#e8f5f3] text-gray-700">
              <th className="py-3 px-5">Tiêu đề</th>
              <th className="py-3 px-5 text-center">Phản hồi</th>
              <th className="py-3 px-5 text-center">Lượt xem</th>
            </tr>
          </thead>
          <tbody>
            {discussions.map((d) => (
              <tr
                key={d.id}
                className="border-b hover:bg-gray-50 transition cursor-pointer"
                onClick={() => navigate(`/discussion/${type}/${d.id}`)}
              >
                <td className="py-4 px-5 flex items-start space-x-3">
                  <img src={ava} alt={d.author} className="w-10 h-10 rounded-full object-cover mt-1" />
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-[#176d6d] font-medium hover:underline">{d.title}</span>
                      {d.pinned && (
                        <span className="text-xs bg-teal-600 text-white px-2 py-0.5 rounded">
                          Ghim
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mt-1">
                      bởi <span className="font-medium">{d.author}</span> • {d.date}
                    </p>
                    {d.latestPost && (
                      <p className="text-xs text-gray-500 mt-0.5">
                        Bài mới nhất {d.latestPost.date} bởi{" "}
                        <span className="font-medium">{d.latestPost.author}</span>
                      </p>
                    )}
                  </div>
                </td>
                <td className="text-center text-gray-700">{d.replies}</td>
                <td className="text-center text-gray-700">{d.views}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DiscussionDetail;
