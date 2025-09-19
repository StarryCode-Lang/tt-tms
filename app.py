from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymysql
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 用于 session 管理

# 数据库连接配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "ttms_db",
    "cursorclass": pymysql.cursors.DictCursor
}

# 获取数据库连接
def get_db_connection():
    return pymysql.connect(**db_config)

# ---------------------
# 登录页面
# ---------------------
@app.route("/")
def login_page():
    return render_template("login.html")

# ---------------------
# 登录逻辑
# ---------------------
@app.route("/login", methods=["POST"])
def login_action():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, username, password, role FROM users WHERE username=%s AND role=%s"
            cursor.execute(sql, (username, role))
            user = cursor.fetchone()

        if user:
            # 直接明文比对
            if user["password"] == password:
                session["user_id"] = user["id"]
                session["role"] = user["role"]

                if role == "super_admin":
                    print(1)
                    return jsonify({"success": True, "redirect": url_for("super_admin_dashboard")})
                else:
                    print(2)
                    return jsonify({"success": True, "redirect": f"/{role}-dashboard"})
            else:
                return jsonify({"success": False, "message": "密码错误"})
        else:
            return jsonify({"success": False, "message": "用户不存在"})
    finally:
        conn.close()

# ---------------------
# 超级管理员后台首页
# ---------------------
@app.route("/super_admin/dashboard")
def super_admin_dashboard():
    if "role" in session and session["role"] == "super_admin":
        return render_template("super_admin_dashboard.html")
    else:
        return redirect(url_for("login_page"))

# ---------------------
# 退出登录
# ---------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

# ---------------------
# 主入口
# ---------------------
if __name__ == "__main__":
    app.run(debug=True)
