import { useEffect, useState } from "react";
import supabase from "../config/supabaseClient";

function SupabaseTest() {
  const [connectionStatus, setConnectionStatus] = useState("Đang kiểm tra...");
  const [tables, setTables] = useState([]);
  const [error, setError] = useState(null);

  // Test kết nối
  useEffect(() => {
    const testConnection = async () => {
      try {
        // Kiểm tra kết nối bằng cách query đơn giản
        const { data, error } = await supabase
          .from("_test_connection")
          .select("*")
          .limit(1);

        if (error) {
          // Nếu bảng không tồn tại, đó vẫn là kết nối thành công
          if (
            error.code === "PGRST116" ||
            error.message.includes("does not exist")
          ) {
            setConnectionStatus("✅ Kết nối thành công!");
          } else {
            setConnectionStatus("❌ Kết nối thất bại");
            setError(error.message);
          }
        } else {
          setConnectionStatus("✅ Kết nối thành công!");
        }
      } catch (err) {
        setConnectionStatus("❌ Lỗi kết nối");
        setError(err.message);
      }
    };

    testConnection();
  }, []);

  // Tạo bảng mẫu
  const createSampleTable = async () => {
    try {
      // Tạo bảng 'signs' để lưu từ vựng ngôn ngữ ký hiệu
      const { data, error } = await supabase.from("signs").select("*").limit(1);

      if (error) {
        setError(`Bảng chưa tồn tại. Vui lòng tạo bảng trong Supabase Dashboard:\n
SQL Command:
CREATE TABLE signs (
  id BIGSERIAL PRIMARY KEY,
  word VARCHAR(255) NOT NULL,
  video_url TEXT,
  description TEXT,
  category VARCHAR(100),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);`);
      } else {
        alert('✅ Bảng "signs" đã tồn tại!');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  // Insert dữ liệu mẫu
  const insertSampleData = async () => {
    try {
      const { data, error } = await supabase
        .from("signs")
        .insert([
          {
            word: "Xin chào",
            description: "Cách chào hỏi cơ bản",
            category: "Chào hỏi",
          },
        ])
        .select();

      if (error) {
        setError(error.message);
        alert("❌ Lỗi: " + error.message);
      } else {
        alert("✅ Thêm dữ liệu thành công!");
        console.log("Data inserted:", data);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  // Đọc dữ liệu
  const fetchData = async () => {
    try {
      const { data, error } = await supabase.from("signs").select("*");

      if (error) {
        setError(error.message);
      } else {
        setTables(data);
        console.log("Data fetched:", data);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🔌 Supabase Connection Test</h1>

      <div style={{ marginBottom: "20px" }}>
        <h2>Trạng thái kết nối:</h2>
        <p style={{ fontSize: "18px", fontWeight: "bold" }}>
          {connectionStatus}
        </p>
      </div>

      {error && (
        <div
          style={{
            backgroundColor: "#ffebee",
            padding: "15px",
            borderRadius: "5px",
            marginBottom: "20px",
            whiteSpace: "pre-wrap",
          }}
        >
          <h3 style={{ color: "#c62828" }}>❌ Lỗi:</h3>
          <pre style={{ color: "#c62828" }}>{error}</pre>
        </div>
      )}

      <div style={{ marginBottom: "20px" }}>
        <h2>Thao tác:</h2>
        <button
          onClick={createSampleTable}
          style={{
            padding: "10px 20px",
            marginRight: "10px",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          📋 Kiểm tra bảng 'signs'
        </button>

        <button
          onClick={insertSampleData}
          style={{
            padding: "10px 20px",
            marginRight: "10px",
            backgroundColor: "#2196F3",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          ➕ Thêm dữ liệu mẫu
        </button>

        <button
          onClick={fetchData}
          style={{
            padding: "10px 20px",
            backgroundColor: "#FF9800",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          📖 Đọc dữ liệu
        </button>
      </div>

      {tables.length > 0 && (
        <div>
          <h2>📊 Dữ liệu trong bảng:</h2>
          <pre
            style={{
              backgroundColor: "#f5f5f5",
              padding: "15px",
              borderRadius: "5px",
              overflow: "auto",
            }}
          >
            {JSON.stringify(tables, null, 2)}
          </pre>
        </div>
      )}

      <div
        style={{
          marginTop: "30px",
          padding: "15px",
          backgroundColor: "#e3f2fd",
          borderRadius: "5px",
        }}
      >
        <h3>📝 Hướng dẫn tạo bảng trong Supabase:</h3>
        <ol>
          <li>
            Truy cập{" "}
            <a
              href="https://app.supabase.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              Supabase Dashboard
            </a>
          </li>
          <li>Chọn project của bạn</li>
          <li>
            Vào <strong>SQL Editor</strong>
          </li>
          <li>Copy và chạy câu lệnh SQL sau:</li>
        </ol>
        <pre
          style={{
            backgroundColor: "#263238",
            color: "#aed581",
            padding: "15px",
            borderRadius: "5px",
            overflow: "auto",
          }}
        >
          {`CREATE TABLE signs (
  id BIGSERIAL PRIMARY KEY,
  word VARCHAR(255) NOT NULL,
  video_url TEXT,
  description TEXT,
  category VARCHAR(100),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE signs ENABLE ROW LEVEL SECURITY;

-- Tạo policy cho phép đọc công khai
CREATE POLICY "Enable read access for all users" 
ON signs FOR SELECT 
USING (true);

-- Tạo policy cho phép insert cho authenticated users
CREATE POLICY "Enable insert for authenticated users only" 
ON signs FOR INSERT 
WITH CHECK (true);`}
        </pre>
      </div>
    </div>
  );
}

export default SupabaseTest;
