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

 Date: 10/05/2024 22:31:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for self_entity
-- ----------------------------
DROP TABLE IF EXISTS `self_entity`;
CREATE TABLE `self_entity`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '唯一主键',
  `entity` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `imgUrl` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `relatedType` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `abstract` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL,
  `update_time` datetime(3) NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `create_time` datetime(3) NULL DEFAULT CURRENT_TIMESTAMP(3),
  `user_id` int NOT NULL COMMENT '对应用户id',
  `graph_id` int NOT NULL COMMENT '图id',
  `entity_id` int NOT NULL COMMENT '实体id',
  `deleted` tinyint(1) NULL DEFAULT 0 COMMENT '0:未删除 1：删除',
  `isCollect` tinyint(1) NULL DEFAULT 0 COMMENT '0:未收藏 1:已收藏',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of self_entity
-- ----------------------------
INSERT INTO `self_entity` VALUES (1, '贾宝玉', 'https://www.vrrw.net/d/file/uploads/allimg/181228/7-1Q22R3132a33.jpg', '主角;男', '贾宝玉，中国古典名著《红楼梦》中的人物。前世真身为神瑛侍者，荣国府贾政与王夫人所生的次子。因衔通灵宝玉而诞，系贾府玉字辈嫡孙，故名贾宝玉，贾府通称宝二。', '2024-04-30 12:03:21.839', '2024-03-26 22:17:18.432', 1, 1, 0, 0, 0);
INSERT INTO `self_entity` VALUES (2, '薛宝钗', 'https://x0.ifengimg.com/res/2020/F23E875EF466DCCD1305C6C6620B3562AD18C46E_size36_w640_h521.jpeg', '主角;女', '薛宝钗，是曹雪芹著长篇章回体小说《红楼梦》中的人物，与林黛玉并列为金陵十二钗之首，贾宝玉的从母姊（姨姊）、妻子。', '2024-04-12 17:43:57.897', '2024-03-26 22:17:55.050', 1, 1, 1, 0, 1);
INSERT INTO `self_entity` VALUES (3, '林黛玉', 'https://p12.qhimg.com/t010795234ddc441528.jpg', '主角;女', '林黛玉，中国古典名著《红楼梦》中的人物，金陵十二钗正册双首之一，西方灵河岸绛珠仙草转世，荣府幺女贾敏与扬州巡盐御史林如海之独生女，母亲贾敏是贾代善和贾母四个女儿里最小的女儿， [1]贾母的外孙女，贾宝玉的姑表妹、恋人、知己，贾府通称林姑娘。', '2024-04-29 20:38:53.784', '2024-03-26 22:18:55.593', 1, 1, 2, 0, 0);
INSERT INTO `self_entity` VALUES (4, '贾政', 'https://www.vrrw.net/uploads/allimg/181229/7-1Q229225415130.jpg', '男', '贾政，字存周，是曹雪芹著作《红楼梦》中的人物，荣国府二老爷，贾母和贾代善所生的次子，贾宝玉的父亲，林黛玉的舅舅，薛宝钗的姨父。', '2024-04-29 20:53:56.995', '2024-03-26 22:19:31.346', 1, 1, 3, 0, 0);
INSERT INTO `self_entity` VALUES (5, '肺泡蛋白质沉积症', '', '内科;呼吸内科', '肺泡蛋白质沉积症(简称PAP)，又称Rosen-Castle-man-Liebow综合征，是一种罕见疾病。该病以肺泡和细支气管腔内充满PAS染色阳性，来自肺的富磷脂蛋白质物质为其特征，好发于青中年，男性发病约3倍于女性。', '2024-04-29 21:42:59.607', '2024-04-29 12:56:51.933', 1, 3, 0, 0, 1);
INSERT INTO `self_entity` VALUES (6, '呼吸内科', '', '内科', '呼吸内科又称为肺病科，主要看气管、支气管、肺部等呼吸道的病变，不管是原发和既发，都可以在呼吸内科就诊。', '2024-04-29 21:05:30.240', '2024-04-29 13:01:00.328', 1, 3, 1, 0, NULL);
INSERT INTO `self_entity` VALUES (7, '呼吸困难', '', '症状', '呼吸困难是主观感觉和客观征象的综合表现，患者主观上感觉吸气不足、呼吸费力，客观上表现为呼吸频率、节律和深度的改变。严重时可出现张口呼吸、鼻翼扇动、端坐呼吸，甚至发绀。呼吸困难是呼吸衰竭的主要临床症状之一。', '2024-04-29 21:05:55.713', '2024-04-29 13:01:33.983', 1, 3, 2, 0, NULL);
INSERT INTO `self_entity` VALUES (8, '乏力', '', '症状', '乏力是临床上最常见的主诉症状之一，属非特异性疲惫感觉。表现为自觉疲劳、肢体软弱无力。生理状态下，乏力在休息或进食后可缓解，而病理性乏力则不能恢复正常。', '2024-04-29 21:05:51.195', '2024-04-29 13:02:12.968', 1, 3, 3, 0, NULL);
INSERT INTO `self_entity` VALUES (9, '胸痛', '', '症状', '胸痛是一种常见而又能危及生命的病症，造成胸痛的原因复杂多样，包括急性冠脉综合征（ACS）、主动脉夹层、肺栓塞（PE）、气胸、心包炎、心包填塞和食管破裂等，其中ACS在这些严重危及生命的疾病中所占比例最高。', '2024-04-29 21:05:49.513', '2024-04-29 13:03:02.800', 1, 3, 4, 0, NULL);
INSERT INTO `self_entity` VALUES (10, '发绀', '', '症状', '发绀是指血液中去氧血红蛋白增多使皮肤和粘膜呈青紫色改变的一种表现，也可称为紫绀。这种改变常发生在皮肤较薄，色素较少和毛细血管较丰富的部位，如唇、指（趾）、甲床等。', '2024-04-29 21:05:50.102', '2024-04-29 13:03:51.939', 1, 3, 5, 0, NULL);
INSERT INTO `self_entity` VALUES (11, '妙玉', 'https://img.izhixiu.com/2021/1111/21111165.jpg', '女', '妙玉，《红楼梦》金陵十二钗之一，苏州人士，是一个带发修行的居士。她原是仕宦人家的小姐，自小在玄墓蟠香寺出家为尼。', '2024-04-29 21:52:15.906', '2024-04-29 13:48:52.923', 1, 1, 4, 0, NULL);
INSERT INTO `self_entity` VALUES (12, '史湘云', 'https://pic1.zhimg.com/v2-65652e2284e823764f7bf36764cbaa3c_r.jpg', '女', '史湘云，中国古典名著《红楼梦》中的主要人物，金陵十二钗之一，四大家族中史家的千金，是贾母的内侄孙女，贾府通称史大姑娘。', '2024-04-29 21:52:46.719', '2024-04-29 13:49:35.509', 1, 1, 5, 0, NULL);

SET FOREIGN_KEY_CHECKS = 1;
