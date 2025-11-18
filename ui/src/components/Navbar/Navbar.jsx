import React, { useState, useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { IoMdMenu, IoMdClose } from "react-icons/io";
import { FaUserCircle } from "react-icons/fa";
import { motion, AnimatePresence } from "framer-motion";

const NavbarMenu = [
  { id: 1, title: "Trang chủ", path: "/" },
  { id: 2, title: "Chủ đề", path: "/topics" },
  { id: 3, title: "Tìm kiếm", path: "/search" },
  { id: 4, title: "Luyện tập", path: "/practice" },
  { id: 5, title: "Cộng đồng", path: "/community" }
];

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const currentPath = location.pathname;
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [user, setUser] = useState(null);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const toggleMobileMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen);

  // Check if user is logged in
  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (error) {
        console.error("Error parsing user data:", error);
        localStorage.removeItem("user");
      }
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUser(null);
    setShowUserMenu(false);
    navigate("/");
  };

  return (
    <nav className="relative z-50 w-full bg-white shadow-sm">
      {/* ==== Desktop Navbar ==== */}
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="container mx-auto flex items-center justify-between px-0 py-0"
      >
    {/* Logo */}
    <div className="flex items-center ml-12">
      <img
        src="/mtt.svg"
        alt="MTT Logo"
        className="h-32 w-32 object-contain" 
      />
    </div>
        {/* Desktop Menu */}
        <div className="hidden lg:block">
          <ul className="flex items-center gap-6">
            {NavbarMenu.map((menu) => {
              const isActive =
                currentPath === menu.path ||
                (menu.path === "/topics" && (currentPath === "/courses" || currentPath.startsWith("/courses/"))) ||
                (menu.path === "/practice" && currentPath.startsWith("/practice")) ||
                (menu.path === "/search" && currentPath.startsWith("/search")) ||
                (menu.path === "/community" && currentPath.startsWith("/community"));

              return (
                <li key={menu.id}>
                  <Link
                    to={menu.path}
                    className={`relative px-3 py-2 text-base font-medium transition-colors ${
                      isActive ? "text-secondary font-bold" : "text-gray-700 hover:text-secondary"
                    }`}
                  >
                    {menu.title}

                    {/* Active dot */}
                    <span
                      className={`absolute left-1/2 -translate-x-1/2 -bottom-1 h-2 w-2 rounded-full bg-secondary transition-opacity ${
                        isActive ? "opacity-100" : "opacity-0 group-hover:opacity-100"
                      }`}
                    />
                  </Link>
                </li>
              );
            })}

            {user ? (
              <li className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <FaUserCircle className="text-3xl text-secondary" />
                  <span className="font-medium text-gray-700">{user.display_name}</span>
                </button>

                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border py-2 z-50">
                    <Link
                      to="/profile"
                      onClick={() => setShowUserMenu(false)}
                      className="block px-4 py-2 hover:bg-gray-100 transition-colors"
                    >
                      Trang cá nhân
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors text-red-600"
                    >
                      Đăng xuất
                    </button>
                  </div>
                )}
              </li>
            ) : (
              <Link to="/login">
                <button className="primary-btn px-4 py-2">Sign In</button>
              </Link>
            )}
          </ul>
        </div>

        {/* Mobile Hamburger */}
        <div className="lg:hidden text-4xl cursor-pointer">
          <button onClick={toggleMobileMenu}>
            {isMobileMenuOpen ? <IoMdClose /> : <IoMdMenu />}
          </button>
        </div>
      </motion.div>

      {/* ==== Mobile Menu ==== */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="lg:hidden bg-white shadow-lg border-t overflow-hidden"
          >
            <ul className="flex flex-col p-4 gap-2">
              {NavbarMenu.map((menu) => {
                const isActive =
                  currentPath === menu.path ||
                  (menu.path === "/topics" && (currentPath === "/courses" || currentPath.startsWith("/courses/"))) ||
                  (menu.path === "/practice" && currentPath.startsWith("/practice")) ||
                  (menu.path === "/search" && currentPath.startsWith("/search")) ||
                  (menu.path === "/community" && currentPath.startsWith("/community"));

                return (
                  <li key={menu.id}>
                    <Link
                      to={menu.path}
                      onClick={() => setIsMobileMenuOpen(false)}
                      className={`block w-full px-4 py-3 rounded-lg text-base transition-all ${
                        isActive
                          ? "bg-secondary/10 text-secondary font-semibold"
                          : "text-gray-700 hover:bg-secondary/10 hover:text-secondary"
                      }`}
                    >
                      {menu.title}
                    </Link>
                  </li>
                );
              })}

              {user ? (
                <>
                  <li className="mt-2 border-t pt-2">
                    <div className="flex items-center gap-3 px-4 py-3">
                      <FaUserCircle className="text-4xl text-secondary" />
                      <div>
                        <p className="font-medium text-gray-700">{user.display_name}</p>
                        <p className="text-sm text-gray-500">{user.email}</p>
                      </div>
                    </div>
                  </li>
                  <li>
                    <Link
                      to="/profile"
                      onClick={() => setIsMobileMenuOpen(false)}
                      className="block w-full px-4 py-3 rounded-lg text-base text-gray-700 hover:bg-secondary/10 hover:text-secondary transition-all"
                    >
                      Trang cá nhân
                    </Link>
                  </li>
                  <li>
                    <button
                      onClick={() => {
                        handleLogout();
                        setIsMobileMenuOpen(false);
                      }}
                      className="w-full text-left px-4 py-3 rounded-lg text-base text-red-600 hover:bg-red-50 transition-all"
                    >
                      Đăng xuất
                    </button>
                  </li>
                </>
              ) : (
                <li className="mt-2">
                  <Link to="/login" onClick={() => setIsMobileMenuOpen(false)}>
                    <button className="primary-btn w-full py-4">Sign In</button>
                  </Link>
                </li>
              )}
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;