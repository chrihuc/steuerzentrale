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
-- Table structure for table `Settings`
--

DROP TABLE IF EXISTS `Settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Settings` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text,
  `Value` text,
  `AppSet` int(11) DEFAULT NULL,
  `Beschreibung` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Settings`
--

LOCK TABLES `Settings` WRITE;
/*!40000 ALTER TABLE `Settings` DISABLE KEYS */;
INSERT INTO `Settings` VALUES (0,'Alarmanlage','Aus',NULL,NULL),(1,'Anwesenheit','3',NULL,NULL),(2,'Status','Wach',NULL,NULL),(3,'Zusatz_Status','Leer',NULL,NULL),(4,'Autorestart','2015-12-03 07:04:19',NULL,NULL),(5,'Tempbereich','inactive',NULL,NULL),(6,'NumRestart','0',NULL,NULL),(7,'XS1_off','inactive',NULL,NULL),(8,'Laststart','2015-12-06 16:16:26',NULL,NULL),(9,'AV_cmd','1',NULL,NULL),(10,'Kommando','Aus',NULL,NULL),(11,'Temp_Alarm','inactive',NULL,NULL),(12,'Durchsage','T Wohnzimmer normalisiert',NULL,NULL),(13,'Beleuchtung','Abends',NULL,NULL),(14,'TempAlarmSchlafzi','20',NULL,NULL),(15,'Licht_Schlafzi','Aus',NULL,NULL),(16,'Wohnzimmer_Decke','fixed',NULL,NULL),(17,'Esszimmer','dunkler',NULL,NULL),(18,'Licht_Kueche','An',NULL,NULL),(19,'Meldung','Leer',NULL,NULL),(20,'TempSettingWohnziAnw','25.5',NULL,NULL),(21,'TempSettingWohnziAbw','23.5',NULL,NULL),(22,'Schluessel_Christoph','0',NULL,NULL),(23,'Schluessel_Sabina','0',NULL,NULL),(24,'Schluessel_Christoph_neu','0',NULL,NULL),(25,'Schluessel_Sabina_neu','0',NULL,NULL),(26,'TempSteuerung','Ein',1,'Temperatur Alarme'),(27,'Fern_Bett','Wach',NULL,NULL),(28,'Sideboard','Loop2',NULL,NULL),(29,'Schluessel_Besuch','0',NULL,NULL),(30,'Schluessel_Besuch_neu','0',NULL,NULL),(31,'Einbruch','False',NULL,NULL),(32,'Balkontuer','0.0',NULL,NULL),(33,'Next_alarm','Wecker Morgen um 8 Uhr, das ist in 9 Stunden und 39 Minuten.',NULL,NULL),(34,'Christoph_anwesend','1',NULL,NULL),(35,'Sabina_anwesend','1',NULL,NULL),(36,'AutoLicht','Ein',1,'Automatische Lichtszenen'),(37,'Temperatur_Wohnzi','25.6',NULL,NULL),(38,'Temperatur_Schlafzi','25.1',NULL,NULL),(39,'T_Wohnzi_T_Balkon','less',NULL,NULL),(40,'T_Schlafzi_T_Balkon','less',NULL,NULL),(41,'Notify_Sabina','Ein',1,'Nachrichten an Sabinas Handy'),(42,'Notify_Christoph','Ein',NULL,NULL),(43,'Notification_Visuell','Aus',1,'Lichter blinken bei Nachrichten'),(44,'LightstripKueche','1',NULL,NULL),(45,'Sideb_OR','0',NULL,NULL),(46,'Sideb_OM','0',NULL,NULL),(47,'Sideb_OL','0',NULL,NULL),(48,'Helligkeit','20',NULL,NULL),(49,'Restart_PIs','Aus',1,'Restart also PIs'),(50,'Halloween','Aus',1,'Halloween Beleuchtung'),(51,'Kino_Beleuchtung','Aus',1,'Kino Beleuchtung'),(52,'Kino_Beleuchtung_Auto','Aus',1,'Auto Kino Beleuchtung'),(53,'AV_mode','Aus',NULL,NULL),(54,'Kuechentuer','0.0',NULL,NULL),(55,'Haustuer','0',NULL,NULL),(57,'T_WohnZi','normal',NULL,NULL),(58,'T_SchlafZi','normal',NULL,NULL),(59,'Fenster_override','Aus',NULL,NULL),(60,'Frostalarm','Aus',1,'Frostalarm'),(61,'SchlafZiFenster','0',NULL,NULL),(62,'Heizung_eins','Aus',1,'Heizung aussgeschaltet'),(63,'Heizung_auss','Aus',1,'Heizung eingeschaltet'),(64,'Master_Slave','Master',NULL,NULL);
/*!40000 ALTER TABLE `Settings` ENABLE KEYS */;
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
