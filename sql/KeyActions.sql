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
-- Table structure for table `KeyActions`
--

DROP TABLE IF EXISTS `KeyActions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `KeyActions` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `BeBe` varchar(45) DEFAULT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `Szene` varchar(45) DEFAULT NULL,
  `Event` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id_UNIQUE` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `KeyActions`
--

LOCK TABLES `KeyActions` WRITE;
/*!40000 ALTER TABLE `KeyActions` DISABLE KEYS */;
INSERT INTO `KeyActions` VALUES (1,'Bewohner','Abwesend','Heimgekommen','1'),(4,'Bewohner','Urlaub','Heimgekommen','1'),(5,'Bewohner','Gegangen','Heimgekommen','1'),(6,'Bewohner','Besuch','Heimgekommen','1'),(7,'Bewohner','Einbruch','Heimgekommen','1'),(8,'Bewohner','Schlafen','einer_heimgekommen','1'),(9,'Bewohner','Am Gehen','Heimgekommen','1'),(10,'Besucher','Abwesend','Besuch','1'),(11,'Besucher','Urlaub','Besuch','1'),(12,'Besucher','Gegangen','Besuch','1'),(13,'Besucher','Einbruch','Besuch','1'),(14,'Bewohner','einer_Wach','einer_weg','0');
/*!40000 ALTER TABLE `KeyActions` ENABLE KEYS */;
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
