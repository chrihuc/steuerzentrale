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
-- Table structure for table `Sideboard`
--

DROP TABLE IF EXISTS `Sideboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sideboard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `mode` text,
  `start` text,
  `rot` int(11) DEFAULT NULL,
  `gruen` int(11) DEFAULT NULL,
  `blau` int(11) DEFAULT NULL,
  `reverse` varchar(45) DEFAULT NULL,
  `delay` varchar(45) DEFAULT NULL,
  `reset` varchar(45) DEFAULT NULL,
  `new` varchar(45) DEFAULT NULL,
  `n_rot` int(11) DEFAULT NULL,
  `n_gruen` int(11) DEFAULT NULL,
  `n_blau` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sideboard`
--

LOCK TABLES `Sideboard` WRITE;
/*!40000 ALTER TABLE `Sideboard` DISABLE KEYS */;
INSERT INTO `Sideboard` VALUES (1,'Aus','set_one_color','[0,15,30]',0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'Halloween','set_one_color','[0,15,30]',255,50,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'LefToRight','flash','[0,15,30]',255,255,0,'False','0.01','False','True',255,255,0),(4,'Rot','set_one_color','[0,30]',255,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'RightToLeft','flash','[30,15,0]',0,255,0,'False','0.01','False','True',0,255,0),(6,'Hell','set_one_color','[0,15,30]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,'Loop0','set_one_color','[0,15,30]',0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8,'Loop1','set_one_color','[0,15,30]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(9,'Loop2','set_one_color','[0,15,30]',255,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(10,'Loop3','set_one_color','[0,15,30]',0,255,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(11,'Loop4','set_one_color','[0,15,30]',0,0,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(12,'Loop5','set_one_color','[0,15,30]',0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(13,'Loop6','set_one_color','[15]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(14,'Loop7','flash','[0]',0,255,0,'False','0.01','False','True',255,255,255),(15,'Loop8','flash','[30]',0,255,0,'True','0.01','False','True',255,255,255),(16,'Abends','set_one_color','[0,15,30]',255,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(17,'Weiss50','set_one_color','[0,15,30]',50,50,50,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(18,'Weiss','set_one_color','[0,15,30]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,'Weiss25','set_one_color','[0,15,30]',25,25,25,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,'Blau','set_one_color','[0,15,30]',0,0,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(21,'App','set_one_color','[0,15,30]',0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(22,'LinksAn1','flash','[0,15]',255,255,255,'False','0.05','True','False',NULL,NULL,NULL),(23,'Rot125','set_one_color','[0,30]',70,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(24,'Weiss12','set_one_color','[15]',5,5,5,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(25,'LinksAn2','flash','[30]',255,255,255,'False','0.05','False',NULL,NULL,NULL,NULL),(26,'Kino','set_one_color','[0,30]',25,5,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,'Kino_Mitte','set_one_color','[15]',10,2,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,'Hell_l','set_one_color','[30]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,'Hell_m','set_one_color','[15]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,'Hell_r','set_one_color','[0]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Sideboard` ENABLE KEYS */;
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
