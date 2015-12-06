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
-- Table structure for table `Fern_Reduit`
--

DROP TABLE IF EXISTS `Fern_Reduit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Reduit` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) DEFAULT NULL,
  `Fern_Reduit_1` varchar(45) DEFAULT NULL,
  `Fern_Reduit_2` varchar(45) DEFAULT NULL,
  `Fern_Reduit_3` varchar(45) DEFAULT NULL,
  `Fern_Reduit_4` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Reduit`
--

LOCK TABLES `Fern_Reduit` WRITE;
/*!40000 ALTER TABLE `Fern_Reduit` DISABLE KEYS */;
INSERT INTO `Fern_Reduit` VALUES (1,'Rest',NULL,NULL,NULL,'Alles_aus'),(2,'einer_wach',NULL,NULL,NULL,'einer_weg'),(3,'Urlaub',NULL,NULL,NULL,NULL),(4,'Einbruch',NULL,NULL,NULL,NULL),(5,'Besuch',NULL,NULL,NULL,NULL),(6,'Gegangen','Tuer_auf','Tuer_auf','Tuer_auf','Tuer_auf'),(7,'Abwesend','Tuer_auf','Tuer_auf','Tuer_auf','Tuer_auf'),(8,'Wach','Saugstauber',NULL,'Alles_ein','Alles_aus');
/*!40000 ALTER TABLE `Fern_Reduit` ENABLE KEYS */;
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
