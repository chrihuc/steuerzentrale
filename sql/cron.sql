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
-- Table structure for table `cron`
--

DROP TABLE IF EXISTS `cron`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cron` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Bedingung` varchar(45) DEFAULT NULL,
  `Permanent` tinyint(4) DEFAULT '0',
  `Mo` tinyint(1) DEFAULT NULL,
  `Tu` tinyint(1) DEFAULT NULL,
  `Wed` tinyint(1) DEFAULT NULL,
  `Th` tinyint(1) DEFAULT NULL,
  `Fr` tinyint(1) DEFAULT NULL,
  `Sa` tinyint(1) DEFAULT NULL,
  `Su` tinyint(1) DEFAULT NULL,
  `Enabled` tinyint(4) DEFAULT NULL,
  `Sonne` varchar(45) DEFAULT NULL,
  `offset` varchar(45) DEFAULT NULL,
  `Zufall` varchar(45) DEFAULT NULL,
  `Rohtime` time DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cron`
--

LOCK TABLES `cron` WRITE;
/*!40000 ALTER TABLE `cron` DISABLE KEYS */;
INSERT INTO `cron` VALUES (1,'Pflanzen_ein','07:00:00',NULL,1,1,1,1,1,1,1,1,1,NULL,NULL,NULL,NULL),(2,'Pflanzen_aus','19:00:00',NULL,1,1,1,1,1,1,1,1,1,NULL,NULL,NULL,NULL),(3,'Sonnenaufgang','08:51:00',NULL,1,1,1,1,1,1,1,1,1,'rise',NULL,NULL,NULL),(4,'Sonnenuntergang','17:37:00',NULL,1,1,1,1,1,1,1,1,1,'set',NULL,NULL,NULL),(5,'Buero','10:15:00',NULL,1,1,1,1,1,1,1,1,0,NULL,'-30','90','10:00:00'),(6,'AbendBelEin','16:37:00',NULL,1,1,1,1,1,1,1,1,1,'set','-60',NULL,NULL),(7,'AbendBelAus','00:35:00',NULL,1,1,1,1,1,1,1,1,1,NULL,'-60','118','01:00:00'),(8,'MorgenBelEin','06:51:00',NULL,1,1,1,1,1,1,1,1,1,'rise','-120',NULL,NULL),(9,'MorgenBelAus','09:51:00',NULL,1,1,1,1,1,1,1,1,1,'rise','60',NULL,NULL);
/*!40000 ALTER TABLE `cron` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-06 16:52:55
