import React, { useState } from "react";
import { motion } from "framer-motion";
import { X } from "lucide-react";

const RegisterModal = ({ isOpen, onClose, onLoginClick }) => {
  if (!isOpen) return null;

  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Registering:", formData);
    // 👉 Thêm logic đăng ký (API, validate, v.v.)
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        className="bg-white rounded-2xl p-8 w-[400px] shadow-xl relative"
      >
        {/* Nút đóng */}
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
        >
          <X size={20} />
        </button>

        <h2 className="text-2xl font-bold text-center mb-6 text-indigo-500">
          Tạo tài khoản
        </h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="text-sm font-medium">Họ và tên</label>
            <input
              type="text"
              name="fullName"
              placeholder="Nhập họ và tên"
              value={formData.fullName}
              onChange={handleChange}
              className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-indigo-400 outline-none"
              required
            />
          </div>

          <div>
            <label className="text-sm font-medium">Email</label>
            <input
              type="email"
              name="email"
              placeholder="Nhập email"
              value={formData.email}
              onChange={handleChange}
              className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-indigo-400 outline-none"
              required
            />
          </div>

          <div>
            <label className="text-sm font-medium">Mật khẩu</label>
            <input
              type="password"
              name="password"
              placeholder="Nhập mật khẩu"
              value={formData.password}
              onChange={handleChange}
              className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-indigo-400 outline-none"
              required
            />
          </div>

          <div>
            <label className="text-sm font-medium">Xác nhận mật khẩu</label>
            <input
              type="password"
              name="confirmPassword"
              placeholder="Nhập lại mật khẩu"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-indigo-400 outline-none"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-indigo-400 to-pink-500 text-white py-2 rounded-md font-semibold shadow-md hover:opacity-90 transition"
          >
            Đăng ký
          </button>
        </form>

        {/* Liên kết đăng nhập */}
        <div className="text-center mt-6 text-sm text-gray-500">
          Đã có tài khoản?{" "}
          <button
            type="button"
            onClick={() => {
              onClose(); // đóng popup đăng ký
              if (onLoginClick) onLoginClick(); // mở popup đăng nhập
            }}
            className="text-indigo-500 hover:underline"
          >
            Đăng nhập
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default RegisterModal;
