from supabase import create_client
import os
from dotenv import load_dotenv

# === 1. Tải biến môi trường ===
load_dotenv()

supabase_url = os.getenv("REACT_APP_SUPABASE_URL")
supabase_key = os.getenv("REACT_APP_SUPABASE_ANON_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("❌ Thiếu REACT_APP_SUPABASE_URL hoặc REACT_APP_SUPABASE_ANON_KEY trong .env")

# === 2. Tạo client Supabase ===
supabase = create_client(supabase_url, supabase_key)

# === 3. Dữ liệu topic (11 topic từ file Excel) ===
topics = [
    {
        "name": "Bảng chữ cái",
        "code": "BC",
        "level": 0,
        "order_index": 1,
        "is_active": True
    },
    {
        "name": "Số đếm cơ bản",
        "code": "SD0",
        "level": 0,
        "order_index": 2,
        "is_active": True
    },
    {
        "name": "Chào hỏi",
        "code": "CH",
        "level": 0,
        "order_index": 3,
        "is_active": True
    },
    {
        "name": "Bản thân",
        "code": "BT",
        "level": 0,
        "order_index": 4,
        "is_active": True
    },
    {
        "name": "Gia đình",
        "code": "GD",
        "level": 0,
        "order_index": 5,
        "is_active": True
    },
    {
        "name": "Màu sắc",
        "code": "MS",
        "level": 0,
        "order_index": 6,
        "is_active": True
    },
    {
        "name": "Nghề nghiệp",
        "code": "NN",
        "level": 0,
        "order_index": 7,
        "is_active": True
    },
    {
        "name": "Số đếm nâng cao",
        "code": "SD1",
        "level": 1,
        "order_index": 8,
        "is_active": True
    },
    {
        "name": "Hỏi đáp sở thích",
        "code": "HDS",
        "level": 1,
        "order_index": 9,
        "is_active": True
    },
    {
        "name": "Hỏi đáp nghề nghiệp",
        "code": "HDN",
        "level": 1,
        "order_index": 10,
        "is_active": True
    },
    {
        "name": "Giới thiệu cơ bản",
        "code": "GT2",
        "level": 2,
        "order_index": 11,
        "is_active": True
    }
]

# === 4. Chèn dữ liệu vào bảng topic ===
try:
    response = supabase.table("topic").insert(topics).execute()
    
    # Kiểm tra phản hồi
    if hasattr(response, 'data') and response.data:
        print(f"✅ Đã chèn thành công {len(response.data)} topic vào bảng 'topic'")
    else:
        print("❌ Không nhận được dữ liệu trả về từ Supabase")

except Exception as e:
    print(f"❌ Lỗi khi chèn dữ liệu: {e}")
