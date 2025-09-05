# TT-TMS: Table-tennis Training Management System

## 项目概述
基于 2025 软件工程课程设计需求开发的乒乓球培训管理系统，支持校区管理、用户注册登录、教练审核等功能。

**技术栈：**
- 后端：Flask + SQLAlchemy + JWT + Redis
- 前端：Vue3 + Vite + Element Plus + Pinia
- 数据库：MySQL 8.0+
- 开发环境：Win11 + VSCode

## 快速开始

### 环境要求
- Node.js v18+
- Python 3.10+
- MySQL 8.0+
- Redis (可选，用于token黑名单)

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd tt-tms
```

### 2. 后端设置
```bash
cd backend
pip install -r requirements.txt
# 创建数据库: CREATE DATABASE tt_tms CHARACTER SET utf8mb4;
# 如果有数据库备份文件: mysql -u root -p tt_tms < tt_tms_backup.sql
python run.py
```
后端运行在: http://localhost:5000

### 3. 前端设置
```bash
cd frontend
npm install
npm run dev
```
前端运行在: http://localhost:5173

## 当前进度 (Sprint1 已完成)

### 📋 API 接口
- `POST /api/register/student` - 学员注册
- `POST /api/register/coach` - 教练注册
- `POST /api/login` - 用户登录
- `GET /api/profile` - 获取个人信息
- `GET /api/campuses` - 获取校区列表
- `GET /api/admin/users` - 管理员查看所有用户
- `GET /api/coaches` - 学员查看教练列表

### 🗄️ 数据库结构
- `user` 表：用户信息 (学员/教练/管理员)
- `campus` 表：校区信息

### 🧪 测试数据
有两种方式初始化测试数据：

**方式1：导入数据库备份（快速）**
```bash
mysql -u root -p tt_tms < tt_tms_backup.sql
```

**方式2：运行Python脚本（推荐）**
```bash
cd backend
python init_data.py
```

### 🔑 测试账号
- 超级管理员：superadmin / Admin123!
- 校区管理员：admin_branch1 / Admin123!
- 学员：student1 / Student123!
- 教练(已审核)：coach1 / Coach123!
- 教练(待审核)：coach2 / Coach123!

## 开发说明

### 项目结构
```
tt-tms/
├── backend/          # Flask 后端
│   ├── app.py       # 应用工厂
│   ├── config.py    # 配置文件
│   ├── models.py    # 数据模型
│   ├── routes.py    # API 路由
│   └── run.py       # 启动脚本
├── frontend/         # Vue3 前端
│   ├── src/
│   │   ├── views/   # 页面组件
│   │   ├── router/  # 路由配置
│   │   └── store/   # 状态管理
│   └── package.json
└── README.md
```

### 配置说明
- 数据库配置：`backend/config.py`
- 前端代理配置：`frontend/vite.config.js`

## 已知问题
- 照片上传暂用 URL 字符串存储
- 支付功能未集成
- 消息通知系统待开发