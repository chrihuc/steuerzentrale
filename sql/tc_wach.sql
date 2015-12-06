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
-- Table structure for table `tc_wach`
--

DROP TABLE IF EXISTS `tc_wach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_wach` (
  `idtc_wach` int(11) NOT NULL,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` varchar(45) DEFAULT NULL,
  `tc_value_eq` varchar(45) DEFAULT NULL,
  `tc_value_gt` varchar(45) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(1) DEFAULT NULL,
  PRIMARY KEY (`idtc_wach`),
  UNIQUE KEY `idtc_wach_UNIQUE` (`idtc_wach`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_wach`
--

LOCK TABLES `tc_wach` WRITE;
/*!40000 ALTER TABLE `tc_wach` DISABLE KEYS */;
INSERT INTO `tc_wach` VALUES (1,'Helligkeit',NULL,NULL,'-1','AutoBeleuchtung',1),(11,'a1',NULL,'0',NULL,'Sideb_Aus',1),(12,'a1',NULL,NULL,'0','Sideb_An',1),(13,'a2',NULL,'0',NULL,'Sideb_OR_Aus',1),(14,'a2',NULL,NULL,'0','Sideb_OR_An',1),(15,'a4',NULL,'0',NULL,'Sideb_Aus',1),(16,'a4',NULL,NULL,'0','Sideb_An',1),(17,'a8',NULL,'0',NULL,'Sideb_OM_Aus',1),(18,'a8',NULL,NULL,'0','Sideb_OM_An',1),(19,'a16',NULL,'0',NULL,'Sideb_Aus',1),(20,'a16',NULL,NULL,'0','Sideb_An',1),(21,'a32',NULL,'0',NULL,'Sideb_OL_Aus',1),(22,'a32',NULL,NULL,'0','Sideb_OL_An',1),(25,'Wand_Wohnzi_1',NULL,'100',NULL,'Kueche',1),(26,'Wand_Wohnzi_3',NULL,'100',NULL,'LightstripKueche_2',1),(27,'Wand_Wohnzi_3',NULL,'0',NULL,'LightstripKueche_aus',1),(30,'Wand_Haupt_3',NULL,'100',NULL,'DRS3',1),(80,'Wand_Wohnzi_5',NULL,'0',NULL,'Balkonlampe',1),(101,'Wand_Wohnzi_5',NULL,'100',NULL,'Sonos_Kueche_TV',1),(120,'Wand_Buero_1',NULL,'0',NULL,'Buero_hell',1),(121,'Wand_Buero_1',NULL,'100',NULL,'Buero',1),(130,'Wand_Buero_2',NULL,'0',NULL,'Buero_romantisch',1),(131,'Wand_Buero_2',NULL,'100',NULL,'Buero',1),(140,'n13_229','3000',NULL,NULL,'Buero_hell',1),(151,'Wand_Flur_5',NULL,'100',NULL,'SchlafZi_alles_an',1),(171,'Wand_Flur_7',NULL,'100',NULL,'SchlafZi_alles_aus',1),(191,'Wand_Flur_9',NULL,'0',NULL,'Einer_schlafengegangen',1),(192,'Wand_Flur_9',NULL,'100',NULL,'Wetter',1),(200,'balkon_dt',NULL,'1',NULL,'Monaco',0),(201,'balkon_dt',NULL,'-1',NULL,'Monaco',0),(301,'Bad_bewegung',NULL,NULL,'0','Bad_ir',1),(400,'Bett_1',NULL,'1',NULL,'Schlafzimmer_aus',1),(401,'Bett_1',NULL,'3',NULL,'Romantisch',1),(402,'Bett_1',NULL,'2',NULL,'SchlafZi_alles_an',1),(500,'Temperatur_Balkon','Temperatur_Schlafzi',NULL,NULL,'Schlafzi_fenster_auf',1),(501,'Temperatur_Balkon',NULL,NULL,'Temperatur_Schlafzi','Schlafzi_fenster_zu',1),(502,'Temperatur_Balkon','Temperatur_Wohnzi',NULL,NULL,'Wohnzi_fenster_auf',1),(503,'Temperatur_Balkon',NULL,NULL,'Temperatur_Wohnzi','Wohnzi_fenster_zu',1),(504,'Temperatur_Schlafzi','23.5',NULL,NULL,'Schlafzi_kalt',1),(505,'Temperatur_Schlafzi','26',NULL,'24','Schlafzi_normal',1),(506,'Temperatur_Schlafzi',NULL,NULL,'26','Schlafzi_lueften',1),(507,'Temperatur_Wohnzi','24',NULL,NULL,'Wohnzi_kalt',1),(508,'Temperatur_Wohnzi','26',NULL,'24','Wohnzi_normal',1),(509,'Temperatur_Wohnzi',NULL,NULL,'26','Wohnzi_lueften',1),(600,'Balkontuer',NULL,'1',NULL,'Esszimmer',0),(601,'Balkontuer',NULL,'0',NULL,'Esszimmer',0);
/*!40000 ALTER TABLE `tc_wach` ENABLE KEYS */;
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
