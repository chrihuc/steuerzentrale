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
-- Table structure for table `Marantz`
--

DROP TABLE IF EXISTS `Marantz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Marantz` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Power` varchar(45) DEFAULT NULL,
  `Volume` varchar(45) DEFAULT NULL,
  `Source` varchar(45) DEFAULT NULL,
  `Mute` varchar(45) DEFAULT NULL,
  `Display` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Marantz`
--

LOCK TABLES `Marantz` WRITE;
/*!40000 ALTER TABLE `Marantz` DISABLE KEYS */;
INSERT INTO `Marantz` VALUES (1,'An','True',NULL,NULL,NULL,NULL),(2,'Aus','False',NULL,NULL,NULL,NULL),(3,'TV','True','0-25','11',NULL,NULL),(4,'RaspBMC','True',NULL,'99',NULL,NULL),(5,'Return','True','0-30','CC','False',NULL),(6,'Sonos','True','0-30','CC',NULL,NULL),(7,'Stumm','True',NULL,NULL,'2',NULL),(8,'unStumm','True',NULL,NULL,'1',NULL),(9,'Aktuell','True','0-17','11','False',NULL),(10,'PS3','True','0-25','22',NULL,NULL),(11,'Durchsage','True','0-25','CC',NULL,NULL),(12,'DisplayAn',NULL,NULL,NULL,NULL,'1'),(13,'DisplayAus',NULL,NULL,NULL,NULL,'4');
/*!40000 ALTER TABLE `Marantz` ENABLE KEYS */;
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
