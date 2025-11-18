import psycopg2
import os
from dotenv import load_dotenv

# === 1. Tải biến môi trường ===
load_dotenv()

# Lấy thông tin từ .env
db_host = os.getenv("SUPABASE_DB_HOST")
db_name = os.getenv("SUPABASE_DB_NAME", "postgres")
db_user = os.getenv("SUPABASE_DB_USER")
db_password = os.getenv("SUPABASE_DB_PASSWORD")
db_port = os.getenv("SUPABASE_DB_PORT", "5432")

try:
    # === 2. Kết nối database ===
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )
    
    cur = conn.cursor()
    
    # === 3. Lấy danh sách topic_id từ database ===
    cur.execute("SELECT topic_id, code FROM topic ORDER BY code")
    topics = cur.fetchall()
    
    if not topics:
        print("❌ Không tìm thấy topic nào trong database. Vui lòng chạy insertData.py trước.")
        cur.close()
        conn.close()
        exit()
    
    # Tạo map từ code sang topic_id
    topic_map = {code: topic_id for topic_id, code in topics}
    
    # === 4. Định nghĩa các điều kiện tiên quyết ===
    # Format: {"topic_code": ["prerequisite_code_1", "prerequisite_code_2", ...]}
    prerequisites = {
        "SD1": ["SD0"],                      # Để học SD1 (Số đếm nâng cao) phải hoàn thành SD0 (Số đếm cơ bản)
        "GT2": ["SD1", "BC", "CH", "BT", "GD"],  # Để học GT2 (Giới thiệu cơ bản) phải học SD1, BC, CH, BT, GD
        "HDS": ["BT", "GD", "MS"],           # Để học HDS (Hỏi đáp sở thích) phải học BT, GD, MS
        "HDN": ["BT", "NN"],                 # Để học HDN (Hỏi đáp nghề nghiệp) phải học BT, NN
    }
    
    # === 5. Chuẩn bị dữ liệu để insert ===
    prerequisite_data = []
    
    for topic_code, prereq_codes in prerequisites.items():
        if topic_code not in topic_map:
            continue
            
        topic_id = topic_map[topic_code]
        
        for prereq_code in prereq_codes:
            if prereq_code not in topic_map:
                continue
                
            prerequisite_topic_id = topic_map[prereq_code]
            prerequisite_data.append((topic_id, prerequisite_topic_id))
    
    # === 6. Xóa dữ liệu cũ (nếu có) ===
    cur.execute("DELETE FROM topic_prerequisite")
    
    # === 7. Insert dữ liệu mới ===
    if prerequisite_data:
        insert_query = """
            INSERT INTO topic_prerequisite (topic_id, prerequisite_topic_id)
            VALUES (%s, %s)
            ON CONFLICT (topic_id, prerequisite_topic_id) DO NOTHING
        """
        
        cur.executemany(insert_query, prerequisite_data)
        conn.commit()
        
        print(f"✅ Đã insert {len(prerequisite_data)} prerequisite thành công")
    else:
        print("⚠️  Không có prerequisite nào để insert")
    
    # === 8. Đóng kết nối ===
    cur.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"❌ Lỗi database: {e}")
    if conn:
        conn.rollback()
except Exception as e:
    print(f"❌ Lỗi: {e}")
finally:
    if 'cur' in locals() and cur:
        cur.close()
    if 'conn' in locals() and conn:
        conn.close()
