import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchTopics, fetchLessonsByTopic, fetchUnitsByLesson } from "../services/api";

const Courses = () => {
	const { courseId } = useParams();
	const [currentVideoIndex, setCurrentVideoIndex] = useState(0);
	const [currentLessonIndex, setCurrentLessonIndex] = useState(0);
	const [topics, setTopics] = useState([]);
	const [lessons, setLessons] = useState([]);
	const [units, setUnits] = useState([]); // Units (videos) for current lesson
	const [currentTopic, setCurrentTopic] = useState(null);
	const [loading, setLoading] = useState(true);
	const [loadingUnits, setLoadingUnits] = useState(false);
	const [error, setError] = useState(null);
	const [cameraEnabled, setCameraEnabled] = useState(false);
	const [stream, setStream] = useState(null);
	const videoRef = useRef(null);
	const cameraTimeoutRef = useRef(null);
	const lastActivityRef = useRef(Date.now());

	// Function to enable camera
	const enableCamera = async () => {
		try {
			console.log("Requesting camera access...");
			const mediaStream = await navigator.mediaDevices.getUserMedia({ 
				video: {
					width: { ideal: 1280 },
					height: { ideal: 720 },
					facingMode: "user"
				},
				audio: false 
			});
			console.log("Camera access granted. Stream:", mediaStream);
			console.log("Video tracks:", mediaStream.getVideoTracks());
			
			setStream(mediaStream);
			setCameraEnabled(true);
			
			// Wait for next render cycle then set video stream
			setTimeout(() => {
				if (videoRef.current) {
					console.log("Setting srcObject to video element");
					videoRef.current.srcObject = mediaStream;
					videoRef.current.play().catch(err => console.error("Error playing video:", err));
				} else {
					console.error("videoRef.current is null");
				}
			}, 100);
		} catch (err) {
			console.error("Error accessing camera:", err);
			alert("Không thể truy cập camera. Vui lòng kiểm tra quyền truy cập camera trong trình duyệt.");
		}
	};

	// Function to disable camera
	const disableCamera = () => {
		if (stream) {
			stream.getTracks().forEach(track => track.stop());
			setStream(null);
		}
		setCameraEnabled(false);
		
		// Clear timeout when manually disabling
		if (cameraTimeoutRef.current) {
			clearTimeout(cameraTimeoutRef.current);
			cameraTimeoutRef.current = null;
		}
	};

	// Function to reset camera timeout using useCallback to avoid stale closure
	const resetCameraTimeout = useCallback(() => {
		lastActivityRef.current = Date.now();
		
		// Clear existing timeout
		if (cameraTimeoutRef.current) {
			clearTimeout(cameraTimeoutRef.current);
		}
		
		// Set new timeout for 5 seconds
		if (cameraEnabled && stream) {
			cameraTimeoutRef.current = setTimeout(() => {
				console.log("Camera auto-off after 5 seconds of inactivity");
				// Directly stop camera without calling disableCamera to avoid circular logic
				stream.getTracks().forEach(track => track.stop());
				setStream(null);
				setCameraEnabled(false);
			}, 5000);
		}
	}, [cameraEnabled, stream]);

	// Update video element when stream changes
	useEffect(() => {
		if (stream && videoRef.current && cameraEnabled) {
			videoRef.current.srcObject = stream;
			videoRef.current.play().catch(err => console.error("Error playing video:", err));
		}
	}, [stream, cameraEnabled]);

	// Start timeout when camera is enabled
	useEffect(() => {
		if (cameraEnabled && stream) {
			console.log("Camera enabled, starting 5-second timeout");
			resetCameraTimeout();
		}
		
		return () => {
			if (cameraTimeoutRef.current) {
				clearTimeout(cameraTimeoutRef.current);
			}
		};
	}, [cameraEnabled, stream, resetCameraTimeout]);

	// Reset timeout on user activity (video navigation)
	useEffect(() => {
		if (cameraEnabled && stream) {
			console.log("Activity detected: video/lesson changed, resetting timeout");
			resetCameraTimeout();
		}
	}, [currentVideoIndex, currentLessonIndex, cameraEnabled, stream, resetCameraTimeout]);

	// Detect user activity and reset timeout
	useEffect(() => {
		if (!cameraEnabled || !stream) return;

		const handleActivity = () => {
			console.log("User activity detected, resetting camera timeout");
			resetCameraTimeout();
		};

		// Add event listeners for user activity
		window.addEventListener('mousemove', handleActivity);
		window.addEventListener('mousedown', handleActivity);
		window.addEventListener('keydown', handleActivity);
		window.addEventListener('scroll', handleActivity);
		window.addEventListener('touchstart', handleActivity);

		return () => {
			// Cleanup event listeners
			window.removeEventListener('mousemove', handleActivity);
			window.removeEventListener('mousedown', handleActivity);
			window.removeEventListener('keydown', handleActivity);
			window.removeEventListener('scroll', handleActivity);
			window.removeEventListener('touchstart', handleActivity);
		};
	}, [cameraEnabled, stream, resetCameraTimeout]);

	// Cleanup camera when component unmounts or lesson changes
	useEffect(() => {
		return () => {
			if (stream) {
				stream.getTracks().forEach(track => track.stop());
			}
			if (cameraTimeoutRef.current) {
				clearTimeout(cameraTimeoutRef.current);
			}
		};
	}, [stream]);

	// Fetch topics from API
	useEffect(() => {
		const loadTopics = async () => {
			try {
				setLoading(true);
				const data = await fetchTopics();
				setTopics(data);
				setError(null);
			} catch (err) {
				console.error('Failed to load topics:', err);
				setError('Không thể tải danh sách chủ đề. Vui lòng thử lại sau.');
			} finally {
				setLoading(false);
			}
		};

		loadTopics();
	}, []);

	// Fetch lessons when courseId changes
	useEffect(() => {
		if (!courseId) return;

		const loadLessons = async () => {
			try {
				setLoading(true);
				
				// Find topic by code (slug)
				const topic = topics.find(t => t.code === courseId.toUpperCase());
				
				if (!topic) {
					setError('Không tìm thấy chủ đề này.');
					setLoading(false);
					return;
				}

				setCurrentTopic(topic);

				// Fetch lessons for this topic
				const lessonsData = await fetchLessonsByTopic(topic.id);
				setLessons(lessonsData);
				setError(null);
			} catch (err) {
				console.error('Failed to load lessons:', err);
				setError('Không thể tải danh sách bài học. Vui lòng thử lại sau.');
			} finally {
				setLoading(false);
			}
		};

		loadLessons();
	}, [courseId, topics]);

	// Fetch units (videos) when lesson changes
	useEffect(() => {
		if (!lessons || lessons.length === 0) return;
		
		const currentLesson = lessons[currentLessonIndex];
		if (!currentLesson) return;

		const loadUnits = async () => {
			try {
				setLoadingUnits(true);
				const unitsData = await fetchUnitsByLesson(currentLesson.lesson_id || currentLesson.id);
				setUnits(unitsData);
				setCurrentVideoIndex(0); // Reset video về đầu khi chuyển lesson
			} catch (err) {
				console.error('Failed to load units:', err);
				setUnits([]); // Clear units on error
			} finally {
				setLoadingUnits(false);
			}
		};

		loadUnits();
	}, [currentLessonIndex, lessons]);

	// Map topics to course format for display
	const recommendedCourses = topics.map((topic) => ({
		id: topic.id,
		slug: topic.code, // Use code as slug from database
		title: topic.name,
		description: topic.description || `Học về ${topic.name}`,
		image: topic.cover_image_url || `${topic.code}-course.jpg`,
		coverVideo: topic.cover_video_url,
		level: topic.level,
		lessons: topic.SL_lesson || 0, // Number of lessons from database
		SL_lesson: topic.SL_lesson || 0 // Keep original field name for display
	}));

	// Nếu không có courseId, chỉ hiển thị danh sách các chủ đề
	if (!courseId) {
		return (
			<div className="min-h-screen bg-white max-w-7xl mx-auto">
				{/* Header */}
				<div className="bg-secondary text-white py-6">
					<div className="container mx-auto px-4">
						<h1 className="text-3xl font-bold">Các chủ đề ngôn ngữ ký hiệu</h1>
					</div>
				</div>

				<div className="container mx-auto px-4 py-8">
					{/* Loading state */}
					{loading && (
						<div className="text-center py-20">
							<p className="text-xl text-gray-600">Đang tải danh sách chủ đề...</p>
						</div>
					)}

					{/* Error state */}
					{error && (
						<div className="text-center py-20">
							<p className="text-xl text-red-600">{error}</p>
						</div>
					)}

					{/* Các chủ đề */}
					{!loading && !error && (
						<section>
							<div className="flex justify-between items-center mb-6">
								<h2 className="text-2xl font-bold">Các chủ đề</h2>
							</div>

							<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
								{recommendedCourses.map((course) => (
									<Link
										to={`/courses/${course.slug}`}
										key={course.id} 
										className="border rounded-lg overflow-hidden hover:shadow-lg transition-shadow cursor-pointer block"
									>
										<div className="bg-gray-100 h-64 flex items-center justify-center overflow-hidden">
											{/* Hiển thị hình ảnh thực từ database */}
											{course.image && course.image.startsWith('http') ? (
												<img 
													src={course.image} 
													alt={course.title} 
													className="w-full h-full object-cover"
													onError={(e) => {
														e.target.style.display = 'none';
														e.target.nextSibling.style.display = 'flex';
													}}
												/>
											) : null}
											<div 
												className="w-full h-full bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center"
												style={{ display: course.image && course.image.startsWith('http') ? 'none' : 'flex' }}
											>
												<span className="text-6xl">📚</span>
											</div>
										</div>
										<div className="p-4">
											<div className="flex justify-between items-start mb-2">
												<h3 className="text-xl font-semibold">{course.title}</h3>
												<span className="text-sm text-gray-500">{course.SL_lesson} bài học</span>
											</div>
											<p className="text-gray-600 text-sm mb-3">{course.description}</p>
											<span className="text-secondary font-medium hover:underline">
												Xem khóa học →
											</span>
										</div>
									</Link>
								))}
							</div>
						</section>
					)}
				</div>

				{/* Footer Contact Info */}
				<footer className="bg-light mt-16 py-8">
					<div className="container mx-auto px-4">
						<div className="grid md:grid-cols-3 gap-8">
							<div>
								<h3 className="font-bold mb-3">Trang</h3>
								<ul className="space-y-2 text-sm">
									<li><a href="#" className="hover:text-secondary">Trang chủ</a></li>
									<li><a href="#" className="hover:text-secondary">Chủ đề</a></li>
									<li><a href="#" className="hover:text-secondary">Tìm kiếm</a></li>
								</ul>
							</div>
							<div>
								<h3 className="font-bold mb-3">About Us</h3>
								<ul className="space-y-2 text-sm">
									<li><a href="#" className="hover:text-secondary">Về chúng tôi</a></li>
									<li><a href="#" className="hover:text-secondary">Đội ngũ</a></li>
									<li><a href="#" className="hover:text-secondary">Blog của chúng tôi</a></li>
								</ul>
							</div>
							<div>
								<h3 className="font-bold mb-3">Social Media</h3>
								<ul className="space-y-2 text-sm">
									<li>📧 movingtotalk@gmail.com</li>
									<li>📱 +84 868 555 2363</li>
									<li>📍 123 Nguyễn Văn Cừ, TP.HCM</li>
								</ul>
							</div>
						</div>
						<div className="text-center mt-8 text-sm text-gray-600">
							© 2025 Moving to Talk. All rights reserved
						</div>
					</div>
				</footer>
			</div>
		);
	}

	// Nếu có courseId, hiển thị chi tiết khóa học với lesson và video
	if (courseId) {
		// Show loading state
		if (loading) {
			return (
				<div className="min-h-screen bg-white max-w-7xl mx-auto">
					<div className="bg-secondary text-white py-6">
						<div className="container mx-auto px-4">
							<h1 className="text-3xl font-bold">Đang tải...</h1>
						</div>
					</div>
					<div className="text-center py-20">
						<p className="text-xl text-gray-600">Đang tải bài học...</p>
					</div>
				</div>
			);
		}

		// Show error state
		if (error || !currentTopic) {
			return (
				<div className="min-h-screen bg-white max-w-7xl mx-auto">
					<div className="bg-secondary text-white py-6">
						<div className="container mx-auto px-4">
							<h1 className="text-3xl font-bold">Lỗi</h1>
						</div>
					</div>
					<div className="text-center py-20">
						<p className="text-xl text-red-600">{error || 'Không tìm thấy chủ đề này.'}</p>
						<Link to="/courses" className="text-secondary hover:underline mt-4 inline-block">
							← Quay lại danh sách chủ đề
						</Link>
					</div>
				</div>
			);
		}

		// Check if lessons exist
		if (!lessons || lessons.length === 0) {
			return (
				<div className="min-h-screen bg-white max-w-7xl mx-auto">
					<div className="bg-secondary text-white py-6">
						<div className="container mx-auto px-4">
							<h1 className="text-3xl font-bold">{currentTopic.name}</h1>
						</div>
					</div>
					<div className="text-center py-20">
						<p className="text-xl text-gray-600">Chưa có bài học nào cho chủ đề này.</p>
						<Link to="/courses" className="text-secondary hover:underline mt-4 inline-block">
							← Quay lại danh sách chủ đề
						</Link>
					</div>
				</div>
			);
		}

		const currentLesson = lessons[currentLessonIndex];
		const totalLessons = lessons.length;
		
		// Use real units data from API
		const currentVideo = units[currentVideoIndex];
		const totalVideosInLesson = units.length;

		// Show loading state for units
		if (loadingUnits || !currentVideo) {
			return (
				<div className="min-h-screen bg-white max-w-7xl mx-auto">
					<div className="bg-secondary text-white py-6">
						<div className="container mx-auto px-4">
							<h1 className="text-3xl font-bold">{currentTopic.name}</h1>
							<p className="text-white/80 mt-2">{currentLesson.title}</p>
						</div>
					</div>
					<div className="text-center py-20">
						<p className="text-xl text-gray-600">Đang tải nội dung bài học...</p>
					</div>
				</div>
			);
		}

		const handleNext = () => {
			if (currentVideoIndex < totalVideosInLesson - 1) {
				setCurrentVideoIndex(currentVideoIndex + 1);
			}
		};

		const handleBack = () => {
			if (currentVideoIndex > 0) {
				setCurrentVideoIndex(currentVideoIndex - 1);
			}
		};

		const handleCompleteLesson = () => {
			if (currentLessonIndex < totalLessons - 1) {
				setCurrentLessonIndex(currentLessonIndex + 1);
				// Video sẽ được reset tự động bởi useEffect khi currentLessonIndex thay đổi
			}
		};

		const isLastVideoInLesson = currentVideoIndex === totalVideosInLesson - 1;

		return (
			<div className="min-h-screen bg-white max-w-7xl mx-auto">
				{/* Header */}
				<div className="bg-secondary text-white py-6">
					<div className="container mx-auto px-4">
						<h1 className="text-3xl font-bold">{currentTopic.name}</h1>
						<p className="text-white/80 mt-2">{currentLesson.title}</p>
					</div>
				</div>

			<div className="container mx-auto px-4 py-8">
				{/* Video hiện tại */}
				<section className="mb-8">
					<div className="flex justify-between items-center mb-4">
						<h2 className="text-2xl font-bold">Từ khoá: {currentVideo.text || currentVideo.title}</h2>
						<div className="text-right">
							<p className="text-gray-600 font-medium">Lesson {currentLessonIndex + 1}/{totalLessons}</p>
							<p className="text-sm text-gray-500">Video {currentVideoIndex + 1}/{totalVideosInLesson}</p>
						</div>
					</div>
					
					{/* Hiển thị mô tả từ cột description */}
					{currentVideo.description && (
						<div className="mb-4">
							<p className="text-gray-700 text-lg whitespace-pre-line">
								{currentVideo.description}
							</p>
						</div>
					)}
					
					<div className="bg-gray-100 p-3 rounded-lg mb-3">
						{/* Video section - split when camera enabled */}
						<div className={`grid ${cameraEnabled ? 'grid-cols-2' : 'grid-cols-1'} gap-4`}>
							{/* Video YouTube embedded */}
							<div className="aspect-video w-full">
								<iframe
									width="100%"
									height="100%"
									src={currentVideo.video_url}
									title={currentVideo.text || currentVideo.title}
									allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
									allowFullScreen
									className="rounded-lg"
								></iframe>
							</div>

							{/* Camera view - only show when enabled */}
							{cameraEnabled && (
								<div className="aspect-video w-full bg-black rounded-lg overflow-hidden relative">
									<video
										ref={videoRef}
										autoPlay
										playsInline
										muted
										className="w-full h-full object-cover transform scale-x-[-1]"
										style={{ backgroundColor: '#000' }}
										onLoadedMetadata={() => console.log('Video metadata loaded')}
										onPlay={() => console.log('Video playing')}
									/>
									<div className="absolute top-2 right-2 z-10">
										<button
											onClick={disableCamera}
											className="bg-red-600 text-white px-3 py-1 rounded-full text-sm hover:bg-red-700 transition-all shadow-lg"
										>
											✕ Tắt camera
										</button>
									</div>
									<div className="absolute bottom-2 left-2 bg-black/50 text-white px-2 py-1 rounded text-sm z-10">
										Camera của bạn
									</div>
									{!stream && (
										<div className="absolute inset-0 flex items-center justify-center text-white">
											<p>Đang kết nối camera...</p>
										</div>
									)}
								</div>
							)}
						</div>

						{/* Camera control button */}
						{!cameraEnabled && (
							<div className="mt-4 text-center">
								<button
									onClick={enableCamera}
									className="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 transition-all flex items-center gap-2 mx-auto"
								>
									Mở camera để thực hành cùng video hướng dẫn
								</button>
							</div>
						)}
						
						{/* Display image if available and camera not enabled */}
						{!cameraEnabled && currentVideo.image_url && (
							<div className="mt-4 text-center">
								<img 
									src={currentVideo.image_url} 
									alt={currentVideo.text}
									className="max-w-xs mx-auto rounded-lg shadow-md"
									onError={(e) => {
										e.target.style.display = 'none';
									}}
								/>
							</div>
						)}
						
						{/* Display transcription if available */}
						{currentVideo.transcription && (
							<div className="mt-4 p-4 bg-white rounded-lg">
								<p className="text-gray-700 text-center italic">{currentVideo.transcription}</p>
							</div>
						)}
					</div>

					{/* Nút điều hướng Next/Back/Complete */}
					<div className="flex justify-between items-center max-w-4xl mx-auto">
						<button
							onClick={handleBack}
							disabled={currentVideoIndex === 0}
							className={`px-6 py-3 rounded-lg font-semibold transition-all ${
								currentVideoIndex === 0
									? 'bg-gray-300 text-gray-500 cursor-not-allowed'
									: 'bg-secondary text-white hover:bg-opacity-90'
							}`}
						>
							← Back
						</button>
						
						<div className="text-center">
							<p className="text-sm text-gray-600">
								Lesson {currentLessonIndex + 1}/{totalLessons} - Video {currentVideoIndex + 1}/{totalVideosInLesson}
							</p>
						</div>

						{/* Nếu là video cuối của lesson, hiện nút Hoàn thành */}
						{isLastVideoInLesson ? (
							<button
								onClick={handleCompleteLesson}
								disabled={currentLessonIndex === totalLessons - 1}
								className={`px-6 py-3 rounded-lg font-semibold transition-all ${
									currentLessonIndex === totalLessons - 1
										? 'bg-green-300 text-gray-500 cursor-not-allowed'
										: 'bg-green-600 text-white hover:bg-green-700'
								}`}
							>
								{currentLessonIndex === totalLessons - 1 ? 'Hoàn thành chủ đề ✓' : 'Hoàn thành lesson →'}
							</button>
						) : (
							<button
								onClick={handleNext}
								className="px-6 py-3 rounded-lg font-semibold bg-secondary text-white hover:bg-opacity-90 transition-all"
							>
								Next →
							</button>
						)}
					</div>
				</section>

				{/* Các chủ đề khác */}
				<section>
					<div className="flex justify-between items-center mb-6">
						<h2 className="text-2xl font-bold">Các chủ đề khác</h2>

					</div>

					<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
						{recommendedCourses.map((course) => (
							<Link
								to={`/courses/${course.slug}`}
								key={course.id} 
								className="border rounded-lg overflow-hidden hover:shadow-lg transition-shadow cursor-pointer block"
							>
								<div className="bg-gray-100 h-64 flex items-center justify-center overflow-hidden">
									{/* Hiển thị hình ảnh thực từ database */}
									{course.image && course.image.startsWith('http') ? (
										<img 
											src={course.image} 
											alt={course.title} 
											className="w-full h-full object-cover"
											onError={(e) => {
												e.target.style.display = 'none';
												e.target.nextSibling.style.display = 'flex';
											}}
										/>
									) : null}
									<div 
										className="w-full h-full bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center"
										style={{ display: course.image && course.image.startsWith('http') ? 'none' : 'flex' }}
									>
										<span className="text-6xl">📚</span>
									</div>
								</div>
								<div className="p-4">
									<div className="flex justify-between items-start mb-2">
										<h3 className="text-xl font-semibold">{course.title}</h3>
										<span className="text-sm text-gray-500">{course.SL_lesson} bài học</span>
									</div>
									<p className="text-gray-600 text-sm mb-3">{course.description}</p>
									<span className="text-secondary font-medium hover:underline">
										Xem khóa học →
									</span>
								</div>
							</Link>
						))}
					</div>
				</section>
			</div>
		</div>
		);
	}
};

export default Courses;
