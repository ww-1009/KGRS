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

 Date: 10/05/2024 22:31:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for self_graph_info
-- ----------------------------
DROP TABLE IF EXISTS `self_graph_info`;
CREATE TABLE `self_graph_info`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `graph_id` int NOT NULL,
  `graph_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `deleted` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '0:未删除 1：删除',
  `update_time` datetime(3) NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `create_time` datetime(3) NULL DEFAULT CURRENT_TIMESTAMP(3),
  `description` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of self_graph_info
-- ----------------------------
INSERT INTO `self_graph_info` VALUES (1, 1, 1, '红楼梦人物知识图谱', 0, '2024-04-14 11:43:14.048', '2024-03-13 09:29:52.602', '是一个帮助了解红楼梦中人物关系的图谱。');
INSERT INTO `self_graph_info` VALUES (2, 1, 2, '计算机网络知识图谱', 0, '2024-03-24 23:55:44.337', '2024-03-13 09:30:11.690', '	\r\n关于计算机网络的知识图谱');
INSERT INTO `self_graph_info` VALUES (3, 1, 3, '医疗知识图谱', 0, '2024-03-24 23:56:05.621', '2024-03-24 23:56:01.322', '关于医疗的知识图谱');
INSERT INTO `self_graph_info` VALUES (4, 1, 4, '13', 1, '2024-04-29 20:32:26.387', '2024-04-14 11:33:54.366', '123');
INSERT INTO `self_graph_info` VALUES (5, 1, 5, '123', 1, '2024-04-29 20:29:29.315', '2024-04-14 11:43:21.128', '123');
INSERT INTO `self_graph_info` VALUES (6, 1, 6, '123', 0, '2024-04-30 04:02:17.266', '2024-04-30 04:02:17.266', '11233');

SET FOREIGN_KEY_CHECKS = 1;
