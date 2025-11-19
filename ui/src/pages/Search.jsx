import React, { useRef, useState, useEffect } from "react";
import { Link } from "react-router-dom";

/* Camera SVG */
const CameraIcon = ({ size = 48 }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.8"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="inline-block"
  >
    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
    <circle cx="12" cy="13" r="4" />
  </svg>
);

/* Filter SVG */
const FilterIcon = ({ size = 20 }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth="2"
    stroke="currentColor"
  >
    <path strokeLinecap="round" strokeLinejoin="round" d="M3 4h18M6 12h12M10 20h4" />
  </svg>
);

// ---------------- CONFIG ----------------
const API_URL = "https://bioclimatological-superinclusively-dedra.ngrok-free.dev/predict"; // replace with your backend
const SEQUENCE_LEN = 60; // frames
const CAPTURE_FPS = 12; // capture fps
const STRIP_DATAURL_PREFIX = true; // if backend expects raw base64 without data:image/... prefix

// ---------------- COMPONENT ----------------
const Search = () => {
  const videoRef = useRef(null);
  const captureIntervalRef = useRef(null);

  const [mediaStream, setMediaStream] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [isLoadingCamera, setIsLoadingCamera] = useState(false);
  const [showFilter, setShowFilter] = useState(false);
  const [filters, setFilters] = useState({ duration: "", topic: "", level: "" });

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  // Recording & frames
  const [recording, setRecording] = useState(false);
  const [frames, setFrames] = useState([]); // dataURLs

  // Prediction result(s)
  // expected shape: { label: string, confidence: number, alt?: array } or server may return { prediction, confidence }
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]); // store recent results
  const [isPredicting, setIsPredicting] = useState(false);

  useEffect(() => {
    if (videoRef.current && mediaStream) {
      videoRef.current.srcObject = mediaStream;
      videoRef.current.muted = true;
      const playPromise = videoRef.current.play();
      if (playPromise) playPromise.catch(() => {});
    }
  }, [mediaStream]);

  useEffect(() => {
    return () => stopAndReleaseStream();
  }, []);

  const stopAndReleaseStream = () => {
    if (captureIntervalRef.current) {
      clearInterval(captureIntervalRef.current);
      captureIntervalRef.current = null;
    }
    if (mediaStream) {
      mediaStream.getTracks().forEach((t) => t.stop());
      setMediaStream(null);
    }
    if (videoRef.current) videoRef.current.srcObject = null;
  };

  const openCamera = async () => {
    if (mediaStream) {
      setShowPopup(true);
      return;
    }
    setIsLoadingCamera(true);
    try {
      const s = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } },
        audio: false,
      });
      setMediaStream(s);
      setShowPopup(true);
      setTimeout(() => {
        if (videoRef.current) {
          const play = videoRef.current.play();
          if (play) play.catch(() => {});
        }
      }, 80);
    } catch (err) {
      alert("Không thể truy cập camera. Vui lòng kiểm tra quyền truy cập.");
    } finally {
      setIsLoadingCamera(false);
    }
  };

  const closeCamera = () => {
    setRecording(false);
    setFrames([]);
    stopAndReleaseStream();
    setShowPopup(false);
    setPrediction(null);
    setHistory([]);
  };

  const handleFilterChange = (key, value) => setFilters((p) => ({ ...p, [key]: value }));

  // ---------------- FRAME CAPTURE ----------------
  const captureFrame = () => {
    const video = videoRef.current;
    if (!video) return;
    const w = video.videoWidth || 640;
    const h = video.videoHeight || 480;
    if (w === 0 || h === 0) return; // metadata not ready

    const canvas = document.createElement("canvas");
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, w, h);
    // use JPEG to reduce size
    const dataUrl = canvas.toDataURL("image/jpeg", 0.9);

    setFrames((prev) => {
      const next = [...prev, dataUrl];
      // if reached desired length, stop automatic capture
      if (next.length >= SEQUENCE_LEN) {
        if (captureIntervalRef.current) {
          clearInterval(captureIntervalRef.current);
          captureIntervalRef.current = null;
        }
        setRecording(false);
        // small timeout to let UI update then send
        setTimeout(() => sendFramesToApi(next.slice(0, SEQUENCE_LEN)), 100);
      }
      return next;
    });
  };

  const startRecording = () => {
    if (!videoRef.current || !mediaStream) return;
    setFrames([]);
    setPrediction(null);
    setHistory([]);
    setRecording(true);

    const intervalMs = Math.round(1000 / CAPTURE_FPS);
    captureIntervalRef.current = setInterval(captureFrame, intervalMs);
  };

  const stopRecording = async () => {
    if (captureIntervalRef.current) {
      clearInterval(captureIntervalRef.current);
      captureIntervalRef.current = null;
    }
    setRecording(false);

    if (frames.length > 0) {
      await sendFramesToApi(frames.slice(0, SEQUENCE_LEN));
    }
  };

  // ---------------- SEND TO API ----------------
  // backend expects { images: ["data:image/jpeg;base64,...", ...] }
  // some backends prefer raw base64 strings; STRIP_DATAURL_PREFIX controls that
  const payloadFromDataUrls = (arr) => {
    if (!STRIP_DATAURL_PREFIX) return arr;
    return arr.map((d) => {
      const idx = d.indexOf(",");
      return idx >= 0 ? d.slice(idx + 1) : d;
    });
  };

  const sendFramesToApi = async (imagesArray) => {
    setIsPredicting(true);
    setPrediction(null);

    try {
      const payload = { data: payloadFromDataUrls(imagesArray) };
      const resp = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!resp.ok) {
        const text = await resp.text();
        console.error("API error:", resp.status, text);
        setPrediction({ label: "API Error", confidence: 0 });
        return;
      }

      const data = await resp.json();

      // Support multiple response formats. Normalise to {label, confidence, alt}
      let normalized;
      if (data.prediction || data.label) {
        normalized = {
          label: data.prediction || data.label,
          confidence: data.confidence ?? data.score ?? 0,
          alt: data.alternatives ?? data.top_k ?? null,
        };
      } else if (data.results) {
        // e.g. server returns { results: [ {label, confidence}, ... ] }
        const top = data.results[0] || data.results;
        normalized = {
          label: top.label || "?",
          confidence: top.confidence ?? top.score ?? 0,
          alt: data.results,
        };
      } else {
        normalized = { label: JSON.stringify(data).slice(0, 60), confidence: 0 };
      }

      setPrediction(normalized);
      setHistory((h) => [normalized, ...h].slice(0, 6));

      // also show transient overlay for a few seconds
    } catch (err) {
      console.error("Send frames error:", err);
      setPrediction({ label: "Error", confidence: 0 });
    } finally {
      setIsPredicting(false);
      // keep last frames for debugging but usually we clear them to save memory
      setFrames([]);
    }
  };

  return (
    <div className="min-h-screen bg-white text-gray-900 relative">
      {/* Header */}
      <header className="flex items-center justify-between px-8 py-4 border-b border-gray-200">
        <h1 className="text-xl font-semibold">Tìm kiếm</h1>

        <div className="flex items-center gap-3 relative">
          <input
            type="text"
            placeholder="Tìm kiếm chủ đề"
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
          />

          <button onClick={() => setShowFilter((p) => !p)} className="p-2 rounded-lg bg-secondary">
            <FilterIcon />
          </button>

          {showFilter && (
            <div className="absolute top-12 right-0 bg-white border border-gray-200 rounded-lg p-4 shadow-lg w-60 z-50">
              <h4 className="font-semibold text-sm mb-2">Bộ lọc</h4>
              <div className="space-y-3 text-sm">
                <div>
                  <label className="block text-gray-600 mb-1">Thời gian học</label>
                  <select
                    className="w-full border rounded-md p-1"
                    value={filters.duration}
                    onChange={(e) => handleFilterChange("duration", e.target.value)}
                  >
                    <option value="">Tất cả</option>
                    <option value="short">Dưới 1 giờ</option>
                    <option value="medium">1–3 giờ</option>
                    <option value="long">Trên 3 giờ</option>
                  </select>
                </div>
                <div>
                  <label className="block text-gray-600 mb-1">Nội dung</label>
                  <select
                    className="w-full border rounded-md p-1"
                    value={filters.topic}
                    onChange={(e) => handleFilterChange("topic", e.target.value)}
                  >
                    <option value="">Tất cả</option>
                    <option value="design">Thiết kế</option>
                    <option value="coding">Lập trình</option>
                    <option value="ai">AI</option>
                  </select>
                </div>
                <div>
                  <label className="block text-gray-600 mb-1">Mức độ</label>
                  <select
                    className="w-full border rounded-md p-1"
                    value={filters.level}
                    onChange={(e) => handleFilterChange("level", e.target.value)}
                  >
                    <option value="">Tất cả</option>
                    <option value="beginner">Cơ bản</option>
                    <option value="intermediate">Trung cấp</option>
                    <option value="advanced">Nâng cao</option>
                  </select>
                </div>
                <button className="mt-2 bg-secondary text-white rounded-md py-1.5" onClick={() => setShowFilter(false)}>
                  Áp dụng
                </button>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Description search area (kept simple) */}
      <section className="px-8 mt-10">
        <h2 className="text-lg font-semibold mb-1">Tìm kiếm thông qua mô tả</h2>
        <p className="text-xs text-gray-500 mb-4">Nhập mô tả các động tác ký hiệu để tìm từ phù hợp.</p>

        <textarea
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Nhập mô tả..."
          className="w-full h-40 border border-gray-300 rounded-lg p-3 text-sm bg-gray-100 resize-none"
        />
      </section>

      {/* Camera Section */}
      <section className="px-8 mt-14">
        <h2 className="text-lg font-semibold mb-1">Tìm kiếm thông qua ký hiệu</h2>
        <p className="text-xs text-gray-500 mb-4">Quay một video ngắn. Hệ thống sẽ cắt thành {SEQUENCE_LEN} frames và gửi lên server để xử lý.</p>

        <div className="flex justify-center">
          <div
            onClick={openCamera}
            className="bg-secondary hover:bg-[#c0dad5] rounded-lg w-[400px] h-[250px] flex items-center justify-center cursor-pointer transition-transform duration-300 hover:scale-105 shadow-md"
            role="button"
            aria-label="Mở camera"
          >
            {isLoadingCamera ? <div className="text-white text-sm">Đang mở camera...</div> : <CameraIcon size={64} />}
          </div>
        </div>
      </section>

      {/* Camera Popup */}
      {showPopup && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div className="absolute inset-0 bg-black bg-opacity-50" onClick={closeCamera} />

          <div className="relative bg-white rounded-xl p-4 shadow-xl w-[92%] max-w-lg mx-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold">Camera đang hoạt động</h3>
              <div className="flex items-center gap-3">
                <div className="text-sm text-gray-600">{isPredicting ? "Đang xử lý..." : recording ? "Đang ghi" : "Sẵn sàng"}</div>
                <button onClick={closeCamera} className="text-sm text-gray-600 hover:text-gray-900">Đóng</button>
              </div>
            </div>

            <div className="w-full bg-gray-100 rounded-md overflow-hidden relative">
              <video ref={videoRef} autoPlay playsInline muted className="w-full h-[360px] object-cover bg-black" />

              {/* Big result overlay (center) */}
              {prediction && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="bg-white/90 backdrop-blur-md px-6 py-4 rounded-2xl shadow-lg text-center max-w-[80%]">
                    <div className="text-2xl font-bold text-gray-900">{prediction.label}</div>
                    <div className="text-sm text-gray-600 mt-1">Confidence: {(prediction.confidence * 100).toFixed(1)}%</div>
                  </div>
                </div>
              )}

              {/* Small top-left status */}
              <div className="absolute top-3 left-3 bg-white/70 px-3 py-1 rounded text-sm font-semibold text-black">
                {prediction ? `${prediction.label} (${(prediction.confidence * 100).toFixed(0)}%)` : "—"}
              </div>

              {/* Progress bar + frames count */}
              <div className="absolute bottom-3 left-3 right-3">
                <div className="w-full bg-white/40 rounded-full h-2 overflow-hidden">
                  <div className="h-2 bg-green-500" style={{ width: `${Math.min(100, (frames.length / SEQUENCE_LEN) * 100)}%` }} />
                </div>
                <div className="text-xs text-white mt-1 text-right pr-1">{frames.length}/{SEQUENCE_LEN} frames</div>
              </div>
            </div>

            <div className="mt-3 grid grid-cols-4 gap-3 items-center">
              <button
                onClick={() => {
                  if (!videoRef.current) return;
                  const canvas = document.createElement("canvas");
                  canvas.width = videoRef.current.videoWidth || 640;
                  canvas.height = videoRef.current.videoHeight || 480;
                  const ctx = canvas.getContext("2d");
                  ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
                  const dataUrl = canvas.toDataURL("image/png");
                  const w = window.open("");
                  if (w) w.document.write(`<img src="${dataUrl}" alt="capture" />`);
                }}
                className="col-span-1 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-md text-sm"
              >
                Chụp ảnh
              </button>

              <button
                onClick={() => {
                  if (recording) stopRecording();
                  else startRecording();
                }}
                className={`col-span-2 ${recording ? "bg-yellow-600 hover:bg-yellow-700" : "bg-green-600 hover:bg-green-700"} text-white px-3 py-2 rounded-md text-sm`}
              >
                {recording ? "Dừng ghi" : `Bắt đầu ghi (${SEQUENCE_LEN} frames)`}
              </button>

              <button
                onClick={() => {
                  if (captureIntervalRef.current) {
                    clearInterval(captureIntervalRef.current);
                    captureIntervalRef.current = null;
                  }
                  setRecording(false);
                  setFrames([]);
                  setPrediction(null);
                  setHistory([]);
                }}
                className="col-span-1 bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-md text-sm"
              >
                Reset
              </button>
            </div>

            {/* Recent predictions history */}
            <div className="mt-3">
              <h4 className="text-sm font-medium mb-2">Lịch sử dự đoán gần đây</h4>
              <div className="flex gap-2 items-center">
                {history.length === 0 && <div className="text-xs text-gray-500">Chưa có kết quả</div>}
                {history.map((h, i) => (
                  <div key={i} className="bg-gray-50 border border-gray-200 rounded px-3 py-1 text-xs">
                    <div className="font-semibold">{h.label}</div>
                    <div className="text-gray-500 text-[11px]">{(h.confidence * 100).toFixed(0)}%</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-3 text-xs text-gray-600">
              Ghi chú: hệ thống sẽ thu khoảng {SEQUENCE_LEN} frames (ở ~{CAPTURE_FPS} fps) rồi gửi lên server để backend xử lý Mediapipe + ResNet. Nếu backend cần raw base64 (không có tiền tố data:), bật STRIP_DATAURL_PREFIX = true.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Search;
