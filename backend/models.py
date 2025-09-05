# SQLAlchemy 模型（User, Campus）
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 校区管理员


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum("male", "female", "other"))
    age = db.Column(db.Integer)
    campus_id = db.Column(db.Integer, db.ForeignKey("campus.id"), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    role = db.Column(
        db.Enum("super_admin", "campus_admin", "coach", "student"), nullable=False
    )
    status = db.Column(
        db.Enum("pending", "approved", "rejected"), default="approved"
    )  # 对于教练
    level = db.Column(db.Enum("senior", "mid", "junior"))  # 教练级别
    photo_url = db.Column(db.String(255))  # 教练照片
    achievements = db.Column(db.Text)  # 教练成绩
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
