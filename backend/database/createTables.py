import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Lấy thông tin từ .env
db_host = os.getenv("SUPABASE_DB_HOST")
db_name = os.getenv("SUPABASE_DB_NAME", "postgres")
db_user = os.getenv("SUPABASE_DB_USER")
db_password = os.getenv("SUPABASE_DB_PASSWORD")
db_port = os.getenv("SUPABASE_DB_PORT", "5432")

try:
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )
    
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS topic (
            topic_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            level INTEGER NOT NULL CHECK(level >= 0),
            description TEXT,
            cover_image_url TEXT,
            cover_video_url TEXT,
            order_index INTEGER NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS topic_prerequisite (
            topic_id INTEGER NOT NULL,
            prerequisite_topic_id INTEGER NOT NULL,
            UNIQUE (topic_id, prerequisite_topic_id),
            FOREIGN KEY (topic_id) REFERENCES topic(topic_id) ON DELETE CASCADE,
            FOREIGN KEY (prerequisite_topic_id) REFERENCES topic(topic_id) ON DELETE CASCADE
        );
    """)

# slug:Chuỗi định danh duy nhất, giúp tạo đường dẫn đẹp cho web app.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lesson (
            lesson_id SERIAL PRIMARY KEY,
            topic_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            order_index INTEGER NOT NULL,
            slug TEXT UNIQUE NOT NULL, 
            FOREIGN KEY (topic_id) REFERENCES topic(topic_id) ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS unit (
            unit_id SERIAL PRIMARY KEY,
            lesson_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('letter','digit','word','phrase','sentence','sign')),
            text TEXT NOT NULL,
            transcription TEXT,
            code TEXT UNIQUE NOT NULL,
            order_index INTEGER NOT NULL,
            image_url TEXT NOT NULL,    -- bắt buộc
            video_url TEXT NOT NULL,    -- bắt buộc
            FOREIGN KEY (lesson_id) REFERENCES lesson(lesson_id) ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_unit_progress (
            user_id INTEGER NOT NULL,
            unit_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('new','learning','mastered')),
            attempts INTEGER NOT NULL DEFAULT 0,
            last_seen_at TIMESTAMP,
            UNIQUE (user_id, unit_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (unit_id) REFERENCES unit(unit_id) ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_topic_progress (
            user_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('locked','in_progress','completed')),
            score REAL,
            completed_at TIMESTAMP,
            UNIQUE (user_id, topic_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (topic_id) REFERENCES topic(topic_id) ON DELETE CASCADE
        );
    """)

    # Indexes
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_lesson_topic ON lesson(topic_id);
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_unit_lesson ON unit(lesson_id);
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_prereq_topic ON topic_prerequisite(topic_id);
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_progress_topic ON user_topic_progress(user_id, topic_id);
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_progress_unit ON user_unit_progress(user_id, unit_id);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("✅ Đã tạo các bảng và indexes thành công")
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
