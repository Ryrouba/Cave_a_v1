-- Structure de la base de données cave_a_v1

DROP TABLE IF EXISTS `bottles`;
CREATE TABLE `bottles` (
  `bottle_id` int NOT NULL AUTO_INCREMENT,
  `shelf_id` int NOT NULL,
  `winery` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `year` int NOT NULL,
  `region` varchar(255) NOT NULL,
  `comments` text,
  `personal_rating` decimal(3,1) DEFAULT NULL,
  `community_rating` decimal(3,1) DEFAULT NULL,
  `label_photo` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`bottle_id`),
  KEY `shelf_id` (`shelf_id`),
  CONSTRAINT `bottles_ibfk_1` FOREIGN KEY (`shelf_id`) REFERENCES `shelves` (`shelf_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `caves`;
CREATE TABLE `caves` (
  `cave_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `cave_name` varchar(255) NOT NULL,
  PRIMARY KEY (`cave_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `caves_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `shelves`;
CREATE TABLE `shelves` (
  `shelf_id` int NOT NULL AUTO_INCREMENT,
  `cave_id` int NOT NULL,
  `shelf_name` varchar(255) NOT NULL,
  `shelf_number` int NOT NULL,
  `region` varchar(255) NOT NULL,
  `available_slots` int NOT NULL,
  `bottles_per_shelf` int NOT NULL,
  PRIMARY KEY (`shelf_id`),
  UNIQUE KEY `unique_shelf_number_per_cave` (`cave_id`, `shelf_number`),
  CONSTRAINT `shelves_ibfk_1` FOREIGN KEY (`cave_id`) REFERENCES `caves` (`cave_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

