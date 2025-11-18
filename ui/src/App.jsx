import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Hero/Hero";
import Topic from "./components/Topic/Topic";
import Banner from "./components/Banner/Banner";
import Subscribe from "./components/Subscribe/Subscribe";
import Banner2 from "./components/Banner/Banner2";
import Footer from "./components/Footer/Footer";
import Home from "./pages/Home";
import Topics from "./pages/Topics";
import Search from "./pages/Search";
import Practice from "./pages/Practice";
import Community from "./pages/Community";
import Login from "./pages/Login";
import Register from "./pages/Register"; // ✅ thêm trang đăng ký
import Courses from "./pages/Courses";
import TopicPage from "./pages/TopicPage"; 
import DiscussionDetail from "./pages/DiscussionDetail";
import FlashCardsPractice from "./pages/FlashCardsPractice";
import CameraSignPractice from "./pages/CameraSignPractice";
import "@fortawesome/fontawesome-free/css/all.min.css";


const HomePage = () => {
  return (
    <>
      <Hero />
      <Topic />
      <Banner />
      <Subscribe />
      <Banner2 />
    </>
  );
};

const App = () => {
  return (
    <Router>
      <main className="overflow-x-hidden bg-white text-dark">
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/topics" element={<Topics />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/courses/:courseId" element={<Courses />} />
          <Route path="/search" element={<Search />} />
          <Route path="/practice" element={<Practice />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} /> {/* ✅ thêm route đăng ký */}
          <Route path="/topic/:topicName" element={<TopicPage />} />
          <Route path="/community" element={<Community />} />
          <Route path="/discussion/:type" element={<DiscussionDetail />} /> 
          <Route path="/practice/flashcards" element={<FlashCardsPractice />} />
          <Route path="/practice/camera-sign" element={<CameraSignPractice />} />
        
        </Routes>
        <Footer />
      </main>
    </Router>
  );
};

export default App;
