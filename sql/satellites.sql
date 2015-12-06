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
-- Table structure for table `satellites`
--

DROP TABLE IF EXISTS `satellites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `satellites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `IP` varchar(45) DEFAULT NULL,
  `PORT` int(11) DEFAULT NULL,
  `Type` varchar(45) NOT NULL,
  `USER` varchar(45) DEFAULT NULL,
  `PASS` varchar(45) DEFAULT NULL,
  `command_set` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `satellites`
--

LOCK TABLES `satellites` WRITE;
/*!40000 ALTER TABLE `satellites` DISABLE KEYS */;
INSERT INTO `satellites` VALUES (1,'Router','192.168.192.1',0,'Router','','','Router'),(2,'BettPi','192.168.192.24',5000,'sat','pi','raspberry','BettPi'),(3,'TVPi','192.168.192.25',5000,'sat','pi','raspberry','TVPi'),(4,'TuerSPi','192.168.192.32',5000,'sat','pi','raspberry','TuerSPi'),(5,'BueroPi','192.168.192.33',5010,'virt','pi','raspberry','BueroPi'),(6,'LightstripSchlafzi','192.168.192.24',5000,'virt','pi','raspberry','LightstripSchlafzi'),(7,'Marantz','192.168.192.25',5010,'virt','pi','raspberry','Marantz'),(8,'Sideb_oben','192.168.192.25',5010,'virt','pi','raspberry','Sideboard'),(9,'Sideb_links','192.168.192.25',5010,'virt','pi','raspberry','Sideboard'),(10,'Sideb_mitte','192.168.192.25',5010,'virt','pi','raspberry','Sideboard'),(11,'Sideb_rechts','192.168.192.25',5010,'virt','pi','raspberry','Sideboard');
/*!40000 ALTER TABLE `satellites` ENABLE KEYS */;
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
