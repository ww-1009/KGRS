/*
 Navicat Premium Data Transfer

 Source Server         : mycontent
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : fd_dg

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 10/05/2024 22:31:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for self_relation
-- ----------------------------
DROP TABLE IF EXISTS `self_relation`;
CREATE TABLE `self_relation`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '唯一主键',
  `user_id` int NOT NULL COMMENT '用户id',
  `graph_id` int NOT NULL COMMENT '图id',
  `id_S` int NULL DEFAULT NULL COMMENT 'id_s',
  `S` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '主',
  `P` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '谓',
  `O` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '宾',
  `id_O` int NULL DEFAULT NULL COMMENT 'id_o',
  `update_time` datetime(3) NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '更新时间',
  `create_time` datetime(3) NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '创建时间',
  `deleted` tinyint(1) NULL DEFAULT 0 COMMENT '0:未删除 1：删除',
  `relation_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of self_relation
-- ----------------------------
INSERT INTO `self_relation` VALUES (1, 1, 1, 0, '贾宝玉', '夫妻', '薛宝钗', 1, '2024-04-12 17:50:02.867', '2024-03-26 22:21:41.347', 0, 0);
INSERT INTO `self_relation` VALUES (2, 1, 1, 0, '贾宝玉', '表兄妹', '林黛玉', 2, '2024-04-12 17:50:04.647', '2024-03-26 22:21:51.933', 0, 1);
INSERT INTO `self_relation` VALUES (3, 1, 1, 3, '贾政', '父子', '贾宝玉', 0, '2024-04-12 17:50:06.333', '2024-03-26 22:22:55.231', 0, 2);
INSERT INTO `self_relation` VALUES (4, 1, 1, 1, '薛宝钗', '好友', '林黛玉', 2, '2024-04-29 20:33:00.911', '2024-03-26 22:24:02.879', 0, 3);
INSERT INTO `self_relation` VALUES (5, 1, 3, 0, '肺泡蛋白质沉积症', 'has_symptom', '发绀', 5, '2024-04-29 13:34:21.231', '2024-04-29 13:34:21.231', 0, 0);
INSERT INTO `self_relation` VALUES (6, 1, 3, 0, '肺泡蛋白质沉积症', 'belongs_to', '呼吸内科', 1, '2024-04-29 13:36:20.443', '2024-04-29 13:36:20.443', 0, 1);
INSERT INTO `self_relation` VALUES (7, 1, 3, 0, '肺泡蛋白质沉积症', 'has_symptom', '乏力', 3, '2024-04-29 13:36:49.871', '2024-04-29 13:36:49.871', 0, 2);
INSERT INTO `self_relation` VALUES (8, 1, 3, 0, '肺泡蛋白质沉积症', 'has_symptom', '呼吸困难', 2, '2024-04-29 21:38:49.635', '2024-04-29 13:37:51.035', 0, 3);
INSERT INTO `self_relation` VALUES (9, 1, 1, 5, '史湘云', '好友', '贾宝玉', 0, '2024-04-29 13:50:01.524', '2024-04-29 13:50:01.524', 0, 4);
INSERT INTO `self_relation` VALUES (10, 1, 1, 4, '妙玉', '好友', '史湘云', 5, '2024-04-29 13:50:31.410', '2024-04-29 13:50:31.410', 0, 5);
INSERT INTO `self_relation` VALUES (11, 1, 1, 1, '薛宝钗', '好友', '妙玉', 4, '2024-04-29 13:50:59.743', '2024-04-29 13:50:59.743', 0, 6);

SET FOREIGN_KEY_CHECKS = 1;
