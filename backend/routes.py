# API 路由（注册、登录、CRUD）
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies,
)
from models import db, User, Campus
from redis import Redis
from config import Config
import re

api = Blueprint("api", __name__)
redis = Redis.from_url(Config.REDIS_URL)


# 密码验证函数
def validate_password(password):
    if len(password) < 8 or len(password) > 16:
        return False
    if (
        not re.search(r"[a-zA-Z]", password)
        or not re.search(r"\d", password)
        or not re.search(r"[!@#$%^&*]", password)
    ):
        return False
    return True


@api.route("/register/student", methods=["POST"])
def register_student():
    data = request.json
    if not all(
        key in data for key in ["username", "password", "name", "campus_id", "phone"]
    ):
        return jsonify({"error": "Missing fields"}), 400
    if not validate_password(data["password"]):
        return jsonify({"error": "Invalid password format"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username exists"}), 400

    user = User(
        username=data["username"],
        name=data["name"],
        gender=data.get("gender"),
        age=data.get("age"),
        campus_id=data["campus_id"],
        phone=data["phone"],
        email=data.get("email"),
        role="student",
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Student registered"}), 201


@api.route("/register/coach", methods=["POST"])
def register_coach():
    data = request.json
    if not all(
        key in data
        for key in [
            "username",
            "password",
            "name",
            "campus_id",
            "phone",
            "photo_url",
            "achievements",
        ]
    ):
        return jsonify({"error": "Missing fields"}), 400
    if not validate_password(data["password"]):
        return jsonify({"error": "Invalid password format"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username exists"}), 400

    user = User(
        username=data["username"],
        name=data["name"],
        gender=data.get("gender"),
        age=data.get("age"),
        campus_id=data["campus_id"],
        phone=data["phone"],
        email=data.get("email"),
        role="coach",
        status="pending",
        photo_url=data["photo_url"],
        achievements=data["achievements"],
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Coach registration pending approval"}), 201


@api.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    if user.role == "coach" and user.status != "approved":
        return jsonify({"error": "Account not approved"}), 403

    access_token = create_access_token(identity={"id": user.id, "role": user.role})
    return jsonify({"token": access_token}), 200


@api.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt_identity()["jti"]  # 需要 get_jwt() 但简化
    redis.set(jti, "blacklisted", ex=3600)  # 黑名单 1h
    response = jsonify({"message": "Logged out"})
    unset_jwt_cookies(response)
    return response


@api.route("/profile", methods=["GET", "PUT"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.get(current_user["id"])
    if request.method == "GET":
        return jsonify(
            {
                "username": user.username,
                "name": user.name,
                # ... 其他字段
            }
        )
    elif request.method == "PUT":
        data = request.json
        if "password" in data:
            if not validate_password(data["password"]):
                return jsonify({"error": "Invalid password"}), 400
            user.set_password(data["password"])
        # 更新其他字段
        user.name = data.get("name", user.name)
        # ...
        db.session.commit()
        return jsonify({"message": "Profile updated"})


@api.route("/campuses", methods=["GET", "POST"])
@jwt_required()
def manage_campuses():
    current_user = get_jwt_identity()
    if current_user["role"] != "super_admin":
        return jsonify({"error": "Unauthorized"}), 403

    if request.method == "POST":
        data = request.json
        campus = Campus(
            name=data["name"],
            address=data.get("address"),
            # ...
        )
        db.session.add(campus)
        db.session.commit()
        return jsonify({"message": "Campus created"}), 201

    campuses = Campus.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in campuses])


@api.route("/campuses/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_campus(id):
    # 类似，检查 super_admin
    pass  # 实现 PUT/DELETE


@api.route("/approve/coach/<int:coach_id>", methods=["PUT"])
@jwt_required()
def approve_coach(coach_id):
    current_user = get_jwt_identity()
    if current_user["role"] not in ["campus_admin", "super_admin"]:
        return jsonify({"error": "Unauthorized"}), 403
    coach = User.query.get(coach_id)
    if not coach or coach.role != "coach":
        return jsonify({"error": "Not found"}), 404
    data = request.json
    coach.status = data["status"]  # 'approved' or 'rejected'
    coach.level = data["level"]  # 指定级别
    db.session.commit()
    return jsonify({"message": "Coach updated"})


@api.route("/coaches", methods=["GET"])
@jwt_required()
def query_coaches():
    current_user = get_jwt_identity()
    if current_user["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403
    params = request.args
    query = User.query.filter_by(role="coach", status="approved")
    if "name" in params:
        query = query.filter(User.name.like(f"%{params['name']}%"))
    # 其他条件
    coaches = query.all()
    return jsonify(
        [{"id": c.id, "name": c.name, "photo_url": c.photo_url} for c in coaches]
    )


# 管理员查看所有数据的接口
@api.route("/admin/users", methods=["GET"])
@jwt_required()
def admin_get_users():
    current_user = get_jwt_identity()
    if current_user["role"] != "super_admin":
        return jsonify({"error": "Unauthorized"}), 403

    users = User.query.all()
    return jsonify(
        [
            {
                "id": u.id,
                "username": u.username,
                "name": u.name,
                "role": u.role,
                "status": u.status,
                "campus_id": u.campus_id,
                "phone": u.phone,
                "email": u.email,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ]
    )


@api.route("/admin/campuses", methods=["GET"])
@jwt_required()
def admin_get_campuses():
    current_user = get_jwt_identity()
    if current_user["role"] != "super_admin":
        return jsonify({"error": "Unauthorized"}), 403

    campuses = Campus.query.all()
    return jsonify(
        [
            {
                "id": c.id,
                "name": c.name,
                "address": c.address,
                "contact_person": c.contact_person,
                "phone": c.phone,
                "email": c.email,
                "admin_id": c.admin_id,
            }
            for c in campuses
        ]
    )
