/*
Navicat MySQL Data Transfer

Source Server         : testqa
Source Server Version : 50725
Source Host           : www.testqa.cn:3306
Source Database       : sdet

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2021-02-23 21:08:33
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for hook
-- ----------------------------
DROP TABLE IF EXISTS `hook`;
CREATE TABLE `hook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` enum('RESPONSE','REQUEST') NOT NULL,
  `source` varchar(30) NOT NULL,
  `target` varchar(30) NOT NULL,
  `content` text NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_type_uniq_idx` (`name`,`type`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for http_api
-- ----------------------------
DROP TABLE IF EXISTS `http_api`;
CREATE TABLE `http_api` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `url` varchar(1024) NOT NULL,
  `method` varchar(10) NOT NULL,
  `body` longtext,
  `fileList` text,
  `headers` varchar(2048) DEFAULT NULL,
  `validate` enum('express','contain','equal') NOT NULL COMMENT '检查关键字',
  `express` longtext COMMENT '检查规则内容',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0: 未执行，1: 通过，2: 失败, 3: 异常',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for http_api_log
-- ----------------------------
DROP TABLE IF EXISTS `http_api_log`;
CREATE TABLE `http_api_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_id` int(11) NOT NULL COMMENT '用例id',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '运行结果, 1: 通过，2: 失败，3: 异常',
  `content` longtext COMMENT '日志内容',
  `created_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for http_mock
-- ----------------------------
DROP TABLE IF EXISTS `http_mock`;
CREATE TABLE `http_mock` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) DEFAULT NULL COMMENT 'Mock配置唯一键',
  `code` int(11) DEFAULT NULL COMMENT 'Mock响应码',
  `headers` varchar(1000) DEFAULT NULL COMMENT 'Mock响应头',
  `data` longtext COMMENT 'Mock响应体',
  `no_pattern_response` varchar(255) DEFAULT NULL COMMENT '无匹配内容时响应模式',
  `type` varchar(25) NOT NULL DEFAULT '' COMMENT '响应体类型。text：纯文本，dynamic：参数化，express：Python表达式',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for todo
-- ----------------------------
DROP TABLE IF EXISTS `todo`;
CREATE TABLE `todo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '任务名称',
  `desc` varchar(255) DEFAULT NULL COMMENT '任务描述',
  `start_time` date DEFAULT NULL COMMENT '执行开始时间',
  `end_time` date DEFAULT NULL COMMENT '执行结束时间',
  `assign` varchar(50) NOT NULL COMMENT '执行人',
  `status` enum('DISCARD','FINISHED','INPROCESS','INIT') NOT NULL DEFAULT 'INIT' COMMENT '状态',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_del` tinyint(1) DEFAULT '0' COMMENT '逻辑删除标识。0：未删除，1：已删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
