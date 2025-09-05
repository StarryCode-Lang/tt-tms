# 项目交接文档

## Sprint1 完成情况

### 已完成功能
- ✅ 校区管理系统 (半成品)
- ✅ 用户注册系统 (半成品)
- ✅ 登录认证系统 (半成品)
- ✅ 教练审核机制 (半成品)
- ✅ 个人信息维护 (半成品)
- ✅ 教练查询功能 (半成品)

### 技术实现要点
- **后端架构**: Flask + SQLAlchemy ORM
- **认证方式**: JWT token + Redis黑名单
- **数据库**: MySQL，包含 User 和 Campus 两个核心表
- **前端**: Vue3 + Element Plus UI组件库
- **状态管理**: Pinia 存储用户token和角色信息

### 代码结构说明
- `backend/models.py`: 数据模型定义
- `backend/routes.py`: API接口实现
- `frontend/src/router/index.js`: 前端路由配置
- `frontend/src/store/index.js`: 全局状态管理

## Sprint2 开发建议

### 优先级功能
0. **完善上述功能**
1. **双向选课系统** - 学员选择教练，教练确认学员
2. **预约管理** - 时间段预约，冲突检测
3. **支付功能** - 课程费用结算

### 技术建议
- 新增 Selection、Appointment、Payment 等数据模型
- 考虑使用消息队列处理异步通知
- 前端增加日历组件用于预约管理

## 环境配置
- MySQL数据库名: `tt_tms`
- 后端端口: 5000
- 前端端口: 5173
- Redis端口: 6379 (可选)

## 联系方式
如有问题请随时联系，建议先运行项目熟悉现有功能。
