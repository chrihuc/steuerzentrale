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
-- Table structure for table `Hue`
--

DROP TABLE IF EXISTS `Hue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Hue` (
  `idHue` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `hue` int(11) DEFAULT NULL,
  `bri` varchar(45) DEFAULT NULL,
  `an` varchar(10) DEFAULT NULL,
  `sat` int(11) DEFAULT NULL,
  `transitiontime` int(11) DEFAULT NULL,
  PRIMARY KEY (`idHue`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Hue`
--

LOCK TABLES `Hue` WRITE;
/*!40000 ALTER TABLE `Hue` DISABLE KEYS */;
INSERT INTO `Hue` VALUES (1,'Wecker0',0,'0','1',254,1),(2,'Wecker1',5460,'0','1',254,1500),(3,'Wecker2',NULL,'254',NULL,NULL,1500),(4,'Wecker3',NULL,NULL,NULL,0,1500),(5,'Wecker4',39742,NULL,NULL,111,1500),(6,'Alarm_Rot',0,'254','1',254,1),(7,'Alarm_Blau',47124,'254','1',254,1),(9,'Hell',34534,'254','1',240,NULL),(10,'Aus',NULL,NULL,'0',NULL,NULL),(11,'Dunkelrot',0,'0','1',254,1),(12,'SZ_Aus',0,'0','0',254,1),(13,'SZ_hell',0,'254','1',0,NULL),(14,'SchlafziFenster',0,'0','False',254,NULL),(17,'Alarm_Gruen',25718,'254','1',254,1),(18,'Abends',12554,'254','1',254,1),(19,'1.0',0,'254','1',254,1),(20,'2.0',47124,'254','1',254,1),(21,'3.0',25718,'254','1',254,1),(22,'Romantisch',6000,'100','1',254,1),(23,'Wecker0_0',0,'0',NULL,254,1),(24,'Wecker1_0',5460,'0',NULL,254,1500),(25,'Halloween',9000,'254','1',254,1),(26,'Advent1',47124,'132','1',0,1500),(27,'Rot',0,'254','1',254,0),(28,'Orange',4000,'254','1',254,0),(29,'Advent0',47124,'0','1',0,0),(30,'App',54872,'255.0','1',254,NULL),(31,'Gemuetlich',12554,'176','1',225,NULL),(32,'Gemuetlich_1',12554,'60','1',255,NULL),(33,'Balkon_hell',12554,'180','1',255,0),(34,'Balkon_dunkel',12554,'0','1',255,0),(35,'WeckerRomantisch',6000,'100','1',254,60),(36,'Gruen_dunkel',25718,'50','1',254,0),(37,'AutoBel_Monaco',12554,'Monaco','1',254,2),(38,'AutoBel_Steh',12554,'Stehlampe','1',254,2),(39,'AutoBel_Stab',12554,'Stablampe','1',254,2),(40,'AutoBel_Kue',12554,'Kueche','1',254,2),(41,'AutoBel_Flur',12554,'FlurBoden','1',254,2),(42,'AutoBel_Monaco_Kino',12554,'Monaco_Kino','1',254,2),(43,'AutoBel_Steh_Kino',12554,'Stehlampe_Kino','1',254,2),(44,'AutoBel_Kue_Kino',12554,'Kueche_Kino','1',254,2),(45,'AutoBel_Flur_Kino',12554,'FlurBoden_Kino','1',254,2),(46,'AutoBel_Stab_Kino',12554,'Stablampe_Kino','1',254,2),(47,'Bad_hell',0,'254','1',0,NULL),(48,'Wecker6',12554,'254','1',111,600),(49,'Bad_dunkel',0,'20','1',254,0),(101,'LightstripKueche',NULL,NULL,NULL,NULL,NULL),(102,'Lightstrips 2',12554,'156','False',254,NULL),(103,'Stehlampe',12554,'157','False',254,0),(104,'BettSabina',NULL,NULL,NULL,NULL,NULL),(105,'BettChris',NULL,NULL,NULL,NULL,NULL),(106,'Monaco Lampe',NULL,NULL,NULL,NULL,NULL),(107,'Stablampe 1',12554,'156','False',254,NULL),(108,'Balkonlampe',NULL,NULL,NULL,NULL,NULL),(109,'Bad',0,'254','False',0,NULL),(110,'Stablampe 2',12554,'156','False',254,NULL),(111,'Buero',NULL,NULL,NULL,NULL,NULL),(130,'Advent_0ter',47124,'100','1',254,1500),(131,'Advent_1ter',47124,'130','1',254,1500),(132,'Advent_2ter',37124,'130','1',254,1500);
/*!40000 ALTER TABLE `Hue` ENABLE KEYS */;
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
