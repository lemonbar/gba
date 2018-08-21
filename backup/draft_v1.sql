-- MySQL dump 10.13  Distrib 8.0.12, for Linux (x86_64)
--
-- Host: localhost    Database: gba
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `MATCH`
--

DROP TABLE IF EXISTS `MATCH`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `MATCH` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_date` datetime DEFAULT NULL,
  `home_team_id` int(11) NOT NULL,
  `away_team_id` int(11) NOT NULL,
  `home_team_score` int(11) DEFAULT NULL,
  `away_team_score` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `home_team_id` (`home_team_id`),
  KEY `away_team_id` (`away_team_id`),
  CONSTRAINT `MATCH_ibfk_1` FOREIGN KEY (`home_team_id`) REFERENCES `TEAM` (`id`),
  CONSTRAINT `MATCH_ibfk_2` FOREIGN KEY (`away_team_id`) REFERENCES `TEAM` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MATCH`
--

LOCK TABLES `MATCH` WRITE;
/*!40000 ALTER TABLE `MATCH` DISABLE KEYS */;
INSERT INTO `MATCH` VALUES (4,'2018-08-04 08:48:10',3,4,7,3),(5,'2018-08-04 08:48:28',3,2,6,7),(6,'2018-08-04 08:48:57',2,1,7,2),(7,'2018-08-04 08:49:25',2,4,7,5),(8,'2018-08-04 08:49:38',2,3,5,7),(9,'2018-08-04 08:49:54',3,1,7,6),(10,'2018-08-04 08:50:10',3,4,2,7),(11,'2018-08-04 08:50:26',4,2,7,3),(12,'2018-08-04 08:50:41',4,1,7,3),(13,'2018-08-04 08:50:51',4,3,3,7),(14,'2018-08-04 08:51:03',3,2,4,7),(15,'2018-08-04 08:51:18',2,1,7,6),(16,'2018-08-04 08:51:32',2,4,2,7),(17,'2018-08-04 08:51:58',4,3,6,7),(18,'2018-08-04 08:52:14',3,1,6,7),(19,'2018-07-28 13:52:35',2,3,8,2),(20,'2018-07-28 13:52:56',2,1,7,8),(21,'2018-07-28 13:53:13',1,3,8,4),(22,'2018-07-28 13:53:26',1,2,4,8),(23,'2018-07-28 13:53:42',2,3,8,6),(24,'2018-07-28 13:54:12',2,1,6,8),(25,'2018-07-28 13:54:29',1,3,0,8),(26,'2018-07-28 13:54:48',3,2,5,8),(27,'2018-07-28 13:55:05',2,1,6,8),(28,'2018-07-28 13:55:24',1,3,8,6);
/*!40000 ALTER TABLE `MATCH` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MATCH_BONUS`
--

DROP TABLE IF EXISTS `MATCH_BONUS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `MATCH_BONUS` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `reason` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `MATCH_BONUS_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `TEAM` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MATCH_BONUS`
--

LOCK TABLES `MATCH_BONUS` WRITE;
/*!40000 ALTER TABLE `MATCH_BONUS` DISABLE KEYS */;
/*!40000 ALTER TABLE `MATCH_BONUS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MATCH_DETAIL`
--

DROP TABLE IF EXISTS `MATCH_DETAIL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `MATCH_DETAIL` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` int(11) NOT NULL,
  `player_id` int(11) NOT NULL,
  `foul` int(11) DEFAULT NULL,
  `two_point` int(11) DEFAULT NULL,
  `three_point` int(11) DEFAULT NULL,
  `free_throw` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MATCH_DETAIL`
--

LOCK TABLES `MATCH_DETAIL` WRITE;
/*!40000 ALTER TABLE `MATCH_DETAIL` DISABLE KEYS */;
/*!40000 ALTER TABLE `MATCH_DETAIL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PLAYER`
--

DROP TABLE IF EXISTS `PLAYER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `PLAYER` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) DEFAULT NULL,
  `name` varchar(80) NOT NULL,
  `salary` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `PLAYER_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `TEAM` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PLAYER`
--

LOCK TABLES `PLAYER` WRITE;
/*!40000 ALTER TABLE `PLAYER` DISABLE KEYS */;
INSERT INTO `PLAYER` VALUES (1,2,'李盟',1500),(3,NULL,'向心力',1100),(4,NULL,'高潘',800);
/*!40000 ALTER TABLE `PLAYER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TEAM`
--

DROP TABLE IF EXISTS `TEAM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `TEAM` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TEAM`
--

LOCK TABLES `TEAM` WRITE;
/*!40000 ALTER TABLE `TEAM` DISABLE KEYS */;
INSERT INTO `TEAM` VALUES (4,'X战队'),(2,'北极熊'),(3,'蓝灵'),(1,'黑曼巴');
/*!40000 ALTER TABLE `TEAM` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-10 15:59:21
