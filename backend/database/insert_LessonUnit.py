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

# === 3. Lấy danh sách topic_id từ Supabase (để map với code) ===
print("🔁 Đang tải danh sách topic từ Supabase...")
response = supabase.table("topic").select("topic_id, code").execute()

if not hasattr(response, 'data') or not response.data:
    print("❌ Không thể tải danh sách topic. Đảm bảo bảng 'topic' đã có dữ liệu.")
    exit()

topic_map = {item['code']: item['topic_id'] for item in response.data}
print(f"✅ Đã lấy {len(topic_map)} topic")

# === 4. Dữ liệu lesson (nhiều lesson cho mỗi topic) ===
lessons = [
    # BC - 6 lessons
    {"topic_id": topic_map["BC"],  "title": "Bài 1: Bảng chữ cái",         "order_index": 1, "slug": "bc-bai-1"},
    {"topic_id": topic_map["BC"],  "title": "Bài 2: Bảng chữ cái",         "order_index": 2, "slug": "bc-bai-2"},
    {"topic_id": topic_map["BC"],  "title": "Bài 3: Bảng chữ cái",         "order_index": 3, "slug": "bc-bai-3"},
    {"topic_id": topic_map["BC"],  "title": "Bài 4: Bảng chữ cái",         "order_index": 4, "slug": "bc-bai-4"},
    {"topic_id": topic_map["BC"],  "title": "Bài 5: Bảng chữ cái",         "order_index": 5, "slug": "bc-bai-5"},
    {"topic_id": topic_map["BC"],  "title": "Bài 6: Bảng chữ cái",         "order_index": 6, "slug": "bc-bai-6"},
    
    # SD0 - 2 lessons
    {"topic_id": topic_map["SD0"], "title": "Bài 1: Số đếm cơ bản",        "order_index": 1, "slug": "sd0-bai-1"},
    {"topic_id": topic_map["SD0"], "title": "Bài 2: Số đếm cơ bản",        "order_index": 2, "slug": "sd0-bai-2"},
    
    # CH - 2 lessons
    {"topic_id": topic_map["CH"],  "title": "Bài 1: Chào hỏi",             "order_index": 1, "slug": "ch-bai-1"},
    {"topic_id": topic_map["CH"],  "title": "Bài 2: Chào hỏi",             "order_index": 2, "slug": "ch-bai-2"},
    
    # BT - 1 lesson
    {"topic_id": topic_map["BT"],  "title": "Bài 1: Bản thân",             "order_index": 1, "slug": "bt-bai-1"},
    
    # GD - 2 lessons
    {"topic_id": topic_map["GD"],  "title": "Bài 1: Gia đình",             "order_index": 1, "slug": "gd-bai-1"},
    {"topic_id": topic_map["GD"],  "title": "Bài 2: Gia đình",             "order_index": 2, "slug": "gd-bai-2"},
    
    # MS - 2 lessons
    {"topic_id": topic_map["MS"],  "title": "Bài 1: Màu sắc",              "order_index": 1, "slug": "ms-bai-1"},
    {"topic_id": topic_map["MS"],  "title": "Bài 2: Màu sắc",              "order_index": 2, "slug": "ms-bai-2"},
    
    # NN - 2 lessons
    {"topic_id": topic_map["NN"],  "title": "Bài 1: Nghề nghiệp",          "order_index": 1, "slug": "nn-bai-1"},
    {"topic_id": topic_map["NN"],  "title": "Bài 2: Nghề nghiệp",          "order_index": 2, "slug": "nn-bai-2"},
    
    # SD1 - 9 lessons
    {"topic_id": topic_map["SD1"], "title": "Bài 1: Số đếm nâng cao",      "order_index": 1, "slug": "sd1-bai-1"},
    {"topic_id": topic_map["SD1"], "title": "Bài 2: Số đếm nâng cao",      "order_index": 2, "slug": "sd1-bai-2"},
    {"topic_id": topic_map["SD1"], "title": "Bài 3: Số đếm nâng cao",      "order_index": 3, "slug": "sd1-bai-3"},
    {"topic_id": topic_map["SD1"], "title": "Bài 4: Số đếm nâng cao",      "order_index": 4, "slug": "sd1-bai-4"},
    {"topic_id": topic_map["SD1"], "title": "Bài 5: Số đếm nâng cao",      "order_index": 5, "slug": "sd1-bai-5"},
    {"topic_id": topic_map["SD1"], "title": "Bài 6: Số đếm nâng cao",      "order_index": 6, "slug": "sd1-bai-6"},
    {"topic_id": topic_map["SD1"], "title": "Bài 7: Số đếm nâng cao",      "order_index": 7, "slug": "sd1-bai-7"},
    {"topic_id": topic_map["SD1"], "title": "Bài 8: Số đếm nâng cao",      "order_index": 8, "slug": "sd1-bai-8"},
    {"topic_id": topic_map["SD1"], "title": "Bài 9: Số đếm nâng cao",      "order_index": 9, "slug": "sd1-bai-9"},
    
    # HDS - 1 lessons
    {"topic_id": topic_map["HDS"], "title": "Bài 1: Hỏi đáp sở thích",     "order_index": 1, "slug": "hds-bai-1"},
    
    # HDN - 1 lesson
    {"topic_id": topic_map["HDN"], "title": "Bài 1: Hỏi đáp nghề nghiệp",  "order_index": 1, "slug": "hdn-bai-1"},
    
    # GT2 - 2 lessons
    {"topic_id": topic_map["GT2"], "title": "Bài 1: Giới thiệu cơ bản",    "order_index": 1, "slug": "gt2-bai-1"},
    {"topic_id": topic_map["GT2"], "title": "Bài 2: Giới thiệu cơ bản",    "order_index": 2, "slug": "gt2-bai-2"},
]

# === 5. Chèn lesson vào bảng lesson ===
print("🔄 Chèn dữ liệu vào bảng lesson...")
lesson_map = {}  # {slug: lesson_id}
try:
    response = supabase.table("lesson").insert(lessons).execute()

    if hasattr(response, 'data') and response.data:
        for item in response.data:
            lesson_map[item['slug']] = item['lesson_id']
        print(f"✅ Đã chèn thành công {len(response.data)} lesson")
    else:
        print("❌ Không có dữ liệu trả về khi chèn lesson")
        exit()

except Exception as e:
    print(f"❌ Lỗi khi chèn lesson: {e}")
    exit()

# === 6. Dữ liệu unit – Chia đều cho các lesson ===
units = [
    # Bảng chữ cái (BC) - 32 units chia cho 6 lessons (5-6 units/lesson)
    # BC Bài 1 - 6 units
    {"lesson_id": lesson_map["bc-bai-1"], "type": "letter", "text": "Dấu ă",   "code": "BC_1_1", "order_index": 1, "image_url": "/media/letters/dau-a.png",  "video_url": "/media/letters/dau-a.mp4"},
    {"lesson_id": lesson_map["bc-bai-1"], "type": "letter", "text": "Dấu â",   "code": "BC_1_2", "order_index": 2, "image_url": "/media/letters/dau-aa.png", "video_url": "/media/letters/dau-aa.mp4"},
    {"lesson_id": lesson_map["bc-bai-1"], "type": "letter", "text": "Dấu móc", "code": "BC_1_3", "order_index": 3, "image_url": "/media/letters/dau-moc.png", "video_url": "/media/letters/dau-moc.mp4"},
    {"lesson_id": lesson_map["bc-bai-1"], "type": "letter", "text": "A",       "code": "BC_1_4", "order_index": 4, "image_url": "/media/letters/A.png",      "video_url": "/media/letters/A.mp4"},
    {"lesson_id": lesson_map["bc-bai-1"], "type": "letter", "text": "Ă",       "code": "BC_1_5", "order_index": 5, "image_url": "/media/letters/Ă.png",      "video_url": "/media/letters/Ă.mp4"},
    {"lesson_id": lesson_map["bc-bai-1"], "type": "letter", "text": "Â",       "code": "BC_1_6", "order_index": 6, "image_url": "/media/letters/Â.png",      "video_url": "/media/letters/Â.mp4"},
    
    # BC Bài 2 - 6 units
    {"lesson_id": lesson_map["bc-bai-2"], "type": "letter", "text": "B", "code": "BC_2_1", "order_index": 1, "image_url": "/media/letters/B.png", "video_url": "/media/letters/B.mp4"},
    {"lesson_id": lesson_map["bc-bai-2"], "type": "letter", "text": "C", "code": "BC_2_2", "order_index": 2, "image_url": "/media/letters/C.png", "video_url": "/media/letters/C.mp4"},
    {"lesson_id": lesson_map["bc-bai-2"], "type": "letter", "text": "D", "code": "BC_2_3", "order_index": 3, "image_url": "/media/letters/D.png", "video_url": "/media/letters/D.mp4"},
    {"lesson_id": lesson_map["bc-bai-2"], "type": "letter", "text": "Đ", "code": "BC_2_4", "order_index": 4, "image_url": "/media/letters/Đ.png", "video_url": "/media/letters/Đ.mp4"},
    {"lesson_id": lesson_map["bc-bai-2"], "type": "letter", "text": "E", "code": "BC_2_5", "order_index": 5, "image_url": "/media/letters/E.png", "video_url": "/media/letters/E.mp4"},
    {"lesson_id": lesson_map["bc-bai-2"], "type": "letter", "text": "Ê", "code": "BC_2_6", "order_index": 6, "image_url": "/media/letters/Ê.png", "video_url": "/media/letters/Ê.mp4"},
    
    # BC Bài 3 - 5 units
    {"lesson_id": lesson_map["bc-bai-3"], "type": "letter", "text": "G", "code": "BC_3_1", "order_index": 1, "image_url": "/media/letters/G.png", "video_url": "/media/letters/G.mp4"},
    {"lesson_id": lesson_map["bc-bai-3"], "type": "letter", "text": "H", "code": "BC_3_2", "order_index": 2, "image_url": "/media/letters/H.png", "video_url": "/media/letters/H.mp4"},
    {"lesson_id": lesson_map["bc-bai-3"], "type": "letter", "text": "I", "code": "BC_3_3", "order_index": 3, "image_url": "/media/letters/I.png", "video_url": "/media/letters/I.mp4"},
    {"lesson_id": lesson_map["bc-bai-3"], "type": "letter", "text": "K", "code": "BC_3_4", "order_index": 4, "image_url": "/media/letters/K.png", "video_url": "/media/letters/K.mp4"},
    {"lesson_id": lesson_map["bc-bai-3"], "type": "letter", "text": "L", "code": "BC_3_5", "order_index": 5, "image_url": "/media/letters/L.png", "video_url": "/media/letters/L.mp4"},
    
    # BC Bài 4 - 5 units
    {"lesson_id": lesson_map["bc-bai-4"], "type": "letter", "text": "M", "code": "BC_4_1", "order_index": 1, "image_url": "/media/letters/M.png", "video_url": "/media/letters/M.mp4"},
    {"lesson_id": lesson_map["bc-bai-4"], "type": "letter", "text": "N", "code": "BC_4_2", "order_index": 2, "image_url": "/media/letters/N.png", "video_url": "/media/letters/N.mp4"},
    {"lesson_id": lesson_map["bc-bai-4"], "type": "letter", "text": "O", "code": "BC_4_3", "order_index": 3, "image_url": "/media/letters/O.png", "video_url": "/media/letters/O.mp4"},
    {"lesson_id": lesson_map["bc-bai-4"], "type": "letter", "text": "Ô", "code": "BC_4_4", "order_index": 4, "image_url": "/media/letters/Ô.png", "video_url": "/media/letters/Ô.mp4"},
    {"lesson_id": lesson_map["bc-bai-4"], "type": "letter", "text": "Ơ", "code": "BC_4_5", "order_index": 5, "image_url": "/media/letters/Ơ.png", "video_url": "/media/letters/Ơ.mp4"},
    
    # BC Bài 5 - 5 units
    {"lesson_id": lesson_map["bc-bai-5"], "type": "letter", "text": "P", "code": "BC_5_1", "order_index": 1, "image_url": "/media/letters/P.png", "video_url": "/media/letters/P.mp4"},
    {"lesson_id": lesson_map["bc-bai-5"], "type": "letter", "text": "Q", "code": "BC_5_3", "order_index": 2, "image_url": "/media/letters/Q.png", "video_url": "/media/letters/Q.mp4"},
    {"lesson_id": lesson_map["bc-bai-5"], "type": "letter", "text": "R", "code": "BC_5_4", "order_index": 3, "image_url": "/media/letters/R.png", "video_url": "/media/letters/R.mp4"},
    {"lesson_id": lesson_map["bc-bai-5"], "type": "letter", "text": "S", "code": "BC_5_5", "order_index": 4, "image_url": "/media/letters/S.png", "video_url": "/media/letters/S.mp4"},
    {"lesson_id": lesson_map["bc-bai-6"], "type": "letter", "text": "T", "code": "BC_6_1", "order_index": 5, "image_url": "/media/letters/T.png", "video_url": "/media/letters/T.mp4"},
   
    # BC Bài 6 - 6 units
    {"lesson_id": lesson_map["bc-bai-6"], "type": "letter", "text": "U", "code": "BC_6_2", "order_index": 1, "image_url": "/media/letters/U.png", "video_url": "/media/letters/U.mp4"},
    {"lesson_id": lesson_map["bc-bai-6"], "type": "letter", "text": "Ư", "code": "BC_6_3", "order_index": 2, "image_url": "/media/letters/Ư.png", "video_url": "/media/letters/Ư.mp4"},
    {"lesson_id": lesson_map["bc-bai-6"], "type": "letter", "text": "V", "code": "BC_6_4", "order_index": 3, "image_url": "/media/letters/V.png", "video_url": "/media/letters/V.mp4"},
    {"lesson_id": lesson_map["bc-bai-6"], "type": "letter", "text": "X", "code": "BC_6_5", "order_index": 4, "image_url": "/media/letters/X.png", "video_url": "/media/letters/X.mp4"},
    {"lesson_id": lesson_map["bc-bai-6"], "type": "letter", "text": "Y", "code": "BC_6_6", "order_index": 5, "image_url": "/media/letters/Y.png", "video_url": "/media/letters/Y.mp4"},

    # Số đếm cơ bản (SD0) - 10 units chia cho 2 lessons (5 units/lesson)
    # SD0 Bài 1 - 5 units
    {"lesson_id": lesson_map["sd0-bai-1"], "type": "digit", "text": "0", "code": "SD0_1_1", "order_index": 1, "image_url": "/media/digits/0.png", "video_url": "/media/digits/0.mp4"},
    {"lesson_id": lesson_map["sd0-bai-1"], "type": "digit", "text": "1", "code": "SD0_1_2", "order_index": 2, "image_url": "/media/digits/1.png", "video_url": "/media/digits/1.mp4"},
    {"lesson_id": lesson_map["sd0-bai-1"], "type": "digit", "text": "2", "code": "SD0_1_3", "order_index": 3, "image_url": "/media/digits/2.png", "video_url": "/media/digits/2.mp4"},
    {"lesson_id": lesson_map["sd0-bai-1"], "type": "digit", "text": "3", "code": "SD0_1_4", "order_index": 4, "image_url": "/media/digits/3.png", "video_url": "/media/digits/3.mp4"},
    {"lesson_id": lesson_map["sd0-bai-1"], "type": "digit", "text": "4", "code": "SD0_1_5", "order_index": 5, "image_url": "/media/digits/4.png", "video_url": "/media/digits/4.mp4"},
    
    # SD0 Bài 2 - 5 units
    {"lesson_id": lesson_map["sd0-bai-2"], "type": "digit", "text": "5", "code": "SD0_2_1", "order_index": 1, "image_url": "/media/digits/5.png", "video_url": "/media/digits/5.mp4"},
    {"lesson_id": lesson_map["sd0-bai-2"], "type": "digit", "text": "6", "code": "SD0_2_2", "order_index": 2, "image_url": "/media/digits/6.png", "video_url": "/media/digits/6.mp4"},
    {"lesson_id": lesson_map["sd0-bai-2"], "type": "digit", "text": "7", "code": "SD0_2_3", "order_index": 3, "image_url": "/media/digits/7.png", "video_url": "/media/digits/7.mp4"},
    {"lesson_id": lesson_map["sd0-bai-2"], "type": "digit", "text": "8", "code": "SD0_2_4", "order_index": 4, "image_url": "/media/digits/8.png", "video_url": "/media/digits/8.mp4"},
    {"lesson_id": lesson_map["sd0-bai-2"], "type": "digit", "text": "9", "code": "SD0_2_5", "order_index": 5, "image_url": "/media/digits/9.png", "video_url": "/media/digits/9.mp4"},
    {"lesson_id": lesson_map["sd0-bai-2"], "type": "digit", "text": "10", "code": "SD0_2_6", "order_index": 6, "image_url": "/media/digits/10.png", "video_url": "/media/digits/10.mp4"},

    # Số đếm nâng cao (SD1) - 89 units (11-99) chia cho 9 lessons (~10 units/lesson)
    # SD1 Bài 1 - 10 units (11-20)
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "11", "code": "SD1_1_1", "order_index": 1, "image_url": "/media/digits/11.png", "video_url": "/media/digits/11.mp4"},
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "12", "code": "SD1_1_2", "order_index": 2, "image_url": "/media/digits/12.png", "video_url": "/media/digits/12.mp4"},
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "13", "code": "SD1_1_3", "order_index": 3, "image_url": "/media/digits/13.png", "video_url": "/media/digits/13.mp4"},
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "14", "code": "SD1_1_4", "order_index": 4, "image_url": "/media/digits/14.png", "video_url": "/media/digits/14.mp4"},
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "15", "code": "SD1_1_5", "order_index": 5, "image_url": "/media/digits/15.png", "video_url": "/media/digits/15.mp4"},
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "16", "code": "SD1_1_6", "order_index": 6, "image_url": "/media/digits/16.png", "video_url": "/media/digits/16.mp4"},
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "17", "code": "SD1_1_7", "order_index": 7, "image_url": "/media/digits/17.png", "video_url": "/media/digits/17.mp4"},
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "18", "code": "SD1_1_8", "order_index": 8, "image_url": "/media/digits/18.png", "video_url": "/media/digits/18.mp4"},
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "19", "code": "SD1_1_9", "order_index": 9, "image_url": "/media/digits/19.png", "video_url": "/media/digits/19.mp4"},
    {"lesson_id": lesson_map["sd1-bai-1"], "type": "digit", "text": "20", "code": "SD1_1_10", "order_index": 10, "image_url": "/media/digits/20.png", "video_url": "/media/digits/20.mp4"},
    
    # SD1 Bài 2 - 10 units (21-30)
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "21", "code": "SD1_2_1", "order_index": 1, "image_url": "/media/digits/21.png", "video_url": "/media/digits/21.mp4"},
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "22", "code": "SD1_2_2", "order_index": 2, "image_url": "/media/digits/22.png", "video_url": "/media/digits/22.mp4"},
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "23", "code": "SD1_2_3", "order_index": 3, "image_url": "/media/digits/23.png", "video_url": "/media/digits/23.mp4"},
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "24", "code": "SD1_2_4", "order_index": 4, "image_url": "/media/digits/24.png", "video_url": "/media/digits/24.mp4"},
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "25", "code": "SD1_2_5", "order_index": 5, "image_url": "/media/digits/25.png", "video_url": "/media/digits/25.mp4"},
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "26", "code": "SD1_2_6", "order_index": 6, "image_url": "/media/digits/26.png", "video_url": "/media/digits/26.mp4"},
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "27", "code": "SD1_2_7", "order_index": 7, "image_url": "/media/digits/27.png", "video_url": "/media/digits/27.mp4"},
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "28", "code": "SD1_2_8", "order_index": 8, "image_url": "/media/digits/28.png", "video_url": "/media/digits/28.mp4"},
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "29", "code": "SD1_2_9", "order_index": 9, "image_url": "/media/digits/29.png", "video_url": "/media/digits/29.mp4"},
    {"lesson_id": lesson_map["sd1-bai-2"], "type": "digit", "text": "30", "code": "SD1_2_10", "order_index": 10, "image_url": "/media/digits/30.png", "video_url": "/media/digits/30.mp4"},
    
    # SD1 Bài 3 - 10 units (31-40)
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "31", "code": "SD1_3_1", "order_index": 1, "image_url": "/media/digits/31.png", "video_url": "/media/digits/31.mp4"},
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "32", "code": "SD1_3_2", "order_index": 2, "image_url": "/media/digits/32.png", "video_url": "/media/digits/32.mp4"},
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "33", "code": "SD1_3_3", "order_index": 3, "image_url": "/media/digits/33.png", "video_url": "/media/digits/33.mp4"},
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "34", "code": "SD1_3_4", "order_index": 4, "image_url": "/media/digits/34.png", "video_url": "/media/digits/34.mp4"},
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "35", "code": "SD1_3_5", "order_index": 5, "image_url": "/media/digits/35.png", "video_url": "/media/digits/35.mp4"},
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "36", "code": "SD1_3_6", "order_index": 6, "image_url": "/media/digits/36.png", "video_url": "/media/digits/36.mp4"},
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "37", "code": "SD1_3_7", "order_index": 7, "image_url": "/media/digits/37.png", "video_url": "/media/digits/37.mp4"},
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "38", "code": "SD1_3_8", "order_index": 8, "image_url": "/media/digits/38.png", "video_url": "/media/digits/38.mp4"},
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "39", "code": "SD1_3_9", "order_index": 9, "image_url": "/media/digits/39.png", "video_url": "/media/digits/39.mp4"},
    {"lesson_id": lesson_map["sd1-bai-3"], "type": "digit", "text": "40", "code": "SD1_3_10", "order_index": 10, "image_url": "/media/digits/40.png", "video_url": "/media/digits/40.mp4"},
    
    # SD1 Bài 4 - 10 units (41-50)
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "41", "code": "SD1_4_1", "order_index": 1, "image_url": "/media/digits/41.png", "video_url": "/media/digits/41.mp4"},
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "42", "code": "SD1_4_2", "order_index": 2, "image_url": "/media/digits/42.png", "video_url": "/media/digits/42.mp4"},
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "43", "code": "SD1_4_3", "order_index": 3, "image_url": "/media/digits/43.png", "video_url": "/media/digits/43.mp4"},
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "44", "code": "SD1_4_4", "order_index": 4, "image_url": "/media/digits/44.png", "video_url": "/media/digits/44.mp4"},
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "45", "code": "SD1_4_5", "order_index": 5, "image_url": "/media/digits/45.png", "video_url": "/media/digits/45.mp4"},
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "46", "code": "SD1_4_6", "order_index": 6, "image_url": "/media/digits/46.png", "video_url": "/media/digits/46.mp4"},
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "47", "code": "SD1_4_7", "order_index": 7, "image_url": "/media/digits/47.png", "video_url": "/media/digits/47.mp4"},
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "48", "code": "SD1_4_8", "order_index": 8, "image_url": "/media/digits/48.png", "video_url": "/media/digits/48.mp4"},
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "49", "code": "SD1_4_9", "order_index": 9, "image_url": "/media/digits/49.png", "video_url": "/media/digits/49.mp4"},
    {"lesson_id": lesson_map["sd1-bai-4"], "type": "digit", "text": "50", "code": "SD1_4_10", "order_index": 10, "image_url": "/media/digits/50.png", "video_url": "/media/digits/50.mp4"},
    
    # SD1 Bài 5 - 10 units (51-60)
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "51", "code": "SD1_5_1", "order_index": 1, "image_url": "/media/digits/51.png", "video_url": "/media/digits/51.mp4"},
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "52", "code": "SD1_5_2", "order_index": 2, "image_url": "/media/digits/52.png", "video_url": "/media/digits/52.mp4"},
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "53", "code": "SD1_5_3", "order_index": 3, "image_url": "/media/digits/53.png", "video_url": "/media/digits/53.mp4"},
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "54", "code": "SD1_5_4", "order_index": 4, "image_url": "/media/digits/54.png", "video_url": "/media/digits/54.mp4"},
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "55", "code": "SD1_5_5", "order_index": 5, "image_url": "/media/digits/55.png", "video_url": "/media/digits/55.mp4"},
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "56", "code": "SD1_5_6", "order_index": 6, "image_url": "/media/digits/56.png", "video_url": "/media/digits/56.mp4"},
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "57", "code": "SD1_5_7", "order_index": 7, "image_url": "/media/digits/57.png", "video_url": "/media/digits/57.mp4"},
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "58", "code": "SD1_5_8", "order_index": 8, "image_url": "/media/digits/58.png", "video_url": "/media/digits/58.mp4"},
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "59", "code": "SD1_5_9", "order_index": 9, "image_url": "/media/digits/59.png", "video_url": "/media/digits/59.mp4"},
    {"lesson_id": lesson_map["sd1-bai-5"], "type": "digit", "text": "60", "code": "SD1_5_10", "order_index": 10, "image_url": "/media/digits/60.png", "video_url": "/media/digits/60.mp4"},
    
    # SD1 Bài 6 - 10 units (61-70)
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "61", "code": "SD1_6_1", "order_index": 1, "image_url": "/media/digits/61.png", "video_url": "/media/digits/61.mp4"},
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "62", "code": "SD1_6_2", "order_index": 2, "image_url": "/media/digits/62.png", "video_url": "/media/digits/62.mp4"},
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "63", "code": "SD1_6_3", "order_index": 3, "image_url": "/media/digits/63.png", "video_url": "/media/digits/63.mp4"},
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "64", "code": "SD1_6_4", "order_index": 4, "image_url": "/media/digits/64.png", "video_url": "/media/digits/64.mp4"},
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "65", "code": "SD1_6_5", "order_index": 5, "image_url": "/media/digits/65.png", "video_url": "/media/digits/65.mp4"},
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "66", "code": "SD1_6_6", "order_index": 6, "image_url": "/media/digits/66.png", "video_url": "/media/digits/66.mp4"},
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "67", "code": "SD1_6_7", "order_index": 7, "image_url": "/media/digits/67.png", "video_url": "/media/digits/67.mp4"},
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "68", "code": "SD1_6_8", "order_index": 8, "image_url": "/media/digits/68.png", "video_url": "/media/digits/68.mp4"},
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "69", "code": "SD1_6_9", "order_index": 9, "image_url": "/media/digits/69.png", "video_url": "/media/digits/69.mp4"},
    {"lesson_id": lesson_map["sd1-bai-6"], "type": "digit", "text": "70", "code": "SD1_6_10", "order_index": 10, "image_url": "/media/digits/70.png", "video_url": "/media/digits/70.mp4"},
    
    # SD1 Bài 7 - 10 units (71-80)
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "71", "code": "SD1_7_1", "order_index": 1, "image_url": "/media/digits/71.png", "video_url": "/media/digits/71.mp4"},
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "72", "code": "SD1_7_2", "order_index": 2, "image_url": "/media/digits/72.png", "video_url": "/media/digits/72.mp4"},
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "73", "code": "SD1_7_3", "order_index": 3, "image_url": "/media/digits/73.png", "video_url": "/media/digits/73.mp4"},
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "74", "code": "SD1_7_4", "order_index": 4, "image_url": "/media/digits/74.png", "video_url": "/media/digits/74.mp4"},
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "75", "code": "SD1_7_5", "order_index": 5, "image_url": "/media/digits/75.png", "video_url": "/media/digits/75.mp4"},
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "76", "code": "SD1_7_6", "order_index": 6, "image_url": "/media/digits/76.png", "video_url": "/media/digits/76.mp4"},
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "77", "code": "SD1_7_7", "order_index": 7, "image_url": "/media/digits/77.png", "video_url": "/media/digits/77.mp4"},
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "78", "code": "SD1_7_8", "order_index": 8, "image_url": "/media/digits/78.png", "video_url": "/media/digits/78.mp4"},
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "79", "code": "SD1_7_9", "order_index": 9, "image_url": "/media/digits/79.png", "video_url": "/media/digits/79.mp4"},
    {"lesson_id": lesson_map["sd1-bai-7"], "type": "digit", "text": "80", "code": "SD1_7_10", "order_index": 10, "image_url": "/media/digits/80.png", "video_url": "/media/digits/80.mp4"},
    
    # SD1 Bài 8 - 10 units (81-90)
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "81", "code": "SD1_8_1", "order_index": 1, "image_url": "/media/digits/81.png", "video_url": "/media/digits/81.mp4"},
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "82", "code": "SD1_8_2", "order_index": 2, "image_url": "/media/digits/82.png", "video_url": "/media/digits/82.mp4"},
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "83", "code": "SD1_8_3", "order_index": 3, "image_url": "/media/digits/83.png", "video_url": "/media/digits/83.mp4"},
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "84", "code": "SD1_8_4", "order_index": 4, "image_url": "/media/digits/84.png", "video_url": "/media/digits/84.mp4"},
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "85", "code": "SD1_8_5", "order_index": 5, "image_url": "/media/digits/85.png", "video_url": "/media/digits/85.mp4"},
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "86", "code": "SD1_8_6", "order_index": 6, "image_url": "/media/digits/86.png", "video_url": "/media/digits/86.mp4"},
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "87", "code": "SD1_8_7", "order_index": 7, "image_url": "/media/digits/87.png", "video_url": "/media/digits/87.mp4"},
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "88", "code": "SD1_8_8", "order_index": 8, "image_url": "/media/digits/88.png", "video_url": "/media/digits/88.mp4"},
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "89", "code": "SD1_8_9", "order_index": 9, "image_url": "/media/digits/89.png", "video_url": "/media/digits/89.mp4"},
    {"lesson_id": lesson_map["sd1-bai-8"], "type": "digit", "text": "90", "code": "SD1_8_10", "order_index": 10, "image_url": "/media/digits/90.png", "video_url": "/media/digits/90.mp4"},
    
    # SD1 Bài 9 - 9 units (91-99)
    {"lesson_id": lesson_map["sd1-bai-9"], "type": "digit", "text": "91", "code": "SD1_9_1", "order_index": 1, "image_url": "/media/digits/91.png", "video_url": "/media/digits/91.mp4"},
    {"lesson_id": lesson_map["sd1-bai-9"], "type": "digit", "text": "92", "code": "SD1_9_2", "order_index": 2, "image_url": "/media/digits/92.png", "video_url": "/media/digits/92.mp4"},
    {"lesson_id": lesson_map["sd1-bai-9"], "type": "digit", "text": "93", "code": "SD1_9_3", "order_index": 3, "image_url": "/media/digits/93.png", "video_url": "/media/digits/93.mp4"},
    {"lesson_id": lesson_map["sd1-bai-9"], "type": "digit", "text": "94", "code": "SD1_9_4", "order_index": 4, "image_url": "/media/digits/94.png", "video_url": "/media/digits/94.mp4"},
    {"lesson_id": lesson_map["sd1-bai-9"], "type": "digit", "text": "95", "code": "SD1_9_5", "order_index": 5, "image_url": "/media/digits/95.png", "video_url": "/media/digits/95.mp4"},
    {"lesson_id": lesson_map["sd1-bai-9"], "type": "digit", "text": "96", "code": "SD1_9_6", "order_index": 6, "image_url": "/media/digits/96.png", "video_url": "/media/digits/96.mp4"},
    {"lesson_id": lesson_map["sd1-bai-9"], "type": "digit", "text": "97", "code": "SD1_9_7", "order_index": 7, "image_url": "/media/digits/97.png", "video_url": "/media/digits/97.mp4"},
    {"lesson_id": lesson_map["sd1-bai-9"], "type": "digit", "text": "98", "code": "SD1_9_8", "order_index": 8, "image_url": "/media/digits/98.png", "video_url": "/media/digits/98.mp4"},
    {"lesson_id": lesson_map["sd1-bai-9"], "type": "digit", "text": "99", "code": "SD1_9_9", "order_index": 9, "image_url": "/media/digits/99.png", "video_url": "/media/digits/99.mp4"},

    # Chào hỏi (CH) - 8 units chia cho 2 lessons (4 units/lesson)
    # CH Bài 1 - 4 units
    {"lesson_id": lesson_map["ch-bai-1"], "type": "word", "text": "Xin chào", "code": "CH_1_1", "order_index": 1, "image_url": "/media/words/xin-chao.png", "video_url": "/media/words/xin-chao.mp4"},
    {"lesson_id": lesson_map["ch-bai-1"], "type": "word", "text": "Tạm biệt", "code": "CH_1_2", "order_index": 2, "image_url": "/media/words/tam-biet.png", "video_url": "/media/words/tam-biet.mp4"},
    {"lesson_id": lesson_map["ch-bai-1"], "type": "word", "text": "Xin lỗi", "code": "CH_1_3", "order_index": 3, "image_url": "/media/words/xin-loi.png", "video_url": "/media/words/xin-loi.mp4"},
    {"lesson_id": lesson_map["ch-bai-1"], "type": "word", "text": "Cảm ơn", "code": "CH_1_4", "order_index": 4, "image_url": "/media/words/cam-on.png", "video_url": "/media/words/cam-on.mp4"},
    
    # CH Bài 2 - 4 units
    {"lesson_id": lesson_map["ch-bai-2"], "type": "word", "text": "Chào buổi sáng", "code": "CH_2_1", "order_index": 1, "image_url": "/media/words/chao-buoi-sang.png", "video_url": "/media/words/chao-buoi-sang.mp4"},
    {"lesson_id": lesson_map["ch-bai-2"], "type": "word", "text": "Chào buổi trưa", "code": "CH_2_2", "order_index": 2, "image_url": "/media/words/chao-buoi-trua.png", "video_url": "/media/words/chao-buoi-trua.mp4"},
    {"lesson_id": lesson_map["ch-bai-2"], "type": "word", "text": "Chào buổi tối", "code": "CH_2_3", "order_index": 3, "image_url": "/media/words/chao-buoi-toi.png", "video_url": "/media/words/chao-buoi-toi.mp4"},
    {"lesson_id": lesson_map["ch-bai-2"], "type": "word", "text": "Chúc ngủ ngon", "code": "CH_2_4", "order_index": 4, "image_url": "/media/words/chuc-ngu-ngon.png", "video_url": "/media/words/chuc-ngu-ngon.mp4"},

    # Bản thân (BT) - 7 units cho 1 lesson
    # BT Bài 1 - 7 units
    {"lesson_id": lesson_map["bt-bai-1"], "type": "word", "text": "Tôi", "code": "BT_1_1", "order_index": 1, "image_url": "/media/words/toi.png", "video_url": "/media/words/toi.mp4"},
    {"lesson_id": lesson_map["bt-bai-1"], "type": "word", "text": "Bạn", "code": "BT_1_2", "order_index": 2, "image_url": "/media/words/ban.png", "video_url": "/media/words/ban.mp4"},
    {"lesson_id": lesson_map["bt-bai-1"], "type": "word", "text": "Của tôi", "code": "BT_1_3", "order_index": 3, "image_url": "/media/words/cua-toi.png", "video_url": "/media/words/cua-toi.mp4"},
    {"lesson_id": lesson_map["bt-bai-1"], "type": "word", "text": "Của bạn", "code": "BT_1_4", "order_index": 4, "image_url": "/media/words/cua-ban.png", "video_url": "/media/words/cua-ban.mp4"},
    {"lesson_id": lesson_map["bt-bai-1"], "type": "word", "text": "Tên", "code": "BT_1_5", "order_index": 5, "image_url": "/media/words/ten.png", "video_url": "/media/words/ten.mp4"},
    {"lesson_id": lesson_map["bt-bai-1"], "type": "word", "text": "Tên kí hiệu", "code": "BT_1_6", "order_index": 6, "image_url": "/media/words/ten-ki-hieu.png", "video_url": "/media/words/ten-ki-hieu.mp4"},
    {"lesson_id": lesson_map["bt-bai-1"], "type": "word", "text": "Tuổi", "code": "BT_1_7", "order_index": 7, "image_url": "/media/words/tuoi.png", "video_url": "/media/words/tuoi.mp4"},

    # Gia đình (GD) - 11 units chia cho 2 lessons (6+5 units)
    # GD Bài 1 - 6 units
    {"lesson_id": lesson_map["gd-bai-1"], "type": "word", "text": "Gia đình", "code": "GD_1_1", "order_index": 1, "image_url": "/media/words/gia-dinh.png", "video_url": "/media/words/gia-dinh.mp4"},
    {"lesson_id": lesson_map["gd-bai-1"], "type": "word", "text": "Ông", "code": "GD_1_2", "order_index": 2, "image_url": "/media/words/ong.png", "video_url": "/media/words/ong.mp4"},
    {"lesson_id": lesson_map["gd-bai-1"], "type": "word", "text": "Bà", "code": "GD_1_3", "order_index": 3, "image_url": "/media/words/ba.png", "video_url": "/media/words/ba.mp4"},
    {"lesson_id": lesson_map["gd-bai-1"], "type": "word", "text": "Ba", "code": "GD_1_4", "order_index": 4, "image_url": "/media/words/bo.png", "video_url": "/media/words/bo.mp4"},
    {"lesson_id": lesson_map["gd-bai-1"], "type": "word", "text": "Mẹ", "code": "GD_1_5", "order_index": 5, "image_url": "/media/words/me.png", "video_url": "/media/words/me.mp4"},
    
    # GD Bài 2 - 5 units
    {"lesson_id": lesson_map["gd-bai-2"], "type": "word", "text": "Vợ", "code": "GD_2_1", "order_index": 1, "image_url": "/media/words/vo.png", "video_url": "/media/words/vo.mp4"},
    {"lesson_id": lesson_map["gd-bai-2"], "type": "word", "text": "Chồng", "code": "GD_2_2", "order_index": 2, "image_url": "/media/words/chong.png", "video_url": "/media/words/chong.mp4"},
    {"lesson_id": lesson_map["gd-bai-2"], "type": "word", "text": "Em trai", "code": "GD_2_3", "order_index": 3, "image_url": "/media/words/em-trai.png", "video_url": "/media/words/em-trai.mp4"},
    {"lesson_id": lesson_map["gd-bai-2"], "type": "word", "text": "Em gái", "code": "GD_2_4", "order_index": 4, "image_url": "/media/words/em-gai.png", "video_url": "/media/words/em-gai.mp4"},
    {"lesson_id": lesson_map["gd-bai-2"], "type": "word", "text": "Anh trai", "code": "GD_2_5", "order_index": 5, "image_url": "/media/words/anh-trai.png", "video_url": "/media/words/anh-trai.mp4"},
    {"lesson_id": lesson_map["gd-bai-2"], "type": "word", "text": "Chị gái", "code": "GD_2_6", "order_index": 6, "image_url": "/media/words/chi-gai.png", "video_url": "/media/words/chi-gai.mp4"},

    # Màu sắc (MS) - 10 units chia cho 2 lessons (5 units/lesson)
    # MS Bài 1 - 5 units
    {"lesson_id": lesson_map["ms-bai-1"], "type": "word", "text": "Đỏ", "code": "MS_1_1", "order_index": 1, "image_url": "/media/words/do.png", "video_url": "/media/words/do.mp4"},
    {"lesson_id": lesson_map["ms-bai-1"], "type": "word", "text": "Xanh", "code": "MS_1_2", "order_index": 2, "image_url": "/media/words/xanh.png", "video_url": "/media/words/xanh.mp4"},
    {"lesson_id": lesson_map["ms-bai-1"], "type": "word", "text": "Vàng", "code": "MS_1_3", "order_index": 3, "image_url": "/media/words/vang.png", "video_url": "/media/words/vang.mp4"},
    {"lesson_id": lesson_map["ms-bai-1"], "type": "word", "text": "Tím", "code": "MS_1_4", "order_index": 4, "image_url": "/media/words/tim.png", "video_url": "/media/words/tim.mp4"},
    {"lesson_id": lesson_map["ms-bai-1"], "type": "word", "text": "Hồng", "code": "MS_1_5", "order_index": 5, "image_url": "/media/words/hong.png", "video_url": "/media/words/hong.mp4"},
    
    # MS Bài 2 - 5 units
    {"lesson_id": lesson_map["ms-bai-2"], "type": "word", "text": "Trắng", "code": "MS_2_1", "order_index": 1, "image_url": "/media/words/trang.png", "video_url": "/media/words/trang.mp4"},
    {"lesson_id": lesson_map["ms-bai-2"], "type": "word", "text": "Đen", "code": "MS_2_2", "order_index": 2, "image_url": "/media/words/den.png", "video_url": "/media/words/den.mp4"},
    {"lesson_id": lesson_map["ms-bai-2"], "type": "word", "text": "Cam", "code": "MS_2_3", "order_index": 3, "image_url": "/media/words/cam.png", "video_url": "/media/words/cam.mp4"},
    {"lesson_id": lesson_map["ms-bai-2"], "type": "word", "text": "Nâu", "code": "MS_2_4", "order_index": 4, "image_url": "/media/words/nau.png", "video_url": "/media/words/nau.mp4"},
    {"lesson_id": lesson_map["ms-bai-2"], "type": "word", "text": "Xám", "code": "MS_2_5", "order_index": 5, "image_url": "/media/words/xam.png", "video_url": "/media/words/xam.mp4"},

    # Nghề nghiệp (NN) - 8 units chia cho 2 lessons (4 units/lesson)
    # NN Bài 1 - 4 units
    {"lesson_id": lesson_map["nn-bai-1"], "type": "word", "text": "Giáo viên", "code": "NN_1_1", "order_index": 1, "image_url": "/media/words/giao-vien.png", "video_url": "/media/words/giao-vien.mp4"},
    {"lesson_id": lesson_map["nn-bai-1"], "type": "word", "text": "Công nhân", "code": "NN_1_2", "order_index": 2, "image_url": "/media/words/cong-nhan.png", "video_url": "/media/words/cong-nhan.mp4"},
    {"lesson_id": lesson_map["nn-bai-1"], "type": "word", "text": "Bác sĩ", "code": "NN_1_3", "order_index": 3, "image_url": "/media/words/bac-si.png", "video_url": "/media/words/bac-si.mp4"},
    {"lesson_id": lesson_map["nn-bai-1"], "type": "word", "text": "Công an", "code": "NN_1_4", "order_index": 4, "image_url": "/media/words/cong-an.png", "video_url": "/media/words/cong-an.mp4"},
    
    # NN Bài 2 - 4 units
    {"lesson_id": lesson_map["nn-bai-2"], "type": "word", "text": "Makeup", "code": "NN_2_1", "order_index": 1, "image_url": "/media/words/makeup.png", "video_url": "/media/words/makeup.mp4"},
    {"lesson_id": lesson_map["nn-bai-2"], "type": "word", "text": "Y tá", "code": "NN_2_2", "order_index": 2, "image_url": "/media/words/y-ta.png", "video_url": "/media/words/y-ta.mp4"},
    {"lesson_id": lesson_map["nn-bai-2"], "type": "word", "text": "Kỹ sư", "code": "NN_2_3", "order_index": 3, "image_url": "/media/words/ky-su.png", "video_url": "/media/words/ky-su.mp4"},
    {"lesson_id": lesson_map["nn-bai-2"], "type": "word", "text": "Phiên dịch", "code": "NN_2_4", "order_index": 4, "image_url": "/media/words/phien-dich.png", "video_url": "/media/words/phien-dich.mp4"},

    # Giới thiệu cơ bản (GT2) - 10 units chia cho 2 lessons (5 units/lesson)
    # GT2 Bài 1 - 5 units
    {"lesson_id": lesson_map["gt2-bai-1"], "type": "phrase", "text": "Bao nhiêu?", "code": "GT2_1_1", "order_index": 1, "image_url": "/media/phrases/bao-nhieu.png", "video_url": "/media/phrases/bao-nhieu.mp4"},
    {"lesson_id": lesson_map["gt2-bai-1"], "type": "phrase", "text": "Bạn tên gì?", "code": "GT2_1_2", "order_index": 2, "image_url": "/media/phrases/ban-ten-gi.png", "video_url": "/media/phrases/ban-ten-gi.mp4"},
    {"lesson_id": lesson_map["gt2-bai-1"], "type": "phrase", "text": "Tôi tên H-O-A", "code": "GT2_1_3", "order_index": 3, "image_url": "/media/phrases/toi-ten-hoa.png", "video_url": "/media/phrases/toi-ten-hoa.mp4"},
    {"lesson_id": lesson_map["gt2-bai-1"], "type": "phrase", "text": "Bạn bao nhiêu tuổi?", "code": "GT2_1_4", "order_index": 4, "image_url": "/media/phrases/ban-bao-nhieu-tuoi.png", "video_url": "/media/phrases/ban-bao-nhieu-tuoi.mp4"},
    {"lesson_id": lesson_map["gt2-bai-1"], "type": "phrase", "text": "Tôi 18 tuổi", "code": "GT2_1_5", "order_index": 5, "image_url": "/media/phrases/toi-18-tuoi.png", "video_url": "/media/phrases/toi-18-tuoi.mp4"},
    
    # GT2 Bài 2 - 5 units
    {"lesson_id": lesson_map["gt2-bai-2"], "type": "phrase", "text": "Gia đình bạn có bao nhiêu người?", "code": "GT2_2_1", "order_index": 1, "image_url": "/media/phrases/gia-dinh-ban-co-bao-nhieu-nguoi.png", "video_url": "/media/phrases/gia-dinh-ban-co-bao-nhieu-nguoi.mp4"},
    {"lesson_id": lesson_map["gt2-bai-2"], "type": "phrase", "text": "Gia đình tôi có 3 người", "code": "GT2_2_2", "order_index": 2, "image_url": "/media/phrases/gia-dinh-toi-co-3-nguoi.png", "video_url": "/media/phrases/gia-dinh-toi-co-3-nguoi.mp4"},
    {"lesson_id": lesson_map["gt2-bai-2"], "type": "phrase", "text": "Đó là ai?", "code": "GT2_2_3", "order_index": 3, "image_url": "/media/phrases/do-la-ai.png", "video_url": "/media/phrases/do-la-ai.mp4"},
    {"lesson_id": lesson_map["gt2-bai-2"], "type": "phrase", "text": "Ba, mẹ, tôi", "code": "GT2_2_4", "order_index": 4, "image_url": "/media/phrases/ba-me-toi.png", "video_url": "/media/phrases/ba-me-toi.mp4"},
    {"lesson_id": lesson_map["gt2-bai-2"], "type": "phrase", "text": "Còn bạn?", "code": "GT2_2_5", "order_index": 5, "image_url": "/media/phrases/con-ban.png", "video_url": "/media/phrases/con-ban.mp4"},

    # Hỏi đáp sở thích (HDS) - 7 units chia cho 2 lessons (4+3 units)
    # HDS Bài 1 - 4 units
    {"lesson_id": lesson_map["hds-bai-1"], "type": "phrase", "text": "Thích", "code": "HDS_1_1", "order_index": 1, "image_url": "/media/phrases/thich.png", "video_url": "/media/phrases/thich.mp4"},
    {"lesson_id": lesson_map["hds-bai-1"], "type": "phrase", "text": "Xin chào", "code": "HDS_1_2", "order_index": 2, "image_url": "/media/phrases/xin-chao-hds.png", "video_url": "/media/phrases/xin-chao-hds.mp4"},
    {"lesson_id": lesson_map["hds-bai-1"], "type": "phrase", "text": "Bạn thích màu gì?", "code": "HDS_1_3", "order_index": 3, "image_url": "/media/phrases/ban-thich-mau-gi.png", "video_url": "/media/phrases/ban-thich-mau-gi.mp4"},
    {"lesson_id": lesson_map["hds-bai-1"], "type": "phrase", "text": "Tôi thích màu trắng", "code": "HDS_1_4", "order_index": 4, "image_url": "/media/phrases/toi-thich-mau-trang.png", "video_url": "/media/phrases/toi-thich-mau-trang.mp4"},
    {"lesson_id": lesson_map["hds-bai-1"], "type": "phrase", "text": "Mẹ bạn thích màu gì?", "code": "HDS_1_5", "order_index": 5, "image_url": "/media/phrases/me-ban-thich-mau-gi.png", "video_url": "/media/phrases/me-ban-thich-mau-gi.mp4"},
    {"lesson_id": lesson_map["hds-bai-1"], "type": "phrase", "text": "Mẹ tôi thích màu đỏ", "code": "HDS_1_6", "order_index": 6, "image_url": "/media/phrases/me-toi-thich-mau-do.png", "video_url": "/media/phrases/me-toi-thich-mau-do.mp4"},

    # Hỏi đáp nghề nghiệp (HDN) - 5 units cho 1 lesson
    # HDN Bài 1 - 5 units
    {"lesson_id": lesson_map["hdn-bai-1"], "type": "phrase", "text": "Đúng không?", "code": "HDN_1_1", "order_index": 1, "image_url": "/media/phrases/dung-khong.png", "video_url": "/media/phrases/dung-khong.mp4"},
    {"lesson_id": lesson_map["hdn-bai-1"], "type": "phrase", "text": "Đúng", "code": "HDN_1_2", "order_index": 2, "image_url": "/media/phrases/dung.png", "video_url": "/media/phrases/dung.mp4"},
    {"lesson_id": lesson_map["hdn-bai-1"], "type": "phrase", "text": "Không", "code": "HDN_1_3", "order_index": 3, "image_url": "/media/phrases/khong.png", "video_url": "/media/phrases/khong.mp4"},
    {"lesson_id": lesson_map["hdn-bai-1"], "type": "phrase", "text": "Mẹ bạn là cô giáo đúng không?", "code": "HDN_1_4", "order_index": 4, "image_url": "/media/phrases/me-ban-la-co-giao-dung-khong.png", "video_url": "/media/phrases/me-ban-la-co-giao-dung-khong.mp4"},
    {"lesson_id": lesson_map["hdn-bai-1"], "type": "phrase", "text": "Bạn là giáo viên đúng không?", "code": "HDN_1_5", "order_index": 5, "image_url": "/media/phrases/ban-la-giao-vien-dung-khong.png", "video_url": "/media/phrases/ban-la-giao-vien-dung-khong.mp4"},

]

# === 7. Chèn unit vào bảng unit ===
print("🔄 Chèn dữ liệu vào bảng unit...")
try:
    response = supabase.table("unit").insert(units).execute()
    
    if hasattr(response, 'data') and response.data:
        print(f"✅ Đã chèn thành công {len(response.data)} unit")
    else:
        print("❌ Không có dữ liệu trả về khi chèn unit")
        
except Exception as e:
    print(f"❌ Lỗi khi chèn unit: {e}")
