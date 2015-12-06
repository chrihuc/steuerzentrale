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
-- Table structure for table `Fern_Bad`
--

DROP TABLE IF EXISTS `Fern_Bad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Bad` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) NOT NULL,
  `Fern_Bad_1` varchar(45) DEFAULT NULL,
  `Fern_Bad_2` varchar(45) DEFAULT NULL,
  `Fern_Bad_3` varchar(45) DEFAULT NULL,
  `Fern_Bad_4` varchar(45) DEFAULT NULL,
  `Fern_Bad_5` varchar(45) DEFAULT NULL,
  `Fern_Bad_6` varchar(45) DEFAULT NULL,
  `Fern_Bad_7` varchar(45) DEFAULT NULL,
  `Fern_Bad_8` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Szene_UNIQUE` (`Szene`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Bad`
--

LOCK TABLES `Fern_Bad` WRITE;
/*!40000 ALTER TABLE `Fern_Bad` DISABLE KEYS */;
INSERT INTO `Fern_Bad` VALUES (1,'Rest','Bad_hell','Bad','SonosBadSRF3','SonosBadSwPop','SonosBadInpWohnzi','SonosBadInpWohnzi','SonosBadVolUp','SonosBadVolDown'),(2,'Wecken','VolMorgensBad','VolMorgensBad','VolMorgensBad','VolMorgensBad',NULL,NULL,'SonosBadVolUp','SonosBadVolDown'),(3,'Schlafen','Bad_dunkel','Bad',NULL,NULL,NULL,NULL,NULL,NULL),(4,'einer_wach','Bad_dunkel','Bad','SonosBadSRF3','SonosBadSRF3',NULL,NULL,'SonosBadVolUp','SonosBadVolDown');
/*!40000 ALTER TABLE `Fern_Bad` ENABLE KEYS */;
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
