# 乒乓球培训管理系统

## 项目简介

乒乓球培训管理系统是一个基于 Flask 框架开发的 Web 应用程序，面向学员、教练、校区管理员和超级管理员，提供课程预约、收费管理、用户管理等综合功能。

---

## 功能特性

- **用户登录**  
  支持学员、教练、校区管理员和超级管理员多角色登录。
- **超级管理员仪表盘**  
  - 校区管理  
  - 用户管理  
  - 课程预约  
  - 收费与退费  
  - 月赛管理  
  - 系统消息  
  - 系统日志
- **安全性**  
  基于 Flask 的 `session` 管理，保障用户登录状态。
- **响应式设计**  
  支持桌面端与移动端访问。

---

## 技术栈

- **后端**：Flask (Python)
- **前端**：HTML、CSS、JavaScript
- **数据库**：MySQL
- **主要依赖库**：
  - Flask
  - pymysql
  - werkzeug

---

## 项目结构

```
项目根目录/
├── app.py                       # 主应用程序文件
├── templates/                   # HTML 模板文件
│   ├── login.html               # 登录页面
│   └── super_admin_dashboard.html # 超级管理员仪表盘页面
├── static/                      # 静态资源（CSS、JS、图片等）
├── requirements.txt             # 项目依赖文件
└── README.md                    # 项目文档
```

---

## 安装与运行

### 环境要求

- Python 3.8 及以上
- MySQL 数据库

### 安装步骤

1. **克隆项目到本地**
   ```bash
   git clone <项目仓库地址>
   cd <项目目录>
   ```

2. **创建虚拟环境并安装依赖**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows 用户请使用 venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **配置数据库**
   - 确保 MySQL 已安装并运行
   - 创建数据库 `ttms_db`
   - 修改 `app.py` 中的 `db_config` 为你的数据库配置

4. **初始化数据库表**
   ```sql
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) NOT NULL,
       password VARCHAR(255) NOT NULL,
       role ENUM('student', 'coach', 'campus_admin', 'super_admin') NOT NULL
   );
   ```

5. **运行项目**
   ```bash
   python app.py
   ```
   浏览器访问：[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 使用说明

- 登录页面：选择用户类型（学员、教练、校区管理员、超级管理员），输入用户名和密码进行登录。
- 超级管理员仪表盘：通过左侧导航栏进入各管理模块，右上方按钮可退出登录。

---

## 注意事项

- 默认超级管理员账户需手动插入数据库：
  ```sql
  INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'super_admin');
  ```
- 生产环境请务必使用更安全的密码存储方式（如哈希加密）。

---

## 贡献

欢迎提交 Issue 或 Pull Request 改进本项目。

---

## 许可证

本项目遵循 [MIT 许可证](LICENSE)。
