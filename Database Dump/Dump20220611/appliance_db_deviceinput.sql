-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: appliance_db
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `deviceinput`
--

DROP TABLE IF EXISTS `deviceinput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deviceinput` (
  `user_id` int DEFAULT NULL,
  `username` varchar(20) NOT NULL,
  `device_id` int NOT NULL AUTO_INCREMENT,
  `device_name` varchar(100) DEFAULT NULL,
  `daya_device` float DEFAULT NULL,
  `jumlah_device` int DEFAULT NULL,
  `total_daya` float DEFAULT NULL,
  `tingkat_prioritas` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`device_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deviceinput`
--

LOCK TABLES `deviceinput` WRITE;
/*!40000 ALTER TABLE `deviceinput` DISABLE KEYS */;
INSERT INTO `deviceinput` VALUES (2,'reviandi',1,'Komputer A',0.6,1,0.6,'Very High'),(2,'reviandi',2,'Komputer B',0.3,1,0.3,'Very High'),(2,'reviandi',3,'Stopkontak 5 Lubang',0.45,1,0.45,'High'),(2,'reviandi',4,'Printer',0.011,1,0.011,'High'),(2,'reviandi',5,'3D Printer',0.27,1,0.27,'Medium'),(2,'reviandi',6,'Dispenser',0.35,1,0.35,'Medium'),(2,'reviandi',7,'Lampu TL A 10W',0.01,8,0.08,'Low'),(2,'reviandi',8,'Stopkontak 3 Lubang',0.35,1,0.35,'Low'),(2,'reviandi',9,'LCD Proyektor',0.195,1,0.195,'Very Low'),(2,'reviandi',10,'Lampu TL B 10W',0.01,4,0.04,'Very Low'),(1,'admin',12,'Kipas',0.1,3,0.3,'High'),(1,'admin',24,'Televisi',0.4,1,0.4,'Low');
/*!40000 ALTER TABLE `deviceinput` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-11 16:55:21
