from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db
from routes import api
from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env 文件


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)
    app.register_blueprint(api, url_prefix="/api")

    @app.route("/")
    def index():
        return jsonify({"message": "TT-TMS API is running. Use /api for endpoints."})

    with app.app_context():
        db.create_all()  # 创建表
    return app
