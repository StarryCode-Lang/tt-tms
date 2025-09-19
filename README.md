# 乒乓球培训管理系统

## 项目简介
乒乓球培训管理系统是一个基于 Flask 框架开发的 Web 应用程序，旨在管理学员、教练、校区管理员和超级管理员的登录、课程预约、收费管理等功能。

---

## 功能特性
- **用户登录**：支持学员、教练、校区管理员和超级管理员的登录。
- **超级管理员仪表盘**：
  - 校区管理
  - 用户管理
  - 课程预约
  - 收费与退费
  - 月赛管理
  - 系统消息
  - 系统日志
- **安全性**：基于 Flask 的 `session` 管理用户登录状态。
- **响应式设计**：支持桌面端和移动端访问。

---

## 技术栈
- **后端**：Flask (Python)
- **前端**：HTML, CSS, JavaScript
- **数据库**：MySQL
- **依赖库**：
  - `Flask`
  - `pymysql`
  - `werkzeug`

---

## 项目结构
项目根目录/ │ ├── app.py # 主应用程序文件 ├── templates/ # HTML 模板文件 │ ├── login.html # 登录页面 │ └── super_admin_dashboard.html # 超级管理员仪表盘页面 ├── static/ # 静态资源（CSS、JS、图片等） ├── requirements.txt # 项目依赖文件 └── README.md # 项目文档


---

## 安装与运行

### 环境要求
- Python 3.8+
- MySQL 数据库

### 安装步骤
1. 克隆项目到本地：
   ```bash
   git clone <项目仓库地址>
   cd <项目目录>
   创建虚拟环境并安装依赖：  
python -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
pip install -r requirements.txt
配置数据库：  
确保 MySQL 数据库已安装并运行。
创建名为 ttms_db 的数据库。
在 app.py 中修改 db_config 为你的数据库配置。
初始化数据库表：  
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'coach', 'campus_admin', 'super_admin') NOT NULL
);
运行项目：  
python app.py
打开浏览器访问：  
http://127.0.0.1:5000
<hr></hr>
使用说明
登录页面：  
选择用户类型（学员、教练、校区管理员、超级管理员）。
输入用户名和密码登录。
超级管理员仪表盘：  
通过左侧导航栏访问不同管理模块。
点击顶部右侧按钮可退出登录。
<hr></hr>
注意事项
默认超级管理员账户需手动插入数据库：
INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'super_admin');
请确保在生产环境中使用更安全的密码存储方式（如哈希加密）。
<hr></hr>
贡献
欢迎提交 Issue 或 Pull Request 来改进本项目。  <hr></hr>
许可证
本项目遵循 MIT 许可证。
