/*
 Navicat Premium Dump SQL

 Source Server         : DBprogramDesign
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : localhost:3306
 Source Schema         : ttms_db

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 23/09/2025 22:52:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for appointments
-- ----------------------------
DROP TABLE IF EXISTS `appointments`;
CREATE TABLE `appointments`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `coach_id` int NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `table_number` int NULL DEFAULT NULL,
  `status` enum('pending','confirmed','cancelled','completed') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending',
  `payment_amount` decimal(10, 2) NULL DEFAULT 0.00,
  `paid` tinyint(1) NULL DEFAULT 0,
  `cancelled_by` enum('student','coach','none') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'none',
  `cancel_confirmed_by_student` tinyint(1) NULL DEFAULT 0,
  `cancel_confirmed_by_coach` tinyint(1) NULL DEFAULT 0,
  `cancel_timestamp` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `duration_minutes` int GENERATED ALWAYS AS (timestampdiff(MINUTE,`start_time`,`end_time`)) STORED NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `student_id`(`student_id` ASC) USING BTREE,
  INDEX `coach_id`(`coach_id` ASC) USING BTREE,
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`coach_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of appointments
-- ----------------------------
INSERT INTO `appointments` VALUES (1, 5, 3, '2025-09-20 10:00:00', '2025-09-20 11:00:00', 1, 'confirmed', 200.00, 1, 'none', 0, 0, NULL, '2025-09-19 10:32:18', '2025-09-19 10:32:18', DEFAULT);
INSERT INTO `appointments` VALUES (2, 6, 4, '2025-09-21 15:00:00', '2025-09-21 16:30:00', 2, 'pending', 120.00, 0, 'none', 0, 0, NULL, '2025-09-19 10:32:18', '2025-09-19 10:32:18', DEFAULT);

-- ----------------------------
-- Table structure for campuses
-- ----------------------------
DROP TABLE IF EXISTS `campuses`;
CREATE TABLE `campuses`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_person` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `manager_id` int NULL DEFAULT NULL,
  `is_center` tinyint(1) NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_name`(`name` ASC) USING BTREE,
  INDEX `manager_id`(`manager_id` ASC) USING BTREE,
  CONSTRAINT `campuses_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of campuses
-- ----------------------------
INSERT INTO `campuses` VALUES (1, '中心校区', '北京市海淀区中关村大街100号', '张主任', '010-88888888', 'center@ttms.com', NULL, 1, '2025-09-19 10:32:18', '2025-09-19 10:32:18');
INSERT INTO `campuses` VALUES (2, '东部分校区', '北京市朝阳区建国路88号', '李老师', '010-66666666', 'east@ttms.com', NULL, 0, '2025-09-19 10:32:18', '2025-09-19 10:32:18');
INSERT INTO `campuses` VALUES (5, '南岭校区', '吉林省长春市朝阳区前进大街2699号吉林大学南岭', '还海华', '574563435', '435432@123.com', NULL, 0, '2025-09-20 10:29:07', '2025-09-20 11:13:45');
INSERT INTO `campuses` VALUES (10, '南湖校区', '我也不知道具体位置在哪吉林大学南湖', '苏嫣然', '171475', '43a2@123.com', NULL, 0, '2025-09-20 11:14:23', '2025-09-20 11:14:23');
INSERT INTO `campuses` VALUES (11, '新民校区', '我不到啊', '张主任', '010-88888888', 'center@ttms.com', NULL, 0, '2025-09-20 11:49:39', '2025-09-20 11:49:39');

-- ----------------------------
-- Table structure for cancel_history
-- ----------------------------
DROP TABLE IF EXISTS `cancel_history`;
CREATE TABLE `cancel_history`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `appointment_id` int NULL DEFAULT NULL,
  `month` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `cancel_date` date NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_cancel`(`user_id` ASC, `appointment_id` ASC) USING BTREE,
  INDEX `appointment_id`(`appointment_id` ASC) USING BTREE,
  CONSTRAINT `cancel_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `cancel_history_ibfk_2` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cancel_history
-- ----------------------------
INSERT INTO `cancel_history` VALUES (1, 5, 1, '2025-09', '2025-09-18');

-- ----------------------------
-- Table structure for coach_change_requests
-- ----------------------------
DROP TABLE IF EXISTS `coach_change_requests`;
CREATE TABLE `coach_change_requests`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `current_coach_id` int NULL DEFAULT NULL,
  `new_coach_id` int NOT NULL,
  `status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending',
  `approved_by_current` tinyint(1) NULL DEFAULT 0,
  `approved_by_new` tinyint(1) NULL DEFAULT 0,
  `approved_by_admin` tinyint(1) NULL DEFAULT 0,
  `rejected_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `requested_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `student_id`(`student_id` ASC) USING BTREE,
  INDEX `current_coach_id`(`current_coach_id` ASC) USING BTREE,
  INDEX `new_coach_id`(`new_coach_id` ASC) USING BTREE,
  CONSTRAINT `coach_change_requests_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `coach_change_requests_ibfk_2` FOREIGN KEY (`current_coach_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `coach_change_requests_ibfk_3` FOREIGN KEY (`new_coach_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of coach_change_requests
-- ----------------------------
INSERT INTO `coach_change_requests` VALUES (1, 5, 3, 4, 'pending', 0, 0, 0, NULL, '2025-09-19 10:32:18');

-- ----------------------------
-- Table structure for evaluations
-- ----------------------------
DROP TABLE IF EXISTS `evaluations`;
CREATE TABLE `evaluations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `appointment_id` int NOT NULL,
  `student_feedback` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `coach_feedback` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_eval_per_appointment`(`appointment_id` ASC) USING BTREE,
  CONSTRAINT `evaluations_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of evaluations
-- ----------------------------
INSERT INTO `evaluations` VALUES (1, 1, '学到了正手攻球技术', '张三进步很大，需要加强反手练习', '2025-09-19 10:32:18');

-- ----------------------------
-- Table structure for licenses
-- ----------------------------
DROP TABLE IF EXISTS `licenses`;
CREATE TABLE `licenses`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `super_admin_id` int NOT NULL,
  `license_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `device_identifier` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `paid_until` date NOT NULL,
  `amount` decimal(10, 2) NULL DEFAULT 500.00,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `license_key`(`license_key` ASC) USING BTREE,
  INDEX `super_admin_id`(`super_admin_id` ASC) USING BTREE,
  CONSTRAINT `licenses_ibfk_1` FOREIGN KEY (`super_admin_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of licenses
-- ----------------------------
INSERT INTO `licenses` VALUES (1, 1, 'ABC123-XYZ789', 'DEVICE001', '2026-09-01', 500.00, '2025-09-19 10:32:18');

-- ----------------------------
-- Table structure for logs
-- ----------------------------
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `action` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `details` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of logs
-- ----------------------------
INSERT INTO `logs` VALUES (1, 5, 'book_appointment', '张三预约了王强的课程', '2025-09-19 10:32:18');
INSERT INTO `logs` VALUES (2, 3, 'confirm_appointment', '王强确认了张三的预约', '2025-09-19 10:32:18');
INSERT INTO `logs` VALUES (3, 1, 'Logged in', 'Username: admin, Role: super_admin', '2025-09-22 21:28:23');
INSERT INTO `logs` VALUES (4, 1, 'Added transaction', 'User ID: 6, Type: deposit, Amount: 500', '2025-09-22 21:28:33');
INSERT INTO `logs` VALUES (5, 1, 'Logged in', 'Username: admin, Role: super_admin', '2025-09-23 17:24:27');
INSERT INTO `logs` VALUES (6, 1, 'Added user', 'Username: aaaaa, Role: student', '2025-09-23 17:25:45');
INSERT INTO `logs` VALUES (7, 1, 'Logged in', 'Username: admin, Role: super_admin', '2025-09-23 21:58:37');
INSERT INTO `logs` VALUES (8, 1, 'Deleted user', 'ID: 7', '2025-09-23 21:58:50');
INSERT INTO `logs` VALUES (9, 1, 'Added user', 'Username: 炸鸡块, Role: student', '2025-09-23 22:02:07');
INSERT INTO `logs` VALUES (10, 1, 'Deleted user', 'ID: 8', '2025-09-23 22:02:11');
INSERT INTO `logs` VALUES (11, 1, 'Added user', 'Username: 炸鸡块, Role: campus_admin', '2025-09-23 22:02:17');
INSERT INTO `logs` VALUES (12, 1, 'Deleted user', 'ID: 9', '2025-09-23 22:02:26');
INSERT INTO `logs` VALUES (13, 1, 'Added user', 'Username: 炸鸡块, Role: coach', '2025-09-23 22:07:51');
INSERT INTO `logs` VALUES (14, 1, 'Added user', 'Username: wudi, Role: super_admin', '2025-09-23 22:09:20');
INSERT INTO `logs` VALUES (15, 1, 'Deleted user', 'ID: 10', '2025-09-23 22:18:38');
INSERT INTO `logs` VALUES (16, 1, 'Added user', 'Username: 炸鸡块, Role: coach', '2025-09-23 22:21:48');
INSERT INTO `logs` VALUES (17, 1, 'Added user', 'Username: witness, Role: super_admin', '2025-09-23 22:22:17');
INSERT INTO `logs` VALUES (18, 1, 'Deleted user', 'ID: 11', '2025-09-23 22:22:47');
INSERT INTO `logs` VALUES (19, 1, 'Added tournament', 'Year: 2024, Month: 10, Date: 2025-09-06', '2025-09-23 22:36:32');
INSERT INTO `logs` VALUES (20, 1, 'Added appointment', 'Student ID: 5, Coach ID: 3, Start Time: 2025-09-04T20:46', '2025-09-23 22:47:07');
INSERT INTO `logs` VALUES (21, 1, 'Deleted appointment', 'ID: 3', '2025-09-23 22:48:00');

-- ----------------------------
-- Table structure for match_registrations
-- ----------------------------
DROP TABLE IF EXISTS `match_registrations`;
CREATE TABLE `match_registrations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `tournament_id` int NOT NULL,
  `group_type` enum('A','B','C') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `paid` tinyint(1) NULL DEFAULT 0,
  `registration_fee` decimal(10, 2) NULL DEFAULT 30.00,
  `registered_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_registration`(`student_id` ASC, `tournament_id` ASC) USING BTREE,
  INDEX `tournament_id`(`tournament_id` ASC) USING BTREE,
  CONSTRAINT `match_registrations_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `match_registrations_ibfk_2` FOREIGN KEY (`tournament_id`) REFERENCES `monthly_tournaments` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of match_registrations
-- ----------------------------
INSERT INTO `match_registrations` VALUES (1, 5, 1, 'A', 1, 30.00, '2025-09-19 10:32:18');
INSERT INTO `match_registrations` VALUES (2, 6, 1, 'B', 1, 30.00, '2025-09-19 10:32:18');

-- ----------------------------
-- Table structure for match_schedules
-- ----------------------------
DROP TABLE IF EXISTS `match_schedules`;
CREATE TABLE `match_schedules`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tournament_id` int NOT NULL,
  `group_type` enum('A','B','C') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `round_num` int NOT NULL,
  `player1_id` int NOT NULL,
  `player2_id` int NULL DEFAULT NULL,
  `table_number` int NULL DEFAULT NULL,
  `scheduled_time` datetime NULL DEFAULT NULL,
  `status` enum('scheduled','completed','bye') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'scheduled',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tournament_id`(`tournament_id` ASC) USING BTREE,
  INDEX `player1_id`(`player1_id` ASC) USING BTREE,
  INDEX `player2_id`(`player2_id` ASC) USING BTREE,
  CONSTRAINT `match_schedules_ibfk_1` FOREIGN KEY (`tournament_id`) REFERENCES `monthly_tournaments` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `match_schedules_ibfk_2` FOREIGN KEY (`player1_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `match_schedules_ibfk_3` FOREIGN KEY (`player2_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of match_schedules
-- ----------------------------
INSERT INTO `match_schedules` VALUES (1, 1, 'A', 1, 5, NULL, 1, '2025-09-28 09:00:00', 'scheduled', '2025-09-19 10:32:18');

-- ----------------------------
-- Table structure for messages
-- ----------------------------
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NULL DEFAULT NULL,
  `receiver_id` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` enum('approval_request','cancel_request','reminder','notification','change_coach') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `related_id` int NULL DEFAULT NULL,
  `is_read` tinyint(1) NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sender_id`(`sender_id` ASC) USING BTREE,
  INDEX `receiver_id`(`receiver_id` ASC) USING BTREE,
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of messages
-- ----------------------------
INSERT INTO `messages` VALUES (1, 3, 5, '你的预约已确认', 'reminder', NULL, 0, '2025-09-19 10:32:18');
INSERT INTO `messages` VALUES (2, 4, 6, '你的预约正在等待确认', 'notification', NULL, 0, '2025-09-19 10:32:18');

-- ----------------------------
-- Table structure for monthly_tournaments
-- ----------------------------
DROP TABLE IF EXISTS `monthly_tournaments`;
CREATE TABLE `monthly_tournaments`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int NOT NULL,
  `month` int NOT NULL,
  `date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_tournament`(`year` ASC, `month` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of monthly_tournaments
-- ----------------------------
INSERT INTO `monthly_tournaments` VALUES (1, 2025, 9, '2025-09-28', '2025-09-19 10:32:18');
INSERT INTO `monthly_tournaments` VALUES (3, 2024, 10, '2025-09-06', '2025-09-23 22:36:32');

-- ----------------------------
-- Table structure for student_coach_relations
-- ----------------------------
DROP TABLE IF EXISTS `student_coach_relations`;
CREATE TABLE `student_coach_relations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `coach_id` int NOT NULL,
  `status` enum('applied','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'applied',
  `applied_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `approved_at` timestamp NULL DEFAULT NULL,
  `rejected_at` timestamp NULL DEFAULT NULL,
  `rejected_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_student_coach`(`student_id` ASC, `coach_id` ASC) USING BTREE,
  INDEX `coach_id`(`coach_id` ASC) USING BTREE,
  CONSTRAINT `student_coach_relations_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `student_coach_relations_ibfk_2` FOREIGN KEY (`coach_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_coach_relations
-- ----------------------------
INSERT INTO `student_coach_relations` VALUES (1, 5, 3, 'approved', '2025-09-19 10:32:18', NULL, NULL, NULL, '2025-09-19 10:32:18');
INSERT INTO `student_coach_relations` VALUES (2, 6, 4, 'approved', '2025-09-19 10:32:18', NULL, NULL, NULL, '2025-09-19 10:32:18');

-- ----------------------------
-- Table structure for transactions
-- ----------------------------
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `amount` decimal(10, 2) NOT NULL,
  `type` enum('deposit','appointment_fee','refund','match_registration') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `method` enum('wechat','alipay','offline') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `appointment_id` int NULL DEFAULT NULL,
  `match_registration_id` int NULL DEFAULT NULL,
  `qr_code_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `status` enum('pending','completed','failed') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `appointment_id`(`appointment_id` ASC) USING BTREE,
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of transactions
-- ----------------------------
INSERT INTO `transactions` VALUES (1, 5, 500.00, 'deposit', 'wechat', NULL, NULL, NULL, 'completed', '2025-09-19 10:32:18');
INSERT INTO `transactions` VALUES (2, 5, 200.00, 'appointment_fee', 'wechat', 1, NULL, NULL, 'completed', '2025-09-19 10:32:18');
INSERT INTO `transactions` VALUES (8, 6, 1000.00, 'deposit', 'wechat', NULL, NULL, NULL, 'pending', '2025-09-22 21:00:31');
INSERT INTO `transactions` VALUES (9, 6, 100.00, 'appointment_fee', 'wechat', NULL, NULL, NULL, 'pending', '2025-09-22 21:00:47');
INSERT INTO `transactions` VALUES (10, 6, 100.00, 'appointment_fee', 'wechat', NULL, NULL, NULL, 'pending', '2025-09-22 21:02:11');
INSERT INTO `transactions` VALUES (11, 6, 100.00, 'appointment_fee', 'wechat', NULL, NULL, NULL, 'pending', '2025-09-22 21:03:18');
INSERT INTO `transactions` VALUES (12, 6, 1000.00, 'deposit', 'wechat', NULL, NULL, NULL, 'pending', '2025-09-22 21:03:33');
INSERT INTO `transactions` VALUES (13, 6, 1000.00, 'deposit', 'wechat', NULL, NULL, NULL, 'pending', '2025-09-22 21:04:12');
INSERT INTO `transactions` VALUES (14, 6, 100.00, 'appointment_fee', 'wechat', NULL, NULL, NULL, 'pending', '2025-09-22 21:04:25');
INSERT INTO `transactions` VALUES (15, 6, 5000.00, 'refund', 'wechat', NULL, NULL, NULL, 'pending', '2025-09-22 21:04:36');
INSERT INTO `transactions` VALUES (16, 6, 500.00, 'deposit', 'wechat', NULL, NULL, NULL, 'pending', '2025-09-22 21:28:33');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `real_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` enum('male','female','other') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `age` int NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `campus_id` int NULL DEFAULT NULL,
  `role` enum('super_admin','campus_admin','student','coach') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `photo_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `coach_level` enum('senior','mid','junior') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `achievements` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `is_approved` tinyint(1) NULL DEFAULT 0,
  `hourly_rate` decimal(10, 2) NULL DEFAULT NULL,
  `balance` decimal(10, 2) NULL DEFAULT 0.00,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  INDEX `fk_users_campus`(`campus_id` ASC) USING BTREE,
  CONSTRAINT `fk_users_campus` FOREIGN KEY (`campus_id`) REFERENCES `campuses` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', '1', '系统管理员', 'male', 40, '13800000001', 'admin@ttms.com', 1, 'super_admin', NULL, NULL, NULL, 1, NULL, 0.00, '2025-09-19 10:32:18', '2025-09-19 10:40:32');
INSERT INTO `users` VALUES (2, 'east_admin', '1', '李东', 'female', 35, '13800000002', 'east_admin@ttms.com', 2, 'campus_admin', NULL, NULL, NULL, 1, NULL, 0.00, '2025-09-19 10:32:18', '2025-09-19 16:10:23');
INSERT INTO `users` VALUES (3, 'coach_wang', '3', '王强', 'male', 30, '13800000003', 'coach_wang@ttms.com', 1, 'coach', '/photos/coach_wang.jpg', 'senior', '全国锦标赛冠军', 1, 200.00, 0.00, '2025-09-19 10:32:18', '2025-09-19 10:40:38');
INSERT INTO `users` VALUES (4, 'coach_liu', '4', '刘芳', 'female', 28, '13800000004', 'coach_liu@ttms.com', 2, 'coach', '/photos/coach_liu.jpg', 'junior', '省赛亚军', 1, 80.00, 0.00, '2025-09-19 10:32:18', '2025-09-19 10:40:39');
INSERT INTO `users` VALUES (5, 'student_zhang', '5', '张三', 'male', 18, '13800000005', 'zhangsan@ttms.com', 1, 'student', NULL, NULL, NULL, 1, NULL, 300.00, '2025-09-19 10:32:18', '2025-09-19 10:40:41');
INSERT INTO `users` VALUES (6, 'student_li', '6', '李四', 'female', 19, '13800000006', 'lisi@ttms.com', 2, 'student', NULL, NULL, NULL, 1, NULL, 5850.00, '2025-09-19 10:32:18', '2025-09-22 21:28:33');
INSERT INTO `users` VALUES (12, '炸鸡块', '1', '炸鸡块', 'male', 40, '12345678977', '2345678977@163.com', 1, 'coach', NULL, 'junior', NULL, 0, 80.00, 0.00, '2025-09-23 22:21:48', '2025-09-23 22:21:48');
INSERT INTO `users` VALUES (13, 'witness', '1', 'LIU Jianzheng', 'male', 21, '17331716730', '1850634290@qq.com', 1, 'super_admin', NULL, NULL, NULL, 0, NULL, 0.00, '2025-09-23 22:22:17', '2025-09-23 22:22:17');

-- ----------------------------
-- Triggers structure for table users
-- ----------------------------
DROP TRIGGER IF EXISTS `set_coach_rate`;
delimiter ;;
CREATE TRIGGER `set_coach_rate` BEFORE INSERT ON `users` FOR EACH ROW BEGIN
    IF NEW.role = 'coach' THEN
        CASE NEW.coach_level
            WHEN 'senior' THEN SET NEW.hourly_rate = 200.00;
            WHEN 'mid' THEN SET NEW.hourly_rate = 150.00;
            WHEN 'junior' THEN SET NEW.hourly_rate = 80.00;
        END CASE;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table users
-- ----------------------------
DROP TRIGGER IF EXISTS `update_coach_rate`;
delimiter ;;
CREATE TRIGGER `update_coach_rate` BEFORE UPDATE ON `users` FOR EACH ROW BEGIN
    IF NEW.role = 'coach' AND (OLD.coach_level != NEW.coach_level OR OLD.coach_level IS NULL) THEN
        CASE NEW.coach_level
            WHEN 'senior' THEN SET NEW.hourly_rate = 200.00;
            WHEN 'mid' THEN SET NEW.hourly_rate = 150.00;
            WHEN 'junior' THEN SET NEW.hourly_rate = 80.00;
        END CASE;
    END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
