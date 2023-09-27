create database demo;
use demo;
CREATE USER 'demo'@'localhost' IDENTIFIED BY 'pleasesubscribe';
GRANT ALL PRIVILEGES ON demo.* TO 'demo'@'localhost';
FLUSH PRIVILEGES;

DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(32) DEFAULT NULL,
  `body` text,
  `author_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
); 
INSERT INTO `posts` VALUES (1,'Please Subscribe','To my channel',1);

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(128) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO `users` VALUES (1,'ippsec','$2b$12$poLViz9Y.eqTySckpeukI.k3ASSJ/OG3k/YklyFLbGxE43H4DD/h6','root@ippsec.rocks');

