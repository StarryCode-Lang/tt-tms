from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymysql
import datetime
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

# 日志记录函数
def log_action(action, details=None):
    user_id = session.get('user_id')
    if user_id is None:
        return  # 如果没有用户 ID，不记录日志
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO logs (user_id, action, details, timestamp) VALUES (%s, %s, %s, NOW())"
            cursor.execute(sql, (user_id, action, details))
        conn.commit()
    finally:
        conn.close()

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
                log_action("Logged in", f"Username: {username}, Role: {role}")

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
    user_id = session.get('user_id')  # 在清除 session 前获取 user_id
    session.clear()
    if user_id:
        log_action("Logged out", f"User ID: {user_id}")
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
        log_action("Added campus", f"Name: {data['name']}, Address: {data['address']}")
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
            log_action("Edited campus", f"ID: {id}, Name: {data['name']}")
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
    log_action("Deleted campus", f"ID: {id}")
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
        log_action("Added user", f"Username: {data['username']}, Role: {data['role']}")
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
            log_action("Edited user", f"ID: {id}, Username: {data['username']}")
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
    log_action("Deleted user", f"ID: {id}")
    return redirect(url_for("user_management"))



# ---------- 课程预约 ----------
@app.route("/super_admin/appointments")
def appointments():
    if "role" not in session or session["role"] != "super_admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT a.id,
                       u_student.real_name AS student,
                       u_coach.real_name AS instructor,
                       a.start_time,
                       a.end_time,
                       a.status
                FROM appointments a
                LEFT JOIN users u_student ON a.student_id = u_student.id
                LEFT JOIN users u_coach ON a.coach_id = u_coach.id
                ORDER BY a.start_time DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

        # 格式化为模板需要的字段： id, student, instructor, time, status
        appointments = []
        for r in rows:
            st = r.get('start_time')
            et = r.get('end_time')
            if isinstance(st, datetime.datetime):
                st_str = st.strftime('%Y-%m-%d %H:%M')
            else:
                st_str = str(st) if st is not None else ''
            if isinstance(et, datetime.datetime):
                et_str = et.strftime('%Y-%m-%d %H:%M')
            else:
                et_str = str(et) if et is not None else ''
            appointments.append({
                "id": r.get("id"),
                "student": r.get("student") or "—",
                "instructor": r.get("instructor") or "—",
                "time": f"{st_str} - {et_str}",
                "status": r.get("status") or "—"
            })
        return render_template("appointments.html", appointments=appointments)
    finally:
        conn.close()

# ---------- 收费与退费 ----------
@app.route("/super_admin/transactions")
def transactions():
    if "role" not in session or session["role"] != "super_admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 注意 transactions 表中时间列是 `timestamp`
            sql = """
                SELECT t.id,
                       u.real_name AS user,
                       t.type,
                       t.amount,
                       t.timestamp AS ts
                FROM transactions t
                LEFT JOIN users u ON t.user_id = u.id
                ORDER BY t.timestamp DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

        transactions = []
        for r in rows:
            ts = r.get('ts')
            if isinstance(ts, datetime.datetime):
                date_str = ts.strftime('%Y-%m-%d %H:%M')
            else:
                date_str = str(ts) if ts is not None else ''
            transactions.append({
                "id": r.get("id"),
                "user": r.get("user") or "—",
                "type": r.get("type"),
                "amount": r.get("amount"),
                "date": date_str
            })
        return render_template("transactions.html", transactions=transactions)
    finally:
        conn.close()

# ---------- 月赛管理 ----------
@app.route("/super_admin/tournaments")
def tournaments():
    if "role" not in session or session["role"] != "super_admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # monthly_tournaments + match_registrations 汇总参赛人数
            sql = """
                SELECT mt.id, mt.year, mt.month, mt.date,
                       COUNT(mr.id) AS participants
                FROM monthly_tournaments mt
                LEFT JOIN match_registrations mr ON mt.id = mr.tournament_id
                GROUP BY mt.id, mt.year, mt.month, mt.date
                ORDER BY mt.year DESC, mt.month DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

        tournaments = []
        for r in rows:
            # 构造可读的赛事名称，例如：2025年9月月赛
            name = f"{r.get('year')}年{r.get('month')}月月赛"
            date_val = r.get('date')
            if isinstance(date_val, datetime.date):
                date_str = date_val.strftime('%Y-%m-%d')
            else:
                date_str = str(date_val) if date_val is not None else ''
            tournaments.append({
                "id": r.get("id"),
                "name": name,
                "date": date_str,
                "participants": r.get("participants", 0)
            })
        return render_template("tournaments.html", tournaments=tournaments)
    finally:
        conn.close()

# ---------- 系统消息 ----------
@app.route("/super_admin/messages")
def messages():
    if "role" not in session or session["role"] != "super_admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT m.id, m.content, m.receiver_id, u.real_name AS receiver, m.created_at
                FROM messages m
                LEFT JOIN users u ON m.receiver_id = u.id
                ORDER BY m.created_at DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

        messages = []
        for r in rows:
            created = r.get('created_at')
            if isinstance(created, datetime.datetime):
                date_str = created.strftime('%Y-%m-%d %H:%M')
            else:
                date_str = str(created) if created is not None else ''
            messages.append({
                "id": r.get("id"),
                "content": r.get("content"),
                "receiver": r.get("receiver") or ("用户ID " + str(r.get("receiver_id")) if r.get("receiver_id") else "系统"),
                "date": date_str
            })
        return render_template("messages.html", messages=messages)
    finally:
        conn.close()

# ---------- 系统日志 ----------
@app.route("/super_admin/logs")
def logs():
    if "role" not in session or session["role"] != "super_admin":
        return redirect(url_for("login_page"))

    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT l.id, l.user_id, u.real_name AS user, l.action, l.details, l.timestamp
                FROM logs l
                LEFT JOIN users u ON l.user_id = u.id
                ORDER BY l.timestamp DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

        logs = []
        for r in rows:
            ts = r.get('timestamp')
            if isinstance(ts, datetime.datetime):
                time_str = ts.strftime('%Y-%m-%d %H:%M')
            else:
                time_str = str(ts) if ts is not None else ''
            logs.append({
                "id": r.get("id"),
                "user": r.get("user") or ("用户ID " + str(r.get("user_id")) if r.get("user_id") else "系统"),
                "action": r.get("action"),
                "time": time_str
            })
        return render_template("logs.html", logs=logs)
    finally:
        conn.close()


# ========== 课程预约 CRUD ==========
@app.route("/super_admin/appointment/add", methods=["GET", "POST"])
def add_appointment():
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, real_name FROM users WHERE role='student'")
        students = cursor.fetchall()
        cursor.execute("SELECT id, real_name FROM users WHERE role='coach'")
        coaches = cursor.fetchall()

    if request.method == "POST":
        data = request.form
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO appointments (student_id, coach_id, start_time, end_time, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (data["student_id"], data["coach_id"], data["start_time"], data["end_time"], data["status"]))
        conn.commit()
        conn.close()
        log_action("Added appointment", f"Student ID: {data['student_id']}, Coach ID: {data['coach_id']}, Start Time: {data['start_time']}")
        return redirect(url_for("appointments"))

    conn.close()
    return render_template("appointment_form.html", appointment=None, students=students, coaches=coaches)

@app.route("/super_admin/appointment/delete/<int:id>")
def delete_appointment(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM appointments WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    log_action("Deleted appointment", f"ID: {id}")
    return redirect(url_for("appointments"))

# ========== 收费记录 CRUD ==========
@app.route("/super_admin/transaction/add", methods=["GET", "POST"])
def add_transaction():
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, real_name FROM users")
        users = cursor.fetchall()

    if request.method == "POST":
        data = request.form
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO transactions (user_id, type, amount, timestamp)
                VALUES (%s, %s, %s, NOW())
            """, (data["user_id"], data["type"], data["amount"]))

            if data["type"]=="refund":
                cursor.execute("""update users set balance=balance+%s where id=%s""", (data["amount"], data["user_id"]))
            elif data["type"]=="deposit":
                cursor.execute("""update users set balance=balance+%s where id=%s""", (data["amount"], data["user_id"]))
            elif data["type"]=="appointment_fee":
                cursor.execute("""update users set balance=balance-%s where id=%s""", (data["amount"], data["user_id"]))
            else:
                cursor.execute("""update users set balance=balance-%s where id=%s""", (data["amount"], data["user_id"]))
        conn.commit()
        conn.close()
        log_action("Added transaction", f"User ID: {data['user_id']}, Type: {data['type']}, Amount: {data['amount']}")
        return redirect(url_for("transactions"))

    conn.close()
    return render_template("transaction_form.html", transaction=None, users=users)

@app.route("/super_admin/transaction/delete/<int:id>")
def delete_transaction(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM transactions WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    log_action("Deleted transaction", f"ID: {id}")
    return redirect(url_for("transactions"))

# ========== 月赛 CRUD ==========
@app.route("/super_admin/tournament/add", methods=["GET", "POST"])
def add_tournament():
    if request.method == "POST":
        data = request.form
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO monthly_tournaments (year, month, date)
                VALUES (%s, %s, %s)
            """, (data["year"], data["month"], data["date"]))
        conn.commit()
        conn.close()
        log_action("Added tournament", f"Year: {data['year']}, Month: {data['month']}, Date: {data['date']}")
        return redirect(url_for("tournaments"))
    return render_template("tournament_form.html", tournament=None)

@app.route("/super_admin/tournament/delete/<int:id>")
def delete_tournament(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM monthly_tournaments WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    log_action("Deleted tournament", f"ID: {id}")
    return redirect(url_for("tournaments"))

# ========== 系统消息 CRUD ==========
@app.route("/super_admin/message/add", methods=["GET", "POST"])
def add_message():
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, real_name FROM users")
        users = cursor.fetchall()

    if request.method == "POST":
        data = request.form
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO messages (content, receiver_id, created_at)
                VALUES (%s, %s, NOW())
            """, (data["content"], data["receiver_id"]))
        conn.commit()
        conn.close()
        log_action("Added message", f"Receiver ID: {data['receiver_id']}, Content: {data['content'][:50]}...")  # 截取内容以避免过长
        return redirect(url_for("messages"))

    conn.close()
    return render_template("message_form.html", message=None, users=users)

@app.route("/super_admin/message/delete/<int:id>")
def delete_message(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM messages WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    log_action("Deleted message", f"ID: {id}")
    return redirect(url_for("messages"))


@app.route("/super_admin/appointment/edit/<int:id>", methods=["GET", "POST"])
def edit_appointment(id):
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, real_name FROM users WHERE role='student'")
        students = cursor.fetchall()
        cursor.execute("SELECT id, real_name FROM users WHERE role='coach'")
        coaches = cursor.fetchall()
        cursor.execute("SELECT * FROM appointments WHERE id=%s", (id,))
        appointment = cursor.fetchone()

    if request.method == "POST":
        data = request.form
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE appointments
                SET student_id=%s, coach_id=%s, start_time=%s, end_time=%s, status=%s
                WHERE id=%s
            """, (data["student_id"], data["coach_id"], data["start_time"], data["end_time"], data["status"], id))
        conn.commit()
        conn.close()
        log_action("Edited appointment", f"ID: {id}, Student ID: {data['student_id']}, Coach ID: {data['coach_id']}")
        return redirect(url_for("appointments"))

    conn.close()
    return render_template("appointment_form.html", appointment=appointment, students=students, coaches=coaches)


@app.route("/super_admin/transaction/edit/<int:id>", methods=["GET", "POST"])
def edit_transaction(id):
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, real_name FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM transactions WHERE id=%s", (id,))
        transaction = cursor.fetchone()

    if request.method == "POST":
        data = request.form
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE transactions
                SET user_id=%s, type=%s, amount=%s
                WHERE id=%s
            """, (data["user_id"], data["type"], data["amount"], id))
        conn.commit()
        conn.close()
        log_action("Edited transaction", f"ID: {id}, User ID: {data['user_id']}, Type: {data['type']}")
        return redirect(url_for("transactions"))

    conn.close()
    return render_template("transaction_form.html", transaction=transaction, users=users)


@app.route("/super_admin/tournament/edit/<int:id>", methods=["GET", "POST"])
def edit_tournament(id):
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM monthly_tournaments WHERE id=%s", (id,))
        tournament = cursor.fetchone()

    if request.method == "POST":
        data = request.form
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE monthly_tournaments
                SET year=%s, month=%s, date=%s
                WHERE id=%s
            """, (data["year"], data["month"], data["date"], id))
        conn.commit()
        conn.close()
        log_action("Edited tournament", f"ID: {id}, Year: {data['year']}, Month: {data['month']}")
        return redirect(url_for("tournaments"))

    conn.close()
    return render_template("tournament_form.html", tournament=tournament)


@app.route("/super_admin/message/edit/<int:id>", methods=["GET", "POST"])
def edit_message(id):
    conn = get_db_connection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, real_name FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM messages WHERE id=%s", (id,))
        message = cursor.fetchone()

    if request.method == "POST":
        data = request.form
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE messages
                SET content=%s, receiver_id=%s
                WHERE id=%s
            """, (data["content"], data["receiver_id"], id))
        conn.commit()
        conn.close()
        log_action("Edited message", f"ID: {id}, Receiver ID: {data['receiver_id']}")
        return redirect(url_for("messages"))

    conn.close()
    return render_template("message_form.html", message=message, users=users)





# ---------------------
# 主入口
# ---------------------
if __name__ == "__main__":
    app.run(debug=True)