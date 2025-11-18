import React from "react";
import { Link } from "react-router-dom";

const Topics = () => {
	return (
		<div className="container mx-auto py-20 px-4">
			<h1 className="text-4xl font-bold text-center mb-8">Chủ đề</h1>
			
			{/* Tổng quan */}
			<div className="max-w-4xl mx-auto mb-12">
				<section className="mb-8">
					<h2 className="text-2xl font-semibold mb-4">Tổng quan về ngôn ngữ ký hiệu</h2>
					<p className="text-gray-700 mb-4">
						Ngôn ngữ ký hiệu là một hệ thống ngôn ngữ đầy đủ sử dụng các cử chỉ tay, biểu cảm khuôn mặt, 
						và ngôn ngữ cơ thể để giao tiếp. Đây là ngôn ngữ chính của cộng đồng người Điếc và là một phần 
						quan trọng của văn hóa Điếc.
					</p>
					<p className="text-gray-700 mb-4">
						Học ngôn ngữ ký hiệu không chỉ giúp bạn giao tiếp với người Điếc mà còn mở ra một thế giới mới 
						về văn hóa, cộng đồng và cách thức giao tiếp độc đáo. Moving to Talk cung cấp các khóa học từ 
						cơ bản đến nâng cao để giúp bạn thành thạo ngôn ngữ ký hiệu.
					</p>
				</section>

				<section className="mb-8">
					<h2 className="text-2xl font-semibold mb-4">Các cấp độ học tập</h2>
					<div className="grid md:grid-cols-3 gap-6">
						<div className="bg-light p-6 rounded-lg">
							<h3 className="text-xl font-semibold mb-2">Cơ bản</h3>
							<p className="text-gray-600">Học bảng chữ cái, số đếm và các từ vựng hàng ngày cơ bản</p>
						</div>
						<div className="bg-light p-6 rounded-lg">
							<h3 className="text-xl font-semibold mb-2">Trung cấp</h3>
							<p className="text-gray-600">Nâng cao từ vựng và luyện tập các câu giao tiếp thông dụng</p>
						</div>
						<div className="bg-light p-6 rounded-lg">
							<h3 className="text-xl font-semibold mb-2">Nâng cao</h3>
							<p className="text-gray-600">Thành thạo giao tiếp phức tạp và tìm hiểu văn hóa Điếc</p>
						</div>
					</div>
				</section>

				{/* Link to Courses */}
				<div className="text-center mt-12">
					<Link 
						to="/courses" 
						className="inline-block bg-secondary text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-opacity-90 transition-all"
					>
						Khám phá các khóa học →
					</Link>
				</div>
			</div>
		</div>
	);
};

export default Topics;
