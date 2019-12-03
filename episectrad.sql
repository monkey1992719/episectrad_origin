/*
 Navicat MySQL Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50643
 Source Host           : localhost:3306
 Source Schema         : episectrad

 Target Server Type    : MySQL
 Target Server Version : 50643
 File Encoding         : 65001

 Date: 08/03/2019 16:56:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 113 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add user', 6, 'add_user');
INSERT INTO `auth_permission` VALUES (22, 'Can change user', 6, 'change_user');
INSERT INTO `auth_permission` VALUES (23, 'Can delete user', 6, 'delete_user');
INSERT INTO `auth_permission` VALUES (24, 'Can view user', 6, 'view_user');
INSERT INTO `auth_permission` VALUES (25, 'Can add static device', 7, 'add_staticdevice');
INSERT INTO `auth_permission` VALUES (26, 'Can change static device', 7, 'change_staticdevice');
INSERT INTO `auth_permission` VALUES (27, 'Can delete static device', 7, 'delete_staticdevice');
INSERT INTO `auth_permission` VALUES (28, 'Can view static device', 7, 'view_staticdevice');
INSERT INTO `auth_permission` VALUES (29, 'Can add static token', 8, 'add_statictoken');
INSERT INTO `auth_permission` VALUES (30, 'Can change static token', 8, 'change_statictoken');
INSERT INTO `auth_permission` VALUES (31, 'Can delete static token', 8, 'delete_statictoken');
INSERT INTO `auth_permission` VALUES (32, 'Can view static token', 8, 'view_statictoken');
INSERT INTO `auth_permission` VALUES (33, 'Can add TOTP device', 9, 'add_totpdevice');
INSERT INTO `auth_permission` VALUES (34, 'Can change TOTP device', 9, 'change_totpdevice');
INSERT INTO `auth_permission` VALUES (35, 'Can delete TOTP device', 9, 'delete_totpdevice');
INSERT INTO `auth_permission` VALUES (36, 'Can view TOTP device', 9, 'view_totpdevice');
INSERT INTO `auth_permission` VALUES (37, 'Can add phone device', 10, 'add_phonedevice');
INSERT INTO `auth_permission` VALUES (38, 'Can change phone device', 10, 'change_phonedevice');
INSERT INTO `auth_permission` VALUES (39, 'Can delete phone device', 10, 'delete_phonedevice');
INSERT INTO `auth_permission` VALUES (40, 'Can view phone device', 10, 'view_phonedevice');
INSERT INTO `auth_permission` VALUES (41, 'Can add news subscription', 11, 'add_newssubscription');
INSERT INTO `auth_permission` VALUES (42, 'Can change news subscription', 11, 'change_newssubscription');
INSERT INTO `auth_permission` VALUES (43, 'Can delete news subscription', 11, 'delete_newssubscription');
INSERT INTO `auth_permission` VALUES (44, 'Can view news subscription', 11, 'view_newssubscription');
INSERT INTO `auth_permission` VALUES (45, 'Can add token metric', 12, 'add_tokenmetric');
INSERT INTO `auth_permission` VALUES (46, 'Can change token metric', 12, 'change_tokenmetric');
INSERT INTO `auth_permission` VALUES (47, 'Can delete token metric', 12, 'delete_tokenmetric');
INSERT INTO `auth_permission` VALUES (48, 'Can view token metric', 12, 'view_tokenmetric');
INSERT INTO `auth_permission` VALUES (49, 'Can add task result', 13, 'add_taskresult');
INSERT INTO `auth_permission` VALUES (50, 'Can change task result', 13, 'change_taskresult');
INSERT INTO `auth_permission` VALUES (51, 'Can delete task result', 13, 'delete_taskresult');
INSERT INTO `auth_permission` VALUES (52, 'Can view task result', 13, 'view_taskresult');
INSERT INTO `auth_permission` VALUES (53, 'Can add chart plot', 14, 'add_chartplot');
INSERT INTO `auth_permission` VALUES (54, 'Can change chart plot', 14, 'change_chartplot');
INSERT INTO `auth_permission` VALUES (55, 'Can delete chart plot', 14, 'delete_chartplot');
INSERT INTO `auth_permission` VALUES (56, 'Can view chart plot', 14, 'view_chartplot');
INSERT INTO `auth_permission` VALUES (57, 'Can add chart plot setting', 15, 'add_chartplotsetting');
INSERT INTO `auth_permission` VALUES (58, 'Can change chart plot setting', 15, 'change_chartplotsetting');
INSERT INTO `auth_permission` VALUES (59, 'Can delete chart plot setting', 15, 'delete_chartplotsetting');
INSERT INTO `auth_permission` VALUES (60, 'Can view chart plot setting', 15, 'view_chartplotsetting');
INSERT INTO `auth_permission` VALUES (61, 'Can add chart setting', 16, 'add_chartsetting');
INSERT INTO `auth_permission` VALUES (62, 'Can change chart setting', 16, 'change_chartsetting');
INSERT INTO `auth_permission` VALUES (63, 'Can delete chart setting', 16, 'delete_chartsetting');
INSERT INTO `auth_permission` VALUES (64, 'Can view chart setting', 16, 'view_chartsetting');
INSERT INTO `auth_permission` VALUES (65, 'Can add chart string', 17, 'add_chartstring');
INSERT INTO `auth_permission` VALUES (66, 'Can change chart string', 17, 'change_chartstring');
INSERT INTO `auth_permission` VALUES (67, 'Can delete chart string', 17, 'delete_chartstring');
INSERT INTO `auth_permission` VALUES (68, 'Can view chart string', 17, 'view_chartstring');
INSERT INTO `auth_permission` VALUES (69, 'Can add indicator', 18, 'add_indicator');
INSERT INTO `auth_permission` VALUES (70, 'Can change indicator', 18, 'change_indicator');
INSERT INTO `auth_permission` VALUES (71, 'Can delete indicator', 18, 'delete_indicator');
INSERT INTO `auth_permission` VALUES (72, 'Can view indicator', 18, 'view_indicator');
INSERT INTO `auth_permission` VALUES (73, 'Can add indicator input', 19, 'add_indicatorinput');
INSERT INTO `auth_permission` VALUES (74, 'Can change indicator input', 19, 'change_indicatorinput');
INSERT INTO `auth_permission` VALUES (75, 'Can delete indicator input', 19, 'delete_indicatorinput');
INSERT INTO `auth_permission` VALUES (76, 'Can view indicator input', 19, 'view_indicatorinput');
INSERT INTO `auth_permission` VALUES (77, 'Can add indicator input member ship', 20, 'add_indicatorinputmembership');
INSERT INTO `auth_permission` VALUES (78, 'Can change indicator input member ship', 20, 'change_indicatorinputmembership');
INSERT INTO `auth_permission` VALUES (79, 'Can delete indicator input member ship', 20, 'delete_indicatorinputmembership');
INSERT INTO `auth_permission` VALUES (80, 'Can view indicator input member ship', 20, 'view_indicatorinputmembership');
INSERT INTO `auth_permission` VALUES (81, 'Can add indicator input value', 21, 'add_indicatorinputvalue');
INSERT INTO `auth_permission` VALUES (82, 'Can change indicator input value', 21, 'change_indicatorinputvalue');
INSERT INTO `auth_permission` VALUES (83, 'Can delete indicator input value', 21, 'delete_indicatorinputvalue');
INSERT INTO `auth_permission` VALUES (84, 'Can view indicator input value', 21, 'view_indicatorinputvalue');
INSERT INTO `auth_permission` VALUES (85, 'Can add trade chart pattern', 22, 'add_tradechartpattern');
INSERT INTO `auth_permission` VALUES (86, 'Can change trade chart pattern', 22, 'change_tradechartpattern');
INSERT INTO `auth_permission` VALUES (87, 'Can delete trade chart pattern', 22, 'delete_tradechartpattern');
INSERT INTO `auth_permission` VALUES (88, 'Can view trade chart pattern', 22, 'view_tradechartpattern');
INSERT INTO `auth_permission` VALUES (89, 'Can add trade indicator', 23, 'add_tradeindicator');
INSERT INTO `auth_permission` VALUES (90, 'Can change trade indicator', 23, 'change_tradeindicator');
INSERT INTO `auth_permission` VALUES (91, 'Can delete trade indicator', 23, 'delete_tradeindicator');
INSERT INTO `auth_permission` VALUES (92, 'Can view trade indicator', 23, 'view_tradeindicator');
INSERT INTO `auth_permission` VALUES (93, 'Can add trade indicator cross2', 24, 'add_tradeindicatorcross2');
INSERT INTO `auth_permission` VALUES (94, 'Can change trade indicator cross2', 24, 'change_tradeindicatorcross2');
INSERT INTO `auth_permission` VALUES (95, 'Can delete trade indicator cross2', 24, 'delete_tradeindicatorcross2');
INSERT INTO `auth_permission` VALUES (96, 'Can view trade indicator cross2', 24, 'view_tradeindicatorcross2');
INSERT INTO `auth_permission` VALUES (97, 'Can add trade indicator crossv', 25, 'add_tradeindicatorcrossv');
INSERT INTO `auth_permission` VALUES (98, 'Can change trade indicator crossv', 25, 'change_tradeindicatorcrossv');
INSERT INTO `auth_permission` VALUES (99, 'Can delete trade indicator crossv', 25, 'delete_tradeindicatorcrossv');
INSERT INTO `auth_permission` VALUES (100, 'Can view trade indicator crossv', 25, 'view_tradeindicatorcrossv');
INSERT INTO `auth_permission` VALUES (101, 'Can add trade indicator indicator', 26, 'add_tradeindicatorindicator');
INSERT INTO `auth_permission` VALUES (102, 'Can change trade indicator indicator', 26, 'change_tradeindicatorindicator');
INSERT INTO `auth_permission` VALUES (103, 'Can delete trade indicator indicator', 26, 'delete_tradeindicatorindicator');
INSERT INTO `auth_permission` VALUES (104, 'Can view trade indicator indicator', 26, 'view_tradeindicatorindicator');
INSERT INTO `auth_permission` VALUES (105, 'Can add trade indicator plot threshold', 27, 'add_tradeindicatorplotthreshold');
INSERT INTO `auth_permission` VALUES (106, 'Can change trade indicator plot threshold', 27, 'change_tradeindicatorplotthreshold');
INSERT INTO `auth_permission` VALUES (107, 'Can delete trade indicator plot threshold', 27, 'delete_tradeindicatorplotthreshold');
INSERT INTO `auth_permission` VALUES (108, 'Can view trade indicator plot threshold', 27, 'view_tradeindicatorplotthreshold');
INSERT INTO `auth_permission` VALUES (109, 'Can add trade pricebar pattern', 28, 'add_tradepricebarpattern');
INSERT INTO `auth_permission` VALUES (110, 'Can change trade pricebar pattern', 28, 'change_tradepricebarpattern');
INSERT INTO `auth_permission` VALUES (111, 'Can delete trade pricebar pattern', 28, 'delete_tradepricebarpattern');
INSERT INTO `auth_permission` VALUES (112, 'Can view trade pricebar pattern', 28, 'view_tradepricebarpattern');

-- ----------------------------
-- Table structure for chart_plot
-- ----------------------------
DROP TABLE IF EXISTS `chart_plot`;
CREATE TABLE `chart_plot`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plotname` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `plottype` varchar(30) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `setting_manual` bigint(1) NULL DEFAULT NULL,
  `indicator_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 63 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of chart_plot
-- ----------------------------
INSERT INTO `chart_plot` VALUES (1, 'AO', 'histogram', 0, 1);
INSERT INTO `chart_plot` VALUES (2, 'acc', 'line', 1, 37);
INSERT INTO `chart_plot` VALUES (3, 'aroon_up', 'line', 1, 13);
INSERT INTO `chart_plot` VALUES (4, 'aroon_down', 'line', 1, 13);
INSERT INTO `chart_plot` VALUES (5, 'adi', 'line', 1, 14);
INSERT INTO `chart_plot` VALUES (6, 'ATR', 'line', 1, 31);
INSERT INTO `chart_plot` VALUES (7, 'cmo', 'line', 1, 2);
INSERT INTO `chart_plot` VALUES (8, 'MOM', 'line', 1, 4);
INSERT INTO `chart_plot` VALUES (9, 'CC', 'line', 1, 3);
INSERT INTO `chart_plot` VALUES (10, 'mfi_', 'line', 1, 5);
INSERT INTO `chart_plot` VALUES (11, 'PO', 'line', 1, 6);
INSERT INTO `chart_plot` VALUES (12, 'RSI', 'line', 1, 7);
INSERT INTO `chart_plot` VALUES (13, 'STOK', 'line', 1, 8);
INSERT INTO `chart_plot` VALUES (14, 'STOD', 'line', 1, 8);
INSERT INTO `chart_plot` VALUES (15, 'STCHRSI', 'line', 1, 9);
INSERT INTO `chart_plot` VALUES (16, 'TSI', 'line', 1, 10);
INSERT INTO `chart_plot` VALUES (17, 'uo', 'line', 1, 11);
INSERT INTO `chart_plot` VALUES (18, 'WPR', 'line', 1, 12);
INSERT INTO `chart_plot` VALUES (19, 'CCI', 'line', 1, 15);
INSERT INTO `chart_plot` VALUES (20, 'adx_pos', 'line', 1, 16);
INSERT INTO `chart_plot` VALUES (21, 'adx_neg', 'line', 1, 16);
INSERT INTO `chart_plot` VALUES (22, 'dema', 'line', 1, 17);
INSERT INTO `chart_plot` VALUES (23, 'hma', 'line', 1, 18);
INSERT INTO `chart_plot` VALUES (24, 'ic_a', 'line', 1, 19);
INSERT INTO `chart_plot` VALUES (25, 'ic_b', 'line', 1, 19);
INSERT INTO `chart_plot` VALUES (26, 'KST', 'line', 1, 20);
INSERT INTO `chart_plot` VALUES (27, 'SMA12', 'line', 1, 21);
INSERT INTO `chart_plot` VALUES (28, 'SMA26', 'line', 1, 21);
INSERT INTO `chart_plot` VALUES (29, 'MACD', 'line', 1, 22);
INSERT INTO `chart_plot` VALUES (30, 'MACDSig', 'line', 1, 22);
INSERT INTO `chart_plot` VALUES (31, 'mass_index', 'line', 1, 23);
INSERT INTO `chart_plot` VALUES (32, 'ema', 'line', 1, 24);
INSERT INTO `chart_plot` VALUES (33, 'sma', 'line', 1, 25);
INSERT INTO `chart_plot` VALUES (34, 'wma', 'line', 1, 26);
INSERT INTO `chart_plot` VALUES (35, 'smooth_ma', 'line', 1, 27);
INSERT INTO `chart_plot` VALUES (36, 'TRIX', 'line', 1, 28);
INSERT INTO `chart_plot` VALUES (37, 'tema', 'line', 1, 29);
INSERT INTO `chart_plot` VALUES (38, 'voi_pos', 'line', 1, 30);
INSERT INTO `chart_plot` VALUES (39, 'voi_neg', 'line', 1, 30);
INSERT INTO `chart_plot` VALUES (40, 'UPRBB', 'line', 1, 32);
INSERT INTO `chart_plot` VALUES (41, 'MIDBB', 'line', 1, 32);
INSERT INTO `chart_plot` VALUES (42, 'LWRBB', 'line', 1, 32);
INSERT INTO `chart_plot` VALUES (43, 'bb_pb', 'line', 1, 33);
INSERT INTO `chart_plot` VALUES (44, 'bb_bw', 'line', 1, 34);
INSERT INTO `chart_plot` VALUES (45, 'dc_hband', 'line', 1, 35);
INSERT INTO `chart_plot` VALUES (46, 'dc_lband', 'line', 1, 35);
INSERT INTO `chart_plot` VALUES (47, 'kc_central', 'line', 1, 36);
INSERT INTO `chart_plot` VALUES (48, 'kc_hband', 'line', 1, 36);
INSERT INTO `chart_plot` VALUES (49, 'kc_lband', 'line', 1, 36);
INSERT INTO `chart_plot` VALUES (50, 'cmf', 'line', 1, 38);
INSERT INTO `chart_plot` VALUES (51, 'ch_osc', 'line', 1, 39);
INSERT INTO `chart_plot` VALUES (52, 'eom_14', 'line', 1, 40);
INSERT INTO `chart_plot` VALUES (53, 'obv', 'line', 1, 41);
INSERT INTO `chart_plot` VALUES (54, 'PVI', 'line', 1, 42);
INSERT INTO `chart_plot` VALUES (55, 'NVI', 'line', 1, 42);
INSERT INTO `chart_plot` VALUES (56, 'vo', 'line', 1, NULL);
INSERT INTO `chart_plot` VALUES (57, 'MACDHistogram', 'histogram', 0, 22);
INSERT INTO `chart_plot` VALUES (58, 'mfi_sma', 'line', 1, 5);
INSERT INTO `chart_plot` VALUES (59, 'mfi_high', 'line', 1, 5);
INSERT INTO `chart_plot` VALUES (60, 'mfi_mid', 'line', 1, 5);
INSERT INTO `chart_plot` VALUES (61, 'mfi_low', 'line', 1, 5);
INSERT INTO `chart_plot` VALUES (62, 'KST_SIG', 'line', 1, 20);

-- ----------------------------
-- Table structure for chart_plot_default_setting
-- ----------------------------
DROP TABLE IF EXISTS `chart_plot_default_setting`;
CREATE TABLE `chart_plot_default_setting`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `string_id` int(11) NULL DEFAULT NULL,
  `color` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `width` int(11) NULL DEFAULT NULL,
  `plottype` varchar(30) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `setting_manual` bigint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 63 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of chart_plot_default_setting
-- ----------------------------
INSERT INTO `chart_plot_default_setting` VALUES (1, 1, '#00ff00', 1, 'histogram', 0);
INSERT INTO `chart_plot_default_setting` VALUES (2, 2, '#ff9900', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (3, 3, '#0084ff', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (4, 4, '#ffbb00', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (5, 5, '#ffbb00', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (6, 6, '#992515', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (7, 7, '#0084ff', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (8, 8, '#92b338', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (9, 9, '#4e93e2', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (10, 10, '#eb6619', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (11, 11, '#00854d', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (12, 12, '#a200ff', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (13, 13, '#0084ff', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (14, 14, '#e94d0f', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (15, 15, '#0084ff', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (16, 16, '#0084ff', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (17, 17, '#d10034', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (18, 18, '#0084ff', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (19, 19, '#836103', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (20, 20, '#004fb6', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (21, 21, '#eb6619', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (22, 22, '#275515', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (23, 23, '#450680', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (24, 24, '#4a9144', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (25, 25, '#ff0000', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (26, 26, '#1e9b6b', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (27, 27, '#ffbb00', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (28, 28, '#ffbb00', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (29, 29, '#497453', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (30, 30, '#8d5869', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (31, 31, '#5c95bb', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (32, 32, '#32528d', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (33, 33, '#9152f7', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (34, 34, '#301777', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (35, 35, '#4eaa46', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (36, 36, '#812e3c', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (37, 37, '#0f6127', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (38, 38, '#4b80bd', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (39, 39, '#d34ca6', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (40, 40, '#28ddf5', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (41, 41, '#578f17', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (42, 42, '#612b13', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (43, 43, '#375abb', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (44, 44, '#20645b', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (45, 45, '#1a5fb9', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (46, 46, '#bda310', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (47, 47, '#30b1ec', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (48, 48, '#30b1ec', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (49, 49, '#30b1ec', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (50, 50, '#fa4040', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (51, 51, '#578f17', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (52, 52, '#578f17', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (53, 53, '#3d3b68', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (54, 54, '#2a6911', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (55, 55, '#b64f3d', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (56, 56, '#1c5c91', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (57, 57, '#000000', 1, 'histogram', 0);
INSERT INTO `chart_plot_default_setting` VALUES (58, 58, '#a0a0a0', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (59, 59, '#00ff00', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (60, 60, '#a0a0a0', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (61, 61, '#ff0000', 1, 'line', 1);
INSERT INTO `chart_plot_default_setting` VALUES (62, 62, '#c72b2b', 1, 'line', 1);

-- ----------------------------
-- Table structure for chart_plot_setting
-- ----------------------------
DROP TABLE IF EXISTS `chart_plot_setting`;
CREATE TABLE `chart_plot_setting`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `plot_id` int(11) NULL DEFAULT NULL COMMENT 'one to one chart_strings',
  `color` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `width` int(11) NULL DEFAULT NULL,
  `plottype` int(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for chart_setting
-- ----------------------------
DROP TABLE IF EXISTS `chart_setting`;
CREATE TABLE `chart_setting`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `symbol` varchar(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `period` varchar(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `interval` varchar(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `bIntraday` int(2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of chart_setting
-- ----------------------------
INSERT INTO `chart_setting` VALUES (1, NULL, 'GOLD', '36m', '30min', 1);

-- ----------------------------
-- Table structure for chart_strings
-- ----------------------------
DROP TABLE IF EXISTS `chart_strings`;
CREATE TABLE `chart_strings`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 63 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of chart_strings
-- ----------------------------
INSERT INTO `chart_strings` VALUES (1, 'AO');
INSERT INTO `chart_strings` VALUES (2, 'acc');
INSERT INTO `chart_strings` VALUES (3, 'aroon_up');
INSERT INTO `chart_strings` VALUES (4, 'aroon_down');
INSERT INTO `chart_strings` VALUES (5, 'adi');
INSERT INTO `chart_strings` VALUES (6, 'ATR');
INSERT INTO `chart_strings` VALUES (7, 'cmo');
INSERT INTO `chart_strings` VALUES (8, 'MOM');
INSERT INTO `chart_strings` VALUES (9, 'CC');
INSERT INTO `chart_strings` VALUES (10, 'mfi_');
INSERT INTO `chart_strings` VALUES (11, 'PO');
INSERT INTO `chart_strings` VALUES (12, 'RSI');
INSERT INTO `chart_strings` VALUES (13, 'STOK');
INSERT INTO `chart_strings` VALUES (14, 'STOD');
INSERT INTO `chart_strings` VALUES (15, 'STCHRSI');
INSERT INTO `chart_strings` VALUES (16, 'TSI');
INSERT INTO `chart_strings` VALUES (17, 'uo');
INSERT INTO `chart_strings` VALUES (18, 'WPR');
INSERT INTO `chart_strings` VALUES (19, 'CCI');
INSERT INTO `chart_strings` VALUES (20, 'adx_pos');
INSERT INTO `chart_strings` VALUES (21, 'adx_neg');
INSERT INTO `chart_strings` VALUES (22, 'dema');
INSERT INTO `chart_strings` VALUES (23, 'hma');
INSERT INTO `chart_strings` VALUES (24, 'ic_a');
INSERT INTO `chart_strings` VALUES (25, 'ic_b');
INSERT INTO `chart_strings` VALUES (26, 'KST');
INSERT INTO `chart_strings` VALUES (27, 'SMA12');
INSERT INTO `chart_strings` VALUES (28, 'SMA26');
INSERT INTO `chart_strings` VALUES (29, 'MACD');
INSERT INTO `chart_strings` VALUES (30, 'MACDSig');
INSERT INTO `chart_strings` VALUES (31, 'mass_index');
INSERT INTO `chart_strings` VALUES (32, 'ema');
INSERT INTO `chart_strings` VALUES (33, 'sma');
INSERT INTO `chart_strings` VALUES (34, 'wma');
INSERT INTO `chart_strings` VALUES (35, 'smooth_ma');
INSERT INTO `chart_strings` VALUES (36, 'TRIX');
INSERT INTO `chart_strings` VALUES (37, 'tema');
INSERT INTO `chart_strings` VALUES (38, 'voi_pos');
INSERT INTO `chart_strings` VALUES (39, 'voi_neg');
INSERT INTO `chart_strings` VALUES (40, 'UPRBB');
INSERT INTO `chart_strings` VALUES (41, 'MIDBB');
INSERT INTO `chart_strings` VALUES (42, 'LWRBB');
INSERT INTO `chart_strings` VALUES (43, 'bb_pb');
INSERT INTO `chart_strings` VALUES (44, 'bb_bw');
INSERT INTO `chart_strings` VALUES (45, 'dc_hband');
INSERT INTO `chart_strings` VALUES (46, 'dc_lband');
INSERT INTO `chart_strings` VALUES (47, 'kc_central');
INSERT INTO `chart_strings` VALUES (48, 'kc_hband');
INSERT INTO `chart_strings` VALUES (49, 'kc_lband');
INSERT INTO `chart_strings` VALUES (50, 'cmf');
INSERT INTO `chart_strings` VALUES (51, 'ch_osc');
INSERT INTO `chart_strings` VALUES (52, 'eom_14');
INSERT INTO `chart_strings` VALUES (53, 'obv');
INSERT INTO `chart_strings` VALUES (54, 'PVI');
INSERT INTO `chart_strings` VALUES (55, 'NVI');
INSERT INTO `chart_strings` VALUES (56, 'vo');
INSERT INTO `chart_strings` VALUES (57, 'MACDHistogram');
INSERT INTO `chart_strings` VALUES (58, 'mfi_sma');
INSERT INTO `chart_strings` VALUES (59, 'mfi_high');
INSERT INTO `chart_strings` VALUES (60, 'mfi_mid');
INSERT INTO `chart_strings` VALUES (61, 'mfi_low');
INSERT INTO `chart_strings` VALUES (62, 'KST_SIG');

-- ----------------------------
-- Table structure for core_newssubscription
-- ----------------------------
DROP TABLE IF EXISTS `core_newssubscription`;
CREATE TABLE `core_newssubscription`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime(6) NOT NULL,
  `email` varchar(254) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for core_tokenmetric
-- ----------------------------
DROP TABLE IF EXISTS `core_tokenmetric`;
CREATE TABLE `core_tokenmetric`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `rank` int(11) NOT NULL,
  `price_usd` decimal(12, 7) NOT NULL,
  `price_btc` decimal(24, 16) NOT NULL,
  `day_volume_usd` decimal(12, 2) NOT NULL,
  `market_cap_usd` decimal(12, 2) NOT NULL,
  `available_supply` decimal(24, 8) NOT NULL,
  `total_supply` decimal(24, 8) NOT NULL,
  `percent_change_1h` decimal(12, 2) NOT NULL,
  `percent_change_24h` decimal(12, 2) NOT NULL,
  `percent_change_7d` decimal(12, 2) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for dashboard_indicatorinput
-- ----------------------------
DROP TABLE IF EXISTS `dashboard_indicatorinput`;
CREATE TABLE `dashboard_indicatorinput`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parameter` varchar(64) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 43 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of dashboard_indicatorinput
-- ----------------------------
INSERT INTO `dashboard_indicatorinput` VALUES (1, 'aa');
INSERT INTO `dashboard_indicatorinput` VALUES (2, 'bb');
INSERT INTO `dashboard_indicatorinput` VALUES (3, 'cc');
INSERT INTO `dashboard_indicatorinput` VALUES (34, 'aa');
INSERT INTO `dashboard_indicatorinput` VALUES (35, 'bb');
INSERT INTO `dashboard_indicatorinput` VALUES (36, 'cc');
INSERT INTO `dashboard_indicatorinput` VALUES (37, 'aa');
INSERT INTO `dashboard_indicatorinput` VALUES (38, 'bb');
INSERT INTO `dashboard_indicatorinput` VALUES (39, 'cc');
INSERT INTO `dashboard_indicatorinput` VALUES (40, 'aa');
INSERT INTO `dashboard_indicatorinput` VALUES (41, 'bb');
INSERT INTO `dashboard_indicatorinput` VALUES (42, 'cc');

-- ----------------------------
-- Table structure for dashboard_user
-- ----------------------------
DROP TABLE IF EXISTS `dashboard_user`;
CREATE TABLE `dashboard_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `email_confirmed` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of dashboard_user
-- ----------------------------
INSERT INTO `dashboard_user` VALUES (20, 'pbkdf2_sha256$120000$TdfwgpppkvCq$Pz8SUV/cMDvJseHtFnJCATg62q8vvsleVciXxKKoo5U=', NULL, 0, 'kss_alexander@outlook.com', 0, 0, 1, '2019-01-31 18:01:54.947472');

-- ----------------------------
-- Table structure for dashboard_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `dashboard_user_groups`;
CREATE TABLE `dashboard_user_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `dashboard_user_groups_user_id_group_id_2c570fca_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `dashboard_user_groups_group_id_54086039_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `dashboard_user_groups_group_id_54086039_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `dashboard_user_groups_user_id_a915c7fc_fk_dashboard_user_id` FOREIGN KEY (`user_id`) REFERENCES `dashboard_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for dashboard_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `dashboard_user_user_permissions`;
CREATE TABLE `dashboard_user_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `dashboard_user_user_perm_user_id_permission_id_550d0c70_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `dashboard_user_user__permission_id_70269958_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `dashboard_user_user__permission_id_70269958_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `dashboard_user_user__user_id_ea9b20c2_fk_dashboard` FOREIGN KEY (`user_id`) REFERENCES `dashboard_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `object_repr` varchar(200) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_dashboard_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_dashboard_user_id` FOREIGN KEY (`user_id`) REFERENCES `dashboard_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for django_celery_results_taskresult
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_results_taskresult`;
CREATE TABLE `django_celery_results_taskresult`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `status` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `content_type` varchar(128) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `content_encoding` varchar(64) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `result` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `task_args` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `task_kwargs` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `task_name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `task_id`(`task_id`) USING BTREE,
  INDEX `django_celery_results_taskresult_hidden_cd77412f`(`hidden`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `model` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (11, 'core', 'newssubscription');
INSERT INTO `django_content_type` VALUES (12, 'core', 'tokenmetric');
INSERT INTO `django_content_type` VALUES (14, 'dashboard', 'chartplot');
INSERT INTO `django_content_type` VALUES (15, 'dashboard', 'chartplotsetting');
INSERT INTO `django_content_type` VALUES (16, 'dashboard', 'chartsetting');
INSERT INTO `django_content_type` VALUES (17, 'dashboard', 'chartstring');
INSERT INTO `django_content_type` VALUES (18, 'dashboard', 'indicator');
INSERT INTO `django_content_type` VALUES (19, 'dashboard', 'indicatorinput');
INSERT INTO `django_content_type` VALUES (20, 'dashboard', 'indicatorinputmembership');
INSERT INTO `django_content_type` VALUES (21, 'dashboard', 'indicatorinputvalue');
INSERT INTO `django_content_type` VALUES (22, 'dashboard', 'tradechartpattern');
INSERT INTO `django_content_type` VALUES (23, 'dashboard', 'tradeindicator');
INSERT INTO `django_content_type` VALUES (24, 'dashboard', 'tradeindicatorcross2');
INSERT INTO `django_content_type` VALUES (25, 'dashboard', 'tradeindicatorcrossv');
INSERT INTO `django_content_type` VALUES (26, 'dashboard', 'tradeindicatorindicator');
INSERT INTO `django_content_type` VALUES (27, 'dashboard', 'tradeindicatorplotthreshold');
INSERT INTO `django_content_type` VALUES (28, 'dashboard', 'tradepricebarpattern');
INSERT INTO `django_content_type` VALUES (6, 'dashboard', 'user');
INSERT INTO `django_content_type` VALUES (13, 'django_celery_results', 'taskresult');
INSERT INTO `django_content_type` VALUES (7, 'otp_static', 'staticdevice');
INSERT INTO `django_content_type` VALUES (8, 'otp_static', 'statictoken');
INSERT INTO `django_content_type` VALUES (9, 'otp_totp', 'totpdevice');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (10, 'two_factor', 'phonedevice');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2019-01-29 00:01:16.511327');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2019-01-29 00:01:17.311175');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2019-01-29 00:01:18.060586');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2019-01-29 00:01:18.196734');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2019-01-29 00:01:18.206706');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2019-01-29 00:01:18.218698');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2019-01-29 00:01:18.227650');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2019-01-29 00:01:18.234603');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2019-01-29 00:01:18.243580');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2019-01-29 00:01:18.252586');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2019-01-29 00:01:18.262529');
INSERT INTO `django_migrations` VALUES (12, 'dashboard', '0001_initial', '2019-01-29 00:01:19.664668');
INSERT INTO `django_migrations` VALUES (13, 'admin', '0001_initial', '2019-01-29 00:01:20.151055');
INSERT INTO `django_migrations` VALUES (14, 'admin', '0002_logentry_remove_auto_add', '2019-01-29 00:01:20.175696');
INSERT INTO `django_migrations` VALUES (15, 'admin', '0003_logentry_add_action_flag_choices', '2019-01-29 00:01:20.207833');
INSERT INTO `django_migrations` VALUES (16, 'otp_static', '0001_initial', '2019-01-29 00:01:20.905689');
INSERT INTO `django_migrations` VALUES (17, 'otp_totp', '0001_initial', '2019-01-29 00:01:21.233950');
INSERT INTO `django_migrations` VALUES (18, 'sessions', '0001_initial', '2019-01-29 00:01:21.441146');
INSERT INTO `django_migrations` VALUES (19, 'two_factor', '0001_initial', '2019-01-29 00:01:21.768020');
INSERT INTO `django_migrations` VALUES (20, 'two_factor', '0002_auto_20150110_0810', '2019-01-29 00:01:21.793787');
INSERT INTO `django_migrations` VALUES (21, 'two_factor', '0003_auto_20150817_1733', '2019-01-29 00:01:21.829228');
INSERT INTO `django_migrations` VALUES (22, 'two_factor', '0004_auto_20160205_1827', '2019-01-29 00:01:21.932509');
INSERT INTO `django_migrations` VALUES (23, 'two_factor', '0005_auto_20160224_0450', '2019-01-29 00:01:22.069277');
INSERT INTO `django_migrations` VALUES (24, 'core', '0001_initial', '2019-01-29 10:51:50.354898');
INSERT INTO `django_migrations` VALUES (25, 'core', '0002_tokenmetric', '2019-01-29 10:51:50.413847');
INSERT INTO `django_migrations` VALUES (26, 'core', '0003_rate_precision', '2019-01-29 10:51:50.536947');
INSERT INTO `django_migrations` VALUES (27, 'dashboard', '0002_remove_user_username', '2019-01-29 10:52:42.349147');
INSERT INTO `django_migrations` VALUES (28, 'django_celery_results', '0001_initial', '2019-01-30 18:28:10.649900');
INSERT INTO `django_migrations` VALUES (29, 'django_celery_results', '0002_add_task_name_args_kwargs', '2019-01-30 18:28:10.869294');
INSERT INTO `django_migrations` VALUES (30, 'django_celery_results', '0003_auto_20181106_1101', '2019-01-30 18:28:10.881260');
INSERT INTO `django_migrations` VALUES (31, 'dashboard', '0003_auto_20190308_0905', '2019-03-08 01:19:16.467906');
INSERT INTO `django_migrations` VALUES (32, 'dashboard', '0004_auto_20190308_0930', '2019-03-08 01:32:34.420381');
INSERT INTO `django_migrations` VALUES (33, 'dashboard', '0005_auto_20190308_1636', '2019-03-08 08:36:36.912388');
INSERT INTO `django_migrations` VALUES (34, 'dashboard', '0006_auto_20190308_1640', '2019-03-08 08:42:15.694023');
INSERT INTO `django_migrations` VALUES (35, 'dashboard', '0003_auto_20190308_1645', '2019-03-08 08:47:41.451104');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `session_data` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('01ykfgdasa9hydvea3bv0uax5a0y8ruj', 'YjAwYTJlOWZhOTlhYTM2ZGQyZDRlYWNiZjQ3MjZiMzYwNThhNWY5NDp7IndpemFyZF9sb2dpbl92aWV3Ijp7InN0ZXAiOiJhdXRoIiwic3RlcF9kYXRhIjp7fSwic3RlcF9maWxlcyI6e30sImV4dHJhX2RhdGEiOnt9LCJ2YWxpZGF0ZWRfc3RlcF9kYXRhIjp7fX19', '2019-02-12 09:34:08.969533');
INSERT INTO `django_session` VALUES ('pcsxoedy7sphj8fumb0r3zx340poknz6', 'YjAwYTJlOWZhOTlhYTM2ZGQyZDRlYWNiZjQ3MjZiMzYwNThhNWY5NDp7IndpemFyZF9sb2dpbl92aWV3Ijp7InN0ZXAiOiJhdXRoIiwic3RlcF9kYXRhIjp7fSwic3RlcF9maWxlcyI6e30sImV4dHJhX2RhdGEiOnt9LCJ2YWxpZGF0ZWRfc3RlcF9kYXRhIjp7fX19', '2019-02-12 09:06:11.687290');
INSERT INTO `django_session` VALUES ('su6dkt0m57qgy3nqj3yx86walokposez', 'MGU1OGZhYmE4ZTM0NjE2Nzk0NzhlYmI1MGE5YWM5OTQyOTVmNWM2ZTp7IndpemFyZF9sb2dpbl92aWV3Ijp7InN0ZXAiOiJhdXRoIiwic3RlcF9kYXRhIjp7fSwic3RlcF9maWxlcyI6e30sImV4dHJhX2RhdGEiOnt9LCJ2YWxpZGF0ZWRfc3RlcF9kYXRhIjp7fX0sIl9hdXRoX3VzZXJfaWQiOiIxMyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMzcxNTk2ZDE4N2M3ZjVhMGIwMGMxMDAyNWViZTA4MjAyYTMxMjFjNyJ9', '2019-02-14 09:18:12.906946');

-- ----------------------------
-- Table structure for indicator_input
-- ----------------------------
DROP TABLE IF EXISTS `indicator_input`;
CREATE TABLE `indicator_input`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parameter` varchar(256) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for indicator_input_value
-- ----------------------------
DROP TABLE IF EXISTS `indicator_input_value`;
CREATE TABLE `indicator_input_value`  (
  `id` int(11) NOT NULL,
  `trade_indicator_indicator_id` int(11) NULL DEFAULT NULL,
  `indicator_input_id` int(11) NULL DEFAULT NULL,
  `value` float(255, 0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for indicators
-- ----------------------------
DROP TABLE IF EXISTS `indicators`;
CREATE TABLE `indicators`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `id_letter` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `category` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `value_indicator` int(11) NOT NULL,
  `possible_combine` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 43 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of indicators
-- ----------------------------
INSERT INTO `indicators` VALUES (1, 'Awesome Oscillator', 'ao', 'Momentum', 0, 0);
INSERT INTO `indicators` VALUES (2, 'Chande Momentum Oscillator', 'cmo', 'Momentum', 1, 0);
INSERT INTO `indicators` VALUES (3, 'Coppock Curve', 'cc', 'Momentum', 0, 0);
INSERT INTO `indicators` VALUES (4, 'Momentum', 'mom', 'Momentum', 0, 0);
INSERT INTO `indicators` VALUES (5, 'Money Flow Index', 'mfi', 'Momentum', 1, 0);
INSERT INTO `indicators` VALUES (6, 'Price Oscillator', 'po', 'Momentum', 0, 1);
INSERT INTO `indicators` VALUES (7, 'Relative Strength Index', 'rsi', 'Momentum', 0, 1);
INSERT INTO `indicators` VALUES (8, 'Stochastic', 'stoch', 'Momentum', 0, 0);
INSERT INTO `indicators` VALUES (9, 'Stochastic RSI', 'stchrsi', 'Momentum', 0, 1);
INSERT INTO `indicators` VALUES (10, 'True Strength Index', 'tsi', 'Momentum', 0, 0);
INSERT INTO `indicators` VALUES (11, 'Ultimate Oscillator', 'uo', 'Momentum', 1, 0);
INSERT INTO `indicators` VALUES (12, 'Williams % R', 'wpr', 'Momentum', 0, 1);
INSERT INTO `indicators` VALUES (13, 'Aroon', 'aroon', 'Trend', 1, 0);
INSERT INTO `indicators` VALUES (14, 'Average Directional Index', 'adi', 'Trend', 1, 0);
INSERT INTO `indicators` VALUES (15, 'Commodity Channel Index', 'cci', 'Trend', 0, 0);
INSERT INTO `indicators` VALUES (16, 'Directional Movement Index', 'dmi', 'Trend', 0, 0);
INSERT INTO `indicators` VALUES (17, 'Double Exponential Moving Avearge', 'dema', 'Trend', 1, 0);
INSERT INTO `indicators` VALUES (18, 'Hull MA', 'hma', 'Trend', 1, 1);
INSERT INTO `indicators` VALUES (19, 'Ichimoku Cloud', 'ic', 'Trend', 1, 0);
INSERT INTO `indicators` VALUES (20, 'Know Sure Thing (KST) Oscillator', 'kst', 'Trend', 0, 0);
INSERT INTO `indicators` VALUES (21, 'MA Cross', 'macross', 'Trend', 0, 0);
INSERT INTO `indicators` VALUES (22, 'MACD', 'macd', 'Trend', 0, 1);
INSERT INTO `indicators` VALUES (23, 'Mass Index', 'mi', 'Trend', 1, 0);
INSERT INTO `indicators` VALUES (24, 'Moving Average Exponential', 'ema', 'Trend', 1, 1);
INSERT INTO `indicators` VALUES (25, 'Moving Average Simple', 'sma', 'Trend', 1, 0);
INSERT INTO `indicators` VALUES (26, 'Moving Average Weighted', 'wma', 'Trend', 1, 1);
INSERT INTO `indicators` VALUES (27, 'Smoothed Moving Average', 'smma', 'Trend', 1, 1);
INSERT INTO `indicators` VALUES (28, 'TRIX', 'trix', 'Trend', 0, 0);
INSERT INTO `indicators` VALUES (29, 'Triple EMA', 'tema', 'Trend', 1, 0);
INSERT INTO `indicators` VALUES (30, 'Vortex Indicator', 'voi', 'Trend', 0, 0);
INSERT INTO `indicators` VALUES (31, 'Average True Range', 'atr', 'Volatility', 0, 0);
INSERT INTO `indicators` VALUES (32, 'Bollinger Bands', 'bb', 'Volatility', 0, 1);
INSERT INTO `indicators` VALUES (33, 'Bollinger Bands % B', 'bb_pb', 'Volatility', 1, 0);
INSERT INTO `indicators` VALUES (34, 'Bollinger Bands Width', 'bb_bw', 'Volatility', 1, 0);
INSERT INTO `indicators` VALUES (35, 'Donchian Channels', 'dc', 'Volatility', 1, 0);
INSERT INTO `indicators` VALUES (36, 'Keltner Channels', 'kc', 'Volatility', 0, 1);
INSERT INTO `indicators` VALUES (37, 'Accumulation Distribution Index', 'acc', 'Volume', 1, 0);
INSERT INTO `indicators` VALUES (38, 'Chaikin Money Flow', 'cmf', 'Volume', 1, 0);
INSERT INTO `indicators` VALUES (39, 'Chaikin Oscillator', 'co', 'Volume', 1, 0);
INSERT INTO `indicators` VALUES (40, 'Ease of Movement', 'eom', 'Volume', 1, 0);
INSERT INTO `indicators` VALUES (41, 'On Balance Volume', 'obv', 'Volume', 1, 0);
INSERT INTO `indicators` VALUES (42, 'Volume', 'volume', 'Volume', 1, 0);

-- ----------------------------
-- Table structure for indicators1
-- ----------------------------
DROP TABLE IF EXISTS `indicators1`;
CREATE TABLE `indicators1`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `id_letter` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `category` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `value_indicator` int(1) NULL DEFAULT NULL,
  `possible_combine` int(2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 43 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of indicators1
-- ----------------------------
INSERT INTO `indicators1` VALUES (1, 'Awesome Oscillator', 'ao', 'Momentum', 0, NULL);
INSERT INTO `indicators1` VALUES (2, 'Chande Momentum Oscillator', 'cmo', 'Momentum', 1, 0);
INSERT INTO `indicators1` VALUES (3, 'Coppock Curve', 'cc', 'Momentum', 0, NULL);
INSERT INTO `indicators1` VALUES (4, 'Momentum', 'mom', 'Momentum', 0, 0);
INSERT INTO `indicators1` VALUES (5, 'Money Flow Index', 'mfi', 'Momentum', 1, NULL);
INSERT INTO `indicators1` VALUES (6, 'Price Oscillator', 'po', 'Momentum', 0, 1);
INSERT INTO `indicators1` VALUES (7, 'Relative Strength Index', 'rsi', 'Momentum', 0, 1);
INSERT INTO `indicators1` VALUES (8, 'Stochastic', 'stoch', 'Momentum', 0, NULL);
INSERT INTO `indicators1` VALUES (9, 'Stochastic RSI', 'stchrsi', 'Momentum', 0, 1);
INSERT INTO `indicators1` VALUES (10, 'True Strength Index', 'tsi', 'Momentum', 0, NULL);
INSERT INTO `indicators1` VALUES (11, 'Ultimate Oscillator', 'uo', 'Momentum', 1, NULL);
INSERT INTO `indicators1` VALUES (12, 'Williams % R', 'wpr', 'Momentum', 0, 1);
INSERT INTO `indicators1` VALUES (13, 'Aroon', 'aroon', 'Trend', 1, NULL);
INSERT INTO `indicators1` VALUES (14, 'Average Directional Index', 'adi', 'Trend', 1, NULL);
INSERT INTO `indicators1` VALUES (15, 'Commodity Channel Index', 'cci', 'Trend', 0, 0);
INSERT INTO `indicators1` VALUES (16, 'Directional Movement Index', 'dmi', 'Trend', 0, NULL);
INSERT INTO `indicators1` VALUES (17, 'Double Exponential Moving Avearge', 'dema', 'Trend', 1, NULL);
INSERT INTO `indicators1` VALUES (18, 'Hull MA', 'hma', 'Trend', 1, 1);
INSERT INTO `indicators1` VALUES (19, 'Ichimoku Cloud', 'ic', 'Trend', 1, NULL);
INSERT INTO `indicators1` VALUES (20, 'Know Sure Thing (KST) Oscillator', 'kst', 'Trend', 0, NULL);
INSERT INTO `indicators1` VALUES (21, 'MA Cross', 'macross', 'Trend', 0, NULL);
INSERT INTO `indicators1` VALUES (22, 'MACD', 'macd', 'Trend', 0, 1);
INSERT INTO `indicators1` VALUES (23, 'Mass Index', 'mi', 'Trend', 1, NULL);
INSERT INTO `indicators1` VALUES (24, 'Moving Average Exponential', 'ema', 'Trend', 1, 1);
INSERT INTO `indicators1` VALUES (25, 'Moving Average Simple', 'sma', 'Trend', 1, NULL);
INSERT INTO `indicators1` VALUES (26, 'Moving Average Weighted', 'wma', 'Trend', 1, 1);
INSERT INTO `indicators1` VALUES (27, 'Smoothed Moving Average', 'smma', 'Trend', 1, 1);
INSERT INTO `indicators1` VALUES (28, 'TRIX', 'trix', 'Trend', 0, NULL);
INSERT INTO `indicators1` VALUES (29, 'Triple EMA', 'tema', 'Trend', 1, NULL);
INSERT INTO `indicators1` VALUES (30, 'Vortex Indicator', 'voi', 'Trend', 0, NULL);
INSERT INTO `indicators1` VALUES (31, 'Average True Range', 'atr', 'Volatility', 0, NULL);
INSERT INTO `indicators1` VALUES (32, 'Bollinger Bands', 'bb', 'Volatility', 0, 1);
INSERT INTO `indicators1` VALUES (33, 'Bollinger Bands % B', 'bb_pb', 'Volatility', 1, 0);
INSERT INTO `indicators1` VALUES (34, 'Bollinger Bands Width', 'bb_bw', 'Volatility', 1, 0);
INSERT INTO `indicators1` VALUES (35, 'Donchian Channels', 'dc', 'Volatility', 1, NULL);
INSERT INTO `indicators1` VALUES (36, 'Keltner Channels', 'kc', 'Volatility', 0, 1);
INSERT INTO `indicators1` VALUES (37, 'Accumulation Distribution Index', 'acc', 'Volume', 1, NULL);
INSERT INTO `indicators1` VALUES (38, 'Chaikin Money Flow', 'cmf', 'Volume', 1, NULL);
INSERT INTO `indicators1` VALUES (39, 'Chaikin Oscillator', 'co', 'Volume', 1, NULL);
INSERT INTO `indicators1` VALUES (40, 'Ease of Movement', 'eom', 'Volume', 1, NULL);
INSERT INTO `indicators1` VALUES (41, 'On Balance Volume', 'obv', 'Volume', 1, NULL);
INSERT INTO `indicators1` VALUES (42, 'Volume', 'volume', 'Volume', 1, NULL);

-- ----------------------------
-- Table structure for indicators_indicatorinputs
-- ----------------------------
DROP TABLE IF EXISTS `indicators_indicatorinputs`;
CREATE TABLE `indicators_indicatorinputs`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `indicator_id` int(11) NOT NULL,
  `indicatorinput_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `indicators_indicatorinpu_indicator_id_indicatorin_649ea465_uniq`(`indicator_id`, `indicatorinput_id`) USING BTREE,
  INDEX `indicators_indicator_indicatorinput_id_4b2534a8_fk_indicator`(`indicatorinput_id`) USING BTREE,
  CONSTRAINT `indicators_indicator_indicator_id_0766593b_fk_indicator` FOREIGN KEY (`indicator_id`) REFERENCES `indicators` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `indicators_indicator_indicatorinput_id_4b2534a8_fk_indicator` FOREIGN KEY (`indicatorinput_id`) REFERENCES `indicator_input` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for otp_static_staticdevice
-- ----------------------------
DROP TABLE IF EXISTS `otp_static_staticdevice`;
CREATE TABLE `otp_static_staticdevice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `otp_static_staticdevice_user_id_7f9cff2b_fk_dashboard_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `otp_static_staticdevice_user_id_7f9cff2b_fk_dashboard_user_id` FOREIGN KEY (`user_id`) REFERENCES `dashboard_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for otp_static_statictoken
-- ----------------------------
DROP TABLE IF EXISTS `otp_static_statictoken`;
CREATE TABLE `otp_static_statictoken`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `device_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `otp_static_statictok_device_id_74b7c7d1_fk_otp_stati`(`device_id`) USING BTREE,
  INDEX `otp_static_statictoken_token_d0a51866`(`token`) USING BTREE,
  CONSTRAINT `otp_static_statictok_device_id_74b7c7d1_fk_otp_stati` FOREIGN KEY (`device_id`) REFERENCES `otp_static_staticdevice` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for otp_totp_totpdevice
-- ----------------------------
DROP TABLE IF EXISTS `otp_totp_totpdevice`;
CREATE TABLE `otp_totp_totpdevice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `key` varchar(80) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `step` smallint(5) UNSIGNED NOT NULL,
  `t0` bigint(20) NOT NULL,
  `digits` smallint(5) UNSIGNED NOT NULL,
  `tolerance` smallint(5) UNSIGNED NOT NULL,
  `drift` smallint(6) NOT NULL,
  `last_t` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `otp_totp_totpdevice_user_id_0fb18292_fk_dashboard_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `otp_totp_totpdevice_user_id_0fb18292_fk_dashboard_user_id` FOREIGN KEY (`user_id`) REFERENCES `dashboard_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for trade_chart_pattern
-- ----------------------------
DROP TABLE IF EXISTS `trade_chart_pattern`;
CREATE TABLE `trade_chart_pattern`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `chart_pattern` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for trade_indicator
-- ----------------------------
DROP TABLE IF EXISTS `trade_indicator`;
CREATE TABLE `trade_indicator`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `trade_mode` int(2) NULL DEFAULT NULL COMMENT '0: original way 1: threshold 2: cross',
  `with_main` int(2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of trade_indicator
-- ----------------------------
INSERT INTO `trade_indicator` VALUES (1, NULL, 0, 0);

-- ----------------------------
-- Table structure for trade_indicator_cross2
-- ----------------------------
DROP TABLE IF EXISTS `trade_indicator_cross2`;
CREATE TABLE `trade_indicator_cross2`  (
  `id` int(11) NOT NULL,
  `trade_indicator_indicator1_id` int(11) NULL DEFAULT NULL,
  `chart_plot1_id` int(11) NULL DEFAULT NULL,
  `trade_indicator_indicator2_id` int(11) NULL DEFAULT NULL,
  `chart_plot2_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for trade_indicator_crossv
-- ----------------------------
DROP TABLE IF EXISTS `trade_indicator_crossv`;
CREATE TABLE `trade_indicator_crossv`  (
  `id` int(11) NOT NULL,
  `trade_indicator_indicator_id` int(11) NULL DEFAULT NULL,
  `chart_plot_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for trade_indicator_indicator
-- ----------------------------
DROP TABLE IF EXISTS `trade_indicator_indicator`;
CREATE TABLE `trade_indicator_indicator`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trade_indicator_id` int(11) NULL DEFAULT NULL,
  `indicator_id` int(11) NULL DEFAULT NULL,
  `traditional` int(2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of trade_indicator_indicator
-- ----------------------------
INSERT INTO `trade_indicator_indicator` VALUES (1, 1, 1, NULL);

-- ----------------------------
-- Table structure for trade_indicator_plot_threshold
-- ----------------------------
DROP TABLE IF EXISTS `trade_indicator_plot_threshold`;
CREATE TABLE `trade_indicator_plot_threshold`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trade_indicator_indicator_id` int(11) NULL DEFAULT NULL,
  `plot_id` int(11) NULL DEFAULT NULL,
  `threshold` float(11, 0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for trade_pricebar_pattern
-- ----------------------------
DROP TABLE IF EXISTS `trade_pricebar_pattern`;
CREATE TABLE `trade_pricebar_pattern`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `pricebar_pattern` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for two_factor_phonedevice
-- ----------------------------
DROP TABLE IF EXISTS `two_factor_phonedevice`;
CREATE TABLE `two_factor_phonedevice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `confirmed` tinyint(1) NOT NULL,
  `number` varchar(128) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `key` varchar(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `method` varchar(4) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `two_factor_phonedevice_user_id_54718003_fk_dashboard_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `two_factor_phonedevice_user_id_54718003_fk_dashboard_user_id` FOREIGN KEY (`user_id`) REFERENCES `dashboard_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
