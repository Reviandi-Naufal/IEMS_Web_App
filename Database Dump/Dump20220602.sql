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
-- Table structure for table `billinginput`
--

DROP TABLE IF EXISTS `billinginput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billinginput` (
  `user_id_bill` int NOT NULL,
  `tarif_listrik` varchar(50) DEFAULT NULL,
  `tagihan_listrik` int DEFAULT NULL,
  PRIMARY KEY (`user_id_bill`),
  CONSTRAINT `billinginput_ibfk_1` FOREIGN KEY (`user_id_bill`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billinginput`
--

LOCK TABLES `billinginput` WRITE;
/*!40000 ALTER TABLE `billinginput` DISABLE KEYS */;
INSERT INTO `billinginput` VALUES (2,'1300',1000000),(4,'900',700000);
/*!40000 ALTER TABLE `billinginput` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_status`
--

DROP TABLE IF EXISTS `device_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_status` (
  `device_id` text,
  `device_name` text,
  `device_status` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_status`
--

LOCK TABLES `device_status` WRITE;
/*!40000 ALTER TABLE `device_status` DISABLE KEYS */;
INSERT INTO `device_status` VALUES ('5','IEMS-3-001',1),('6','IEMS-3-002',1),('3','6281214382436',1),('31','IEMS-1-003',1),('7','IEMS-3-003',1);
/*!40000 ALTER TABLE `device_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deviceinput`
--

DROP TABLE IF EXISTS `deviceinput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deviceinput` (
  `user_id` int NOT NULL,
  `device_id` int NOT NULL,
  `device_name` varchar(50) NOT NULL,
  `daya_device` float NOT NULL,
  `jumlah_device` int NOT NULL,
  `total_daya` float NOT NULL,
  `tingkat_prioritas` varchar(50) NOT NULL,
  PRIMARY KEY (`device_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deviceinput`
--

LOCK TABLES `deviceinput` WRITE;
/*!40000 ALTER TABLE `deviceinput` DISABLE KEYS */;
INSERT INTO `deviceinput` VALUES (4,3,'Lampu',0.01,8,0.08,'Medium'),(2,5,'Kipas',0.3,5,1.5,'Medium'),(2,6,'Komputer',0.6,1,0.6,'Very High');
/*!40000 ALTER TABLE `deviceinput` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `image_file` varchar(20) NOT NULL,
  `password` varchar(60) NOT NULL,
  `user_type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','admin@gmail.com','default.jpg','$2b$12$viWMIofAp3IhVn7KyuBAd.Bf5Tovdi8XRTNuG0ioRfnZMAnSxn7OK','admin'),(2,'reviandi','reviandi@demo.com','default.jpg','$2b$12$STwn4OUf4Cc3ZV6rU1Kg8uS0tXYJs.mOx7TkrGxgaKAlidCN46zTS','user'),(4,'Rani','rani@demo.com','default.jpg','$2b$12$EcNurOq8lHoM6z6Z67WHB.I7dnI4OVPIcQVqDTfKasMma88CERz0C','user'),(5,'Joni','joni@demo.com','default.jpg','$2b$12$WFua.KKBXLtGWGQngO5BUeZJsGM1.ntQdjvV17qQl2sBdF3UnWzlS','user');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-02 19:18:18
