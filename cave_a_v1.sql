mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 8.3.0, for Linux (aarch64)
--
-- Host: localhost    Database: cave_a_v1
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bottles`
--

DROP TABLE IF EXISTS `bottles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bottles`
--

LOCK TABLES `bottles` WRITE;
/*!40000 ALTER TABLE `bottles` DISABLE KEYS */;
INSERT INTO `bottles` VALUES (1,30,'Domaine Romanée-Conti','Romanée-Conti','Vin Rouge',2016,'Bourgogne','Très Rouge',17.0,15.0,'https://raw.githubusercontent.com/Ryrouba/Cave_a_v1/main/static/images/romanee-conti-2016.png',2000.00),(2,30,'Château Yquem','Château Yquem','Vin blanc liquoreux',2017,'Sauternes','Fruité',20.0,19.0,'https://raw.githubusercontent.com/Ryrouba/Cave_a_v1/7f99034b1388058b2847226c6995d6a73f24fc82/static/images/Chateau-Yquem.png',220.00),(3,30,'Veuve Clicquot','Brut Carte Jaune','Champagne',1972,'Champagne','petillant',16.0,18.0,'https://raw.githubusercontent.com/Ryrouba/Cave_a_v1/7f99034b1388058b2847226c6995d6a73f24fc82/static/images/veuve_cliquot.png',50.00),(4,32,'Domaine Leroy','Musigny Grand Cru','Vin rouge',2015,'Bourgogne','Raffiné',17.0,16.0,'https://raw.githubusercontent.com/Ryrouba/Cave_a_v1/main/static/images/musigny-grand-cru.jpeg',3.00);
/*!40000 ALTER TABLE `bottles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `caves`
--

DROP TABLE IF EXISTS `caves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `caves` (
  `cave_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `cave_name` varchar(255) NOT NULL,
  PRIMARY KEY (`cave_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `caves_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caves`
--

LOCK TABLES `caves` WRITE;
/*!40000 ALTER TABLE `caves` DISABLE KEYS */;
INSERT INTO `caves` VALUES (40,36,'cave5'),(41,35,'cave1'),(47,35,'cave 2');
/*!40000 ALTER TABLE `caves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shelves`
--

DROP TABLE IF EXISTS `shelves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shelves` (
  `shelf_id` int NOT NULL AUTO_INCREMENT,
  `cave_id` int NOT NULL,
  `shelf_name` varchar(255) NOT NULL,
  `shelf_number` int NOT NULL,
  `region` varchar(255) NOT NULL,
  `available_slots` int NOT NULL,
  `bottles_per_shelf` int NOT NULL,
  PRIMARY KEY (`shelf_id`),
  UNIQUE KEY `unique_shelf_number_per_cave` (`cave_id`,`shelf_number`),
  CONSTRAINT `shelves_ibfk_1` FOREIGN KEY (`cave_id`) REFERENCES `caves` (`cave_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shelves`
--

LOCK TABLES `shelves` WRITE;
/*!40000 ALTER TABLE `shelves` DISABLE KEYS */;
INSERT INTO `shelves` VALUES (30,41,'Etage 1',1,'savoie',7,3),(32,47,'Etage 2-1',1,'Savoie',4,2);
/*!40000 ALTER TABLE `shelves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (35,'ryan','ryan'),(36,'colin','colin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-17 12:27:49
