# Sign Language Database - MCP Server & FastAPI Backend

MCP Server và REST API để quản lý database sản phẩm thông qua Supabase PostgreSQL với kiến trúc module hóa.

## 🚀 Features

- **MCP Server**: Tích hợp với Claude Desktop và MCP Inspector
- **FastAPI Backend**: REST API chạy trên port 8000
- **Supabase Integration**: Kết nối PostgreSQL database
- **Shared Architecture**: Backend và MCP dùng chung business logic

## 📁 Cấu trúc thư mục

```
signlanguage/
├── database/                # Database setup scripts
│   ├── createTables.py
│   └── insertData.py
│
├── src/
│   ├── backend/            # 🌐 FastAPI REST API (Port 8000)
│   │   ├── main.py         # FastAPI application
│   │   ├── api/            # API routes (future)
│   │   ├── clients/        # API client examples
│   │   │   ├── api_client.py
│   │   │   ├── api_client.js
│   │   │   └── README.md
│   │   └── tests/          # Backend tests
│   │       └── test_backend.py
│   │
│   ├── mcp_server/         # 🤖 MCP Server (Claude Desktop)
│   │   ├── core/           # Server core
│   │   │   ├── config.py
│   │   │   └── server.py
│   │   ├── tools/          # MCP tools
│   │   │   ├── list_products.py
│   │   │   ├── get_product.py
│   │   │   ├── search_products.py
│   │   │   └── filter_products.py
│   │   ├── prompts/        # Pre-defined prompts
│   │   ├── resources/      # Static resources
│   │   └── tests/          # MCP tests
│   │
│   └── shared/             # 🔧 Shared utilities
│       ├── database.py     # DB connection manager
│       └── formatters.py   # Output formatters
│
├── run_backend.py          # Start FastAPI
├── run_mcp_inspector.py    # Start Inspector
└── run_server.py           # Start MCP Server
```


## 🔧 Cài đặt

### 1. Clone và setup môi trường

```bash
cd signlanguage

# Kích hoạt virtual environment (nếu có)
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình database

Tạo file `.env` trong thư mục gốc:

```env
# Supabase Database Connection
SUPABASE_DB_HOST=db.xxxxxxxxxxxxx.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password-here
SUPABASE_DB_PORT=5432

# Supabase API (optional, for React app)
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key-here
```

### 3. Tạo tables và insert dữ liệu

```bash
python database/createTables.py

python database/insertData.py
```


## 🏃 Chạy Server

### 1. Chạy FastAPI Backend (Port 8000)

```bash
python run_backend.py
```

API sẽ chạy tại:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 2. Chạy MCP Server với Inspector

```bash
npx @modelcontextprotocol/inspector python run_mcp_inspector.py
```

### 3. Chạy MCP Server trực tiếp (test mode)

```bash
python run_server.py
```

### 4. Cấu hình trong Claude Desktop

**MacOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sign-language-db": {
      "command": "python",
      "args": [
        "/Users/trinhtrantran/Documents/Sudo Code/SudoCode2025/database/signlanguage/run_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/trinhtrantran/Documents/Sudo Code/SudoCode2025/database/signlanguage",
        "PATH": "/Users/trinhtrantran/Documents/Sudo Code/SudoCode2025/database/signlanguage/venv/bin:/usr/bin:/bin"
      }
    }
  }
}
```

**Lưu ý:** Thay đường dẫn cho phù hợp với máy của bạn.

### 5. Cấu hình trong Cursor

Tạo file `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "sign-language-db": {
      "command": "python",
      "args": ["run_server.py"],
      "cwd": "/Users/trinhtrantran/Documents/Sudo Code/SudoCode2025/database/signlanguage"
    }
  }
}