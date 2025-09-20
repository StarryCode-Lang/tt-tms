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
                    return jsonify({"success": True, "redirect": url_for("super_admin_dashboard")})
                elif role == "student":
                    return jsonify({"success": True, "redirect": url_for("student_dashboard")})
                elif role=="campus_admin":
                    return jsonify({"success": True, "redirect": url_for("campus_admin_dashboard")})
                else:
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
# 学生后台首页
# ---------------------
@app.route("/student-dashboard")
def student_dashboard():
    if "role" in session and session["role"] == "student":
        return render_template("student_dashboard.html")
    else:
        return redirect(url_for("login_page"))

@app.route("/campus_admin-dashboard")
def campus_admin_dashboard():
    if "role" in session and session["role"] == "campus_admin":
        return render_template("campus_admin_dashboard.html")
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
# 校区管理
# ---------------------
@app.route("/super_admin/campus")
def campus_management():
    if "role" not in session or session["role"] != "super_admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM campuses")
            campuses = cursor.fetchall()
        return render_template("campus_management.html", campuses=campuses)
    finally:
        conn.close()

# ---------------------
# 用户管理
# ---------------------
@app.route("/super_admin/user")
def user_management():
    if "role" not in session or session["role"] != "super_admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT u.id, u.username, u.real_name, u.gender, u.age, 
                       u.phone, u.email, u.role, c.name AS campus_name
                FROM users u
                LEFT JOIN campuses c ON u.campus_id = c.id
            """
            cursor.execute(sql)
            users = cursor.fetchall()
        return render_template("user_management.html", users=users)
    finally:
        conn.close()

from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

# ========== 校区管理 ==========
@app.route("/super_admin/campus/add", methods=["GET", "POST"])
def add_campus():
    if request.method == "POST":
        data = request.form
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO campuses (name, address, contact_person, phone, email, is_center)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data["name"], data["address"], data["contact_person"], data["phone"], data["email"], data["is_center"]))
        conn.commit()
        conn.close()
        return redirect(url_for("campus_management"))
    return render_template("campus_form.html", campus=None)

@app.route("/super_admin/campus/edit/<int:id>", methods=["GET", "POST"])
def edit_campus(id):
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        if request.method == "POST":
            data = request.form
            cursor.execute("""
                UPDATE campuses SET name=%s, address=%s, contact_person=%s, phone=%s, email=%s, is_center=%s
                WHERE id=%s
            """, (data["name"], data["address"], data["contact_person"], data["phone"], data["email"], data["is_center"], id))
            conn.commit()
            conn.close()
            return redirect(url_for("campus_management"))
        cursor.execute("SELECT * FROM campuses WHERE id=%s", (id,))
        campus = cursor.fetchone()
    conn.close()
    return render_template("campus_form.html", campus=campus)

@app.route("/super_admin/campus/delete/<int:id>")
def delete_campus(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM campuses WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("campus_management"))


# ========== 用户管理 ==========
@app.route("/super_admin/user/add", methods=["GET", "POST"])
def add_user():
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM campuses")
        campuses = cursor.fetchall()

    if request.method == "POST":
        data = request.form
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, real_name, gender, age, phone, email, role, campus_id, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (data["username"], data["real_name"], data["gender"], data["age"], data["phone"], data["email"], data["role"], data["campus_id"], data["password"]))
        conn.commit()
        conn.close()
        return redirect(url_for("user_management"))

    conn.close()
    return render_template("user_form.html", user=None, campuses=campuses)

@app.route("/super_admin/user/edit/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM campuses")
        campuses = cursor.fetchall()
        if request.method == "POST":
            data = request.form
            cursor.execute("""
                UPDATE users SET username=%s, real_name=%s, gender=%s, age=%s, phone=%s, email=%s, role=%s, campus_id=%s, password=%s
                WHERE id=%s
            """, (data["username"], data["real_name"], data["gender"], data["age"], data["phone"], data["email"], data["role"], data["campus_id"], data["password"], id))
            conn.commit()
            conn.close()
            return redirect(url_for("user_management"))

        cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
        user = cursor.fetchone()
    conn.close()
    return render_template("user_form.html", user=user, campuses=campuses)

@app.route("/super_admin/user/delete/<int:id>")
def delete_user(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("user_management"))


# ---------------------
# 主入口
# ---------------------
if __name__ == "__main__":
    app.run(debug=True)