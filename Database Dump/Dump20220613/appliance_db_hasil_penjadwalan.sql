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
-- Table structure for table `hasil_penjadwalan`
--

DROP TABLE IF EXISTS `hasil_penjadwalan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hasil_penjadwalan` (
  `user_id` bigint DEFAULT NULL,
  `device_id` bigint DEFAULT NULL,
  `durasi` int DEFAULT NULL,
  `tanggal` text,
  `waktu` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hasil_penjadwalan`
--

LOCK TABLES `hasil_penjadwalan` WRITE;
/*!40000 ALTER TABLE `hasil_penjadwalan` DISABLE KEYS */;
INSERT INTO `hasil_penjadwalan` VALUES (1,12,19,'11-06-2022','17:05:28'),(1,24,9,'11-06-2022','17:05:28'),(2,1,24,'11-06-2022','17:05:29'),(2,2,24,'11-06-2022','17:05:29'),(2,3,19,'11-06-2022','17:05:29'),(2,4,19,'11-06-2022','17:05:29'),(2,5,14,'11-06-2022','17:05:29'),(2,6,12,'11-06-2022','17:05:29'),(2,7,9,'11-06-2022','17:05:29'),(2,8,6,'11-06-2022','17:05:29'),(2,9,1,'11-06-2022','17:05:29'),(2,10,4,'11-06-2022','17:05:29');
/*!40000 ALTER TABLE `hasil_penjadwalan` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-13 13:50:22
