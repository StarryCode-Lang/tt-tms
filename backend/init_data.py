#!/usr/bin/env python3
"""
数据库初始化脚本 - 创建测试数据
"""
from app import create_app
from models import db, User, Campus


def init_test_data():
    app = create_app()
    with app.app_context():
        # 清空现有数据（可选）
        print("正在清理现有数据...")
        db.session.query(User).delete()
        db.session.query(Campus).delete()
        db.session.commit()

        # 创建校区
        print("创建校区...")
        campus1 = Campus(
            name="中心校区",
            address="北京市海淀区中关村大街1号",
            contact_person="张伟",
            phone="13812345678",
            email="zhangwei@center.com",
        )

        campus2 = Campus(
            name="分校区1",
            address="上海市浦东新区世纪大道2号",
            contact_person="李明",
            phone="13987654321",
            email="liming@branch1.com",
        )

        campus3 = Campus(
            name="分校区2",
            address="广州市天河区天河北路3号",
            contact_person="王芳",
            phone="13765432198",
            email="wangfang@branch2.com",
        )

        db.session.add_all([campus1, campus2, campus3])
        db.session.commit()

        # 创建超级管理员
        print("创建超级管理员...")
        super_admin = User(
            username="superadmin",
            name="赵强",
            gender="male",
            age=35,
            campus_id=campus1.id,
            phone="13655556666",
            email="zhaoqiang@super.com",
            role="super_admin",
        )
        super_admin.set_password("Admin123!")

        # 创建校区管理员
        print("创建校区管理员...")
        admin1 = User(
            username="admin_branch1",
            name="李明",
            gender="male",
            age=30,
            campus_id=campus2.id,
            phone="13987654321",
            email="liming@branch1.com",
            role="campus_admin",
        )
        admin1.set_password("Admin123!")

        admin2 = User(
            username="admin_branch2",
            name="王芳",
            gender="female",
            age=28,
            campus_id=campus3.id,
            phone="13765432198",
            email="wangfang@branch2.com",
            role="campus_admin",
        )
        admin2.set_password("Admin123!")

        # 创建学员
        print("创建学员...")
        student1 = User(
            username="student1",
            name="小明",
            gender="male",
            age=15,
            campus_id=campus1.id,
            phone="13899998888",
            email="xiaoming@center.com",
            role="student",
        )
        student1.set_password("Student123!")

        student2 = User(
            username="student2",
            name="小红",
            gender="female",
            age=16,
            campus_id=campus2.id,
            phone="13788889999",
            email="xiaohong@branch1.com",
            role="student",
        )
        student2.set_password("Student123!")

        student3 = User(
            username="student3",
            name="小刚",
            gender="male",
            age=14,
            campus_id=campus3.id,
            phone="13677778888",
            email="xiaogang@branch2.com",
            role="student",
        )
        student3.set_password("Student123!")

        # 创建教练
        print("创建教练...")
        coach1 = User(
            username="coach1",
            name="张教练",
            gender="male",
            age=40,
            campus_id=campus1.id,
            phone="13567891234",
            email="zhangjiaolian@center.com",
            role="coach",
            status="approved",  # 已审核通过
            level="senior",
            photo_url="http://example.com/coach1.jpg",
            achievements="全国冠军 2015, 亚军 2018",
        )
        coach1.set_password("Coach123!")

        coach2 = User(
            username="coach2",
            name="李教练",
            gender="female",
            age=35,
            campus_id=campus2.id,
            phone="13678912345",
            email="lijiaolian@branch1.com",
            role="coach",
            status="pending",  # 待审核
            photo_url="http://example.com/coach2.jpg",
            achievements="省冠军 2020",
        )
        coach2.set_password("Coach123!")

        # 保存所有用户
        db.session.add_all(
            [super_admin, admin1, admin2, student1, student2, student3, coach1, coach2]
        )
        db.session.commit()

        # 更新校区管理员
        campus1.admin_id = super_admin.id
        campus2.admin_id = admin1.id
        campus3.admin_id = admin2.id
        db.session.commit()

        print("✅ 测试数据初始化完成！")
        print("\n📋 测试账号：")
        print("超级管理员: superadmin / Admin123!")
        print("校区管理员: admin_branch1 / Admin123!")
        print("校区管理员: admin_branch2 / Admin123!")
        print("学员: student1 / Student123!")
        print("学员: student2 / Student123!")
        print("学员: student3 / Student123!")
        print("教练(已审核): coach1 / Coach123!")
        print("教练(待审核): coach2 / Coach123!")


if __name__ == "__main__":
    init_test_data()
