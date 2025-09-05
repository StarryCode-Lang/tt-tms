from app import create_app

app = create_app()
with app.app_context():
    print(" ✅ DB & Redis 连接正常" if app.extensions.get("sqlalchemy") else " ❌ 失败")
