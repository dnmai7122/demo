# Backend Setup & Testing Guide

## 🚀 Quick Start

### 1. Setup Virtual Environment (First Time Only)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test Database Connection
```bash
cd backend
source venv/bin/activate  # On macOS/Linux
python3 test_db.py
```

### 3. Start Backend Server
```bash
cd backend
source venv/bin/activate  # On macOS/Linux
python3 run_backend.py
```

The server will start at: `http://localhost:8000`

### 4. Test API Endpoints

Open another terminal and test:
```bash
# Test health check
curl http://localhost:8000/health

# Test topics endpoint
curl http://localhost:8000/api/topics
```

## 📋 Available Endpoints

- `GET /` - API documentation
- `GET /health` - Health check
- `GET /api/topics` - Get all topics
- `GET /api/products` - Get all products (legacy)

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError"
Make sure you activated the virtual environment:
```bash
source venv/bin/activate
```

### Error: "Connection refused"
Make sure backend server is running on port 8000

### Error: "Database error"
Check your `.env` file has correct Supabase credentials

## 🗄️ Database Schema

The `topic` table structure:
- `topic_id` (SERIAL PRIMARY KEY)
- `name` (TEXT) - Display name
- `code` (TEXT UNIQUE) - URL-friendly slug
- `level` (INTEGER) - Difficulty level
- `description` (TEXT)
- `cover_image_url` (TEXT)
- `cover_video_url` (TEXT)
- `order_index` (INTEGER)
- `is_active` (BOOLEAN)
