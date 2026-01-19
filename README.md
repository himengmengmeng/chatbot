# 🤖 Chatbot API

<a href="#english">English</a> | <a href="#中文">中文</a>

---

<h2 id="english">📖 Overview</h2>

A smart chatbot backend API service built with **Django REST Framework**, integrated with **OpenAI GPT-4o** model, supporting multi-turn conversation management and user authentication.

## ✨ Key Features

- 🔐 **JWT Authentication** - Secure auth system based on Djoser + SimpleJWT
- 💬 **Multi-turn Conversation** - Create, query, and delete conversation sessions
- 🧠 **GPT-4o Integration** - Seamless OpenAI integration via LangChain
- 👤 **Custom User Model** - Extended Django user system with additional fields
- ⚡ **Redis Caching** - High-performance cache support
- 🔍 **Debug Tools** - Integrated Django Debug Toolbar and Silk profiler

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Framework | Django 4.2 + Django REST Framework 3.16 |
| Database | MySQL |
| Cache | Redis |
| Auth | JWT (djangorestframework-simplejwt) |
| AI | OpenAI GPT-4o + LangChain |
| Debug | Django Debug Toolbar + Silk |

## 📁 Project Structure

```
chatbot/
├── chat_app/           # Chat functionality module
│   ├── models.py       # Conversation and Message models
│   ├── views.py        # API views
│   ├── serializers.py  # Data serialization
│   └── urls.py         # Route configuration
├── core/               # Core module
│   ├── models.py       # Custom user model
│   └── serializers.py  # User serialization
├── root_directory/     # Project configuration
│   ├── settings.py     # Django settings
│   └── urls.py         # Main routes
├── manage.py
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MySQL 5.7+
- Redis 6.0+

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Create .env file
OPENAI_API_KEY=your_openai_api_key
```

5. **Configure database**
```bash
# Create database in MySQL
CREATE DATABASE root_directory CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Start the server**
```bash
python manage.py runserver
```

## 📡 API Endpoints

### Authentication API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/users/` | User registration |
| POST | `/auth/jwt/create/` | Obtain JWT Token |
| POST | `/auth/jwt/refresh/` | Refresh Token |
| GET | `/auth/users/me/` | Get current user info |

### Chat API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/conversations/` | List conversations |
| POST | `/api/conversations/` | Create new conversation |
| GET | `api/conversations/{id}/` | Get conversation details |
| DELETE | `api/conversations/{id}/` | Delete conversation |
| POST | `api/conversations/{id}/send_message/` | Send message and get AI response |

## 📝 Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "your_password"}'
```

### 2. Get Token
```bash
curl -X POST http://localhost:8000/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "your_password"}'
```

### 3. Create Conversation
```bash
curl -X POST http://localhost:8000/root_directory/api/conversations/ \
  -H "Authorization: JWT your_access_token"
```

### 4. Send Message
```bash
curl -X POST http://localhost:8000/root_directory/api/conversations/1/send_message/ \
  -H "Authorization: JWT your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, please introduce yourself"}'
```

## 🔧 Development Tools

- **Debug Toolbar**: http://localhost:8000/__debug__/
- **Silk Profiler**: http://localhost:8000/silk/
- **Django Admin**: http://localhost:8000/admin/

## 📄 License

MIT License

---

<h2 id="中文">📖 项目简介</h2>

<a href="#english">⬆️ Back to English</a>

这是一个基于 **Django REST Framework** 构建的智能聊天机器人后端 API 服务，集成了 **OpenAI GPT-4o** 模型，支持多轮对话管理和用户认证。

## ✨ 核心特性

- 🔐 **JWT 身份认证** - 基于 Djoser + SimpleJWT 的安全认证系统
- 💬 **多轮对话管理** - 支持创建、查询、删除对话会话
- 🧠 **GPT-4o 集成** - 使用 LangChain 无缝对接 OpenAI
- 👤 **自定义用户模型** - 扩展 Django 用户系统，支持额外字段
- ⚡ **Redis 缓存** - 高性能缓存支持
- 🔍 **调试工具** - 集成 Django Debug Toolbar 和 Silk 性能分析

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Django 4.2 + Django REST Framework 3.16 |
| 数据库 | MySQL |
| 缓存 | Redis |
| 认证 | JWT (djangorestframework-simplejwt) |
| AI | OpenAI GPT-4o + LangChain |
| 调试 | Django Debug Toolbar + Silk |

## 📁 项目结构

```
chatbot/
├── chat_app/           # 聊天功能模块
│   ├── models.py       # 对话和消息模型
│   ├── views.py        # API 视图
│   ├── serializers.py  # 数据序列化
│   └── urls.py         # 路由配置
├── core/               # 核心模块
│   ├── models.py       # 自定义用户模型
│   └── serializers.py  # 用户序列化
├── root_directory/     # 项目配置
│   ├── settings.py     # Django 设置
│   └── urls.py         # 主路由
├── manage.py
└── requirements.txt
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+
- Redis 6.0+

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd chatbot
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
# 创建 .env 文件
OPENAI_API_KEY=your_openai_api_key
```

5. **配置数据库**
```bash
# 在 MySQL 中创建数据库
CREATE DATABASE root_directory CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **运行迁移**
```bash
python manage.py migrate
```

7. **启动服务**
```bash
python manage.py runserver
```

## 📡 API 端点

### 认证 API

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/auth/users/` | 用户注册 |
| POST | `/auth/jwt/create/` | 获取 JWT Token |
| POST | `/auth/jwt/refresh/` | 刷新 Token |
| GET | `/auth/users/me/` | 获取当前用户信息 |

### 聊天 API

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/root_directory/api/conversations/` | 获取对话列表 |
| POST | `/root_directory/api/conversations/` | 创建新对话 |
| GET | `/root_directory/api/conversations/{id}/` | 获取对话详情 |
| DELETE | `/root_directory/api/conversations/{id}/` | 删除对话 |
| POST | `/root_directory/api/conversations/{id}/send_message/` | 发送消息并获取 AI 回复 |

## 📝 使用示例

### 1. 用户注册
```bash
curl -X POST http://localhost:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "your_password"}'
```

### 2. 获取 Token
```bash
curl -X POST http://localhost:8000/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "your_password"}'
```

### 3. 创建对话
```bash
curl -X POST http://localhost:8000/root_directory/api/conversations/ \
  -H "Authorization: JWT your_access_token"
```

### 4. 发送消息
```bash
curl -X POST http://localhost:8000/root_directory/api/conversations/1/send_message/ \
  -H "Authorization: JWT your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，请介绍一下你自己"}'
```

## 🔧 开发工具

- **Debug Toolbar**: http://localhost:8000/__debug__/
- **Silk 性能分析**: http://localhost:8000/silk/
- **Django Admin**: http://localhost:8000/admin/

## 📄 许可证

MIT License
