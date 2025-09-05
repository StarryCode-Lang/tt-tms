# 配置文件（DB、JWT、Redis）
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a8c9761238a55581bddd352b93f149f5"
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost:3306/tt_tms"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = (
        os.environ.get("JWT_SECRET_KEY") or "a8c9761238a55581bddd352b93f149f5"
    )
    REDIS_URL = "redis://localhost:6379/0"  # Redis 连接
