import React from "react";
import { motion } from "framer-motion";
import { X } from "lucide-react";

const LoginModal = ({ isOpen, onClose, onRegisterClick }) => {
  if (!isOpen) return null;

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

        <h2 className="text-2xl font-bold text-center mb-6">Đăng nhập</h2>

        <form className="space-y-5">
          <div>
            <label className="text-sm font-medium">Tên đăng nhập</label>
            <input
              type="text"
              placeholder="Nhập tên đăng nhập"
              className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-indigo-400 outline-none"
            />
          </div>

          <div>
            <label className="text-sm font-medium">Mật khẩu</label>
            <input
              type="password"
              placeholder="Nhập mật khẩu"
              className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-indigo-400 outline-none"
            />
            <div className="text-right mt-1">
              <a href="#" className="text-sm text-indigo-500 hover:underline">
                Quên mật khẩu?
              </a>
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-indigo-400 to-pink-500 text-white py-2 rounded-md font-semibold shadow-md hover:opacity-90 transition"
          >
            Đăng nhập
          </button>
        </form>

        {/* Mạng xã hội */}
        <div className="mt-6 flex flex-col items-center space-y-3">
          <p className="text-gray-500 text-sm">Hoặc đăng nhập bằng</p>
          <div className="flex space-x-4">
            <button className="w-10 h-10 rounded-full bg-[#1877F2] flex items-center justify-center hover:opacity-90 transition">
              <i className="fab fa-facebook-f text-white text-lg"></i>
            </button>
            <button className="w-10 h-10 rounded-full bg-black flex items-center justify-center hover:opacity-90 transition">
              <i className="fab fa-x-twitter text-white text-lg"></i>
            </button>
            <button className="w-10 h-10 rounded-full bg-[#EA4335] flex items-center justify-center hover:opacity-90 transition">
              <i className="fab fa-google text-white text-lg"></i>
            </button>
          </div>
        </div>

        {/* Liên kết đăng ký */}
        <div className="text-center mt-6 text-sm text-gray-500">
          Chưa có tài khoản?{" "}
          <button
            type="button"
            onClick={() => {
              onClose(); // đóng login
              if (onRegisterClick) onRegisterClick(); // bật register
            }}
            className="text-indigo-500 hover:underline"
          >
            Đăng ký
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default LoginModal;
