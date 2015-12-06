-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: XS1DB
-- ------------------------------------------------------
-- Server version	5.5.44-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tc_status`
--

DROP TABLE IF EXISTS `tc_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_status` (
  `idtc_status` int(11) NOT NULL,
  `tc_value` varchar(45) DEFAULT NULL,
  `tc_table` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtc_status`),
  UNIQUE KEY `tc_status_UNIQUE` (`tc_value`),
  UNIQUE KEY `tc_table_UNIQUE` (`tc_table`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_status`
--

LOCK TABLES `tc_status` WRITE;
/*!40000 ALTER TABLE `tc_status` DISABLE KEYS */;
INSERT INTO `tc_status` VALUES (0,'Wach','tc_wach'),(1,'Schlafen','tc_schlafen'),(2,'Am Schlafen gehen','tc_schlafen_gehen'),(3,'Wecken','tc_wecken'),(4,'Schlummern','tc_schlummern'),(5,'einer_wach','tc_einer_wach'),(6,'Urlaub','tc_urlaub'),(7,'Gegangen','tc_gegangen'),(8,'Am Gehen','tc_am_gehen'),(9,'Abwesend','tc_abwesend');
/*!40000 ALTER TABLE `tc_status` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-06 16:52:56
