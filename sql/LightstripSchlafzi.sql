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
-- Table structure for table `LightstripSchlafzi`
--

DROP TABLE IF EXISTS `LightstripSchlafzi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LightstripSchlafzi` (
  `id` int(11) NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Rot` int(11) DEFAULT NULL,
  `Gruen` int(11) DEFAULT NULL,
  `Blau` int(11) DEFAULT NULL,
  `Transitiontime` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LightstripSchlafzi`
--

LOCK TABLES `LightstripSchlafzi` WRITE;
/*!40000 ALTER TABLE `LightstripSchlafzi` DISABLE KEYS */;
INSERT INTO `LightstripSchlafzi` VALUES (0,'Aus',0,0,0,0),(1,'Hell',255,255,255,0),(2,'SchlafziLangsamRot',255,0,0,600),(3,'Wecker1',50,0,0,150),(4,'Wecker2',132,0,0,50),(5,'Wecker3',156,156,0,50),(6,'Wecker4',200,200,200,50),(7,'Schlafen1',100,25,0,0),(8,'Schlafen2',0,0,0,60),(9,'Rot',255,0,0,0),(10,'Dunkerot',100,0,0,0),(11,'Romantisch',120,30,0,0),(12,'Wecker0a',10,0,0,300),(13,'WeckerRomantisch',120,30,0,60),(14,'WeckerSonntags0',100,0,0,1200),(15,'WeckerSonntags1',255,255,255,1200),(16,'Wecker6',255,255,255,600);
/*!40000 ALTER TABLE `LightstripSchlafzi` ENABLE KEYS */;
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
