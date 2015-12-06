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
-- Table structure for table `tc_schlummern`
--

DROP TABLE IF EXISTS `tc_schlummern`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_schlummern` (
  `idtc_table` int(11) NOT NULL,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` int(11) DEFAULT NULL,
  `tc_value_eq` int(11) DEFAULT NULL,
  `tc_value_gt` int(11) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtc_table`),
  UNIQUE KEY `idtc_table` (`idtc_table`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_schlummern`
--

LOCK TABLES `tc_schlummern` WRITE;
/*!40000 ALTER TABLE `tc_schlummern` DISABLE KEYS */;
INSERT INTO `tc_schlummern` VALUES (10,'Bett_1',NULL,1,NULL,'Schlafzimmer_aus',1),(14,'Bett_1',NULL,2,NULL,'WeckerPhase0a',1),(15,'Bett_1',NULL,3,NULL,'WeckerRomantisch',1);
/*!40000 ALTER TABLE `tc_schlummern` ENABLE KEYS */;
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
