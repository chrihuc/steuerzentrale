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
-- Table structure for table `Actuators`
--

DROP TABLE IF EXISTS `Actuators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Actuators` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) DEFAULT NULL,
  `Value` decimal(5,1) DEFAULT NULL,
  `Date` datetime DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Actuators`
--

LOCK TABLES `Actuators` WRITE;
/*!40000 ALTER TABLE `Actuators` DISABLE KEYS */;
/*!40000 ALTER TABLE `Actuators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `App`
--

DROP TABLE IF EXISTS `App`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `App` (
  `idApp` int(11) NOT NULL AUTO_INCREMENT,
  `Kommando` varchar(45) DEFAULT NULL,
  `Szene` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idApp`),
  UNIQUE KEY `idApp_UNIQUE` (`idApp`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `App`
--

LOCK TABLES `App` WRITE;
/*!40000 ALTER TABLE `App` DISABLE KEYS */;
INSERT INTO `App` VALUES (1,'app_lights_off','Alle_Lichter_Aus'),(2,'app_lights_on','Alle_Lichter_Ein'),(3,'app_lights_abend','Abendlicht_Decke_aus'),(4,'app_stablampe','Stablampe'),(5,'app_eingang','Eingang'),(6,'app_Weihnachtsbaum','Weihnachtsbaum'),(8,'app_Advent','Advent'),(9,'app_heimgekommen','Heimgekommen'),(10,'app_besuch','Besuch'),(11,'app_stehlampe','Stehlampe'),(12,'app_monaco','Monaco'),(13,'app_schlafzife','SchlafziFe'),(14,'app_BalkonLampe','BalkonLampe'),(15,'app_SZPlay','SchlafZiPlay'),(16,'app_SZPause','SchlafZiPause'),(17,'app_BadPlay','BadPlay'),(18,'app_BadPause','BadPause'),(19,'app_KitPause','KitPause'),(20,'app_KitPlay','KitPlay'),(21,'app_Balkon_1','Balkon_1'),(22,'app_Balkon_2','Balkon_2'),(23,'app_ch_up','ChannelUp'),(24,'app_ch_down','ChannelDown'),(25,'app_mar_lauter','Marantz_lauter'),(26,'app_mar_leiser','Marantz_leiser'),(27,'app_tv_ein','TV'),(28,'app_tv_aus','Media_aus'),(29,'app_tv','TV'),(30,'app_radio','DRS3');
/*!40000 ALTER TABLE `App` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Balkon_H`
--

DROP TABLE IF EXISTS `Balkon_H`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Balkon_H` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` decimal(3,1) DEFAULT NULL,
  `Date` datetime DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Balkon_H`
--

LOCK TABLES `Balkon_H` WRITE;
/*!40000 ALTER TABLE `Balkon_H` DISABLE KEYS */;
/*!40000 ALTER TABLE `Balkon_H` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Balkon_T`
--

DROP TABLE IF EXISTS `Balkon_T`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Balkon_T` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` decimal(3,1) DEFAULT NULL,
  `Date` datetime DEFAULT NULL,
  `RolAvg` decimal(5,3) DEFAULT NULL,
  `D1` decimal(5,3) DEFAULT NULL,
  `D2` decimal(5,3) DEFAULT NULL,
  `D3` decimal(5,3) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Balkon_T`
--

LOCK TABLES `Balkon_T` WRITE;
/*!40000 ALTER TABLE `Balkon_T` DISABLE KEYS */;
/*!40000 ALTER TABLE `Balkon_T` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Besucher`
--

DROP TABLE IF EXISTS `Besucher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Besucher` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `USB_ID` varchar(45) DEFAULT NULL,
  `USB_State` int(11) DEFAULT NULL,
  `prod` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id_UNIQUE` (`Id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Besucher`
--

LOCK TABLES `Besucher` WRITE;
/*!40000 ALTER TABLE `Besucher` DISABLE KEYS */;
INSERT INTO `Besucher` VALUES (1,'Huckle','00D0C9CCDE48EDB14000F139',0,'None'),(2,'Russ','C86000BDB9F2EE10AA310081',-10,'leer'),(4,'Test','001A4D5E40201F719940087A',0,'leer');
/*!40000 ALTER TABLE `Besucher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Bewohner`
--

DROP TABLE IF EXISTS `Bewohner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Bewohner` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Handy_IP` varchar(45) DEFAULT NULL,
  `Handy_State` int(11) DEFAULT NULL,
  `USB_ID` varchar(45) DEFAULT NULL,
  `USB_State` int(11) DEFAULT NULL,
  `prod` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id_UNIQUE` (`Id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Bewohner`
--

LOCK TABLES `Bewohner` WRITE;
/*!40000 ALTER TABLE `Bewohner` DISABLE KEYS */;
INSERT INTO `Bewohner` VALUES (1,'Christoph','192.168.192.21',5,'C86000BDB9E9EE10800000B0',0,'leer'),(2,'Sabina','192.168.192.22',5,'6CF049E0FBE2FD40B95F273B',0,'leer');
/*!40000 ALTER TABLE `Bewohner` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Table structure for table `Fern_Bett`
--

DROP TABLE IF EXISTS `Fern_Bett`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Bett` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) NOT NULL,
  `NeuerStatus` varchar(45) DEFAULT NULL,
  `Status_Delay` varchar(45) DEFAULT NULL,
  `Fern_Bett_0_kurz` varchar(45) DEFAULT NULL,
  `Fern_Bett_0_lang` varchar(45) DEFAULT NULL,
  `Fern_Bett_0_lang_lang` varchar(45) DEFAULT NULL,
  `Fern_Bett_3_kurz` varchar(45) DEFAULT NULL,
  `Fern_Bett_3_lang` varchar(45) DEFAULT NULL,
  `Fern_Bett_4_kurz` varchar(45) DEFAULT NULL,
  `Fern_Bett_4_lang` varchar(45) DEFAULT NULL,
  `Fern_Bett_7_kurz` varchar(45) DEFAULT NULL,
  `Fern_Bett_7_lang` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Status_UNIQUE` (`Szene`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Bett`
--

LOCK TABLES `Fern_Bett` WRITE;
/*!40000 ALTER TABLE `Fern_Bett` DISABLE KEYS */;
INSERT INTO `Fern_Bett` VALUES (1,'Rest',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'Am Schlafen gehen',NULL,NULL,'Bettlampe_Chris',NULL,NULL,NULL,NULL,'Bettlampe_Sabina',NULL,NULL,NULL),(3,'Wecken',NULL,NULL,'Bettlampe_Chris',NULL,NULL,NULL,NULL,'Bettlampe_Sabina',NULL,NULL,NULL),(4,'Wach',NULL,NULL,'Bettlampe_Chris','Bettlampe_Chris_hell',NULL,NULL,NULL,'Bettlampe_Sabina','Bettlampe_Sabina',NULL,NULL),(5,'Schlafen',NULL,NULL,NULL,'Bettlampe_Chris',NULL,NULL,NULL,'Bettlampe_Sabina','Bettlampe_Sabina',NULL,NULL),(6,'einer_wach',NULL,NULL,'Bettlampe_Chris',NULL,NULL,'Bettlampe_Chris',NULL,'Bettlampe_Sabina',NULL,NULL,NULL),(7,'Bett_Chris_dunkel_1',NULL,NULL,'Bett_Chris_aus_1','WeckerPhase1',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Fern_Bett` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fern_Esszi`
--

DROP TABLE IF EXISTS `Fern_Esszi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Esszi` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) DEFAULT NULL,
  `Fern_Esszi_1` varchar(45) DEFAULT NULL,
  `Fern_Esszi_2` varchar(45) DEFAULT NULL,
  `Fern_Esszi_3` varchar(45) DEFAULT NULL,
  `Fern_Esszi_4` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Esszi`
--

LOCK TABLES `Fern_Esszi` WRITE;
/*!40000 ALTER TABLE `Fern_Esszi` DISABLE KEYS */;
INSERT INTO `Fern_Esszi` VALUES (1,'Rest',NULL,NULL,NULL,NULL),(2,'einer_wach',NULL,'Radio_einer_wach',NULL,NULL),(3,'Urlaub',NULL,NULL,NULL,NULL),(4,'Einbruch',NULL,NULL,NULL,NULL),(5,'Besuch',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Fern_Esszi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fern_Flur`
--

DROP TABLE IF EXISTS `Fern_Flur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Flur` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) DEFAULT NULL,
  `Fern_Flur_1` varchar(45) DEFAULT NULL,
  `Fern_Flur_2` varchar(45) DEFAULT NULL,
  `Fern_Flur_3` varchar(45) DEFAULT NULL,
  `Fern_Flur_4` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Flur`
--

LOCK TABLES `Fern_Flur` WRITE;
/*!40000 ALTER TABLE `Fern_Flur` DISABLE KEYS */;
INSERT INTO `Fern_Flur` VALUES (1,'Rest',NULL,NULL,'Schlafen1',NULL),(2,'einer_wach',NULL,'sz_Schlafen_stealth','sz_Schlafen_stealth','sz_Schlafen_stealth'),(3,'Urlaub',NULL,NULL,NULL,NULL),(4,'Schlafen',NULL,NULL,'sz_Schlafen_stealth','sz_Schlafen_stealth'),(5,'Wecken',NULL,NULL,'WeckerAusWach','WeckerAusWach'),(6,'Schlummern',NULL,NULL,'WeckerAusWach','WeckerAusWach'),(7,'Doppelklick',NULL,'SchlafZi_alles_an',NULL,NULL),(8,'Einbruch',NULL,NULL,NULL,NULL),(9,'Besuch',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Fern_Flur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fern_Handy`
--

DROP TABLE IF EXISTS `Fern_Handy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Handy` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) NOT NULL,
  `Fern_Hand_1` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Szene_UNIQUE` (`Szene`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Handy`
--

LOCK TABLES `Fern_Handy` WRITE;
/*!40000 ALTER TABLE `Fern_Handy` DISABLE KEYS */;
INSERT INTO `Fern_Handy` VALUES (1,'Rest',NULL),(2,'Abwesend','Heimgekommen'),(3,'Schlafen','einer_heimgekommen'),(4,'Einbruch','Heimgekommen');
/*!40000 ALTER TABLE `Fern_Handy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fern_Haupt`
--

DROP TABLE IF EXISTS `Fern_Haupt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Haupt` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) DEFAULT NULL,
  `Fern_Haupt_1` varchar(45) DEFAULT NULL,
  `Fern_Haupt_2` varchar(45) DEFAULT NULL,
  `Fern_Haupt_3` varchar(45) DEFAULT NULL,
  `Fern_Haupt_4` varchar(45) DEFAULT NULL,
  `Fern_Haupt_5` varchar(45) DEFAULT NULL,
  `Fern_Haupt_6` varchar(45) DEFAULT NULL,
  `Fern_Haupt_7` varchar(45) DEFAULT NULL,
  `Fern_Haupt_8` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Haupt`
--

LOCK TABLES `Fern_Haupt` WRITE;
/*!40000 ALTER TABLE `Fern_Haupt` DISABLE KEYS */;
INSERT INTO `Fern_Haupt` VALUES (1,'Rest',NULL,NULL,NULL,NULL,NULL,NULL,'Alles_aus',NULL),(2,'Hinweis_aktiv','az_Hinweis_gesehen','az_Hinweis_gesehen','az_Hinweis_gesehen','az_Hinweis_gesehen','az_Hinweis_gesehen','az_Hinweis_gesehen','az_Hinweis_gesehen','az_Hinweis_gesehen'),(3,'Schlafen',NULL,NULL,NULL,NULL,NULL,NULL,'Schlafen_stealth','WeckerAusWach'),(4,'Doppelklick','Alle_Lichter_Aus','Wohnzimmer_hell',NULL,NULL,'sz_RaspBMC','Swisspop',NULL,NULL),(5,'einer_wach',NULL,NULL,'Media_aus',NULL,'TV_Kopfh',NULL,'sz_Schlafen_stealth','WeckerAusWach'),(6,'Urlaub',NULL,NULL,'Media_aus',NULL,'TV',NULL,NULL,NULL),(7,'Schlummern',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerAusWach'),(8,'Wecken',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerAusWach'),(9,'Einbruch',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(10,'Besuch',NULL,NULL,'Media_aus',NULL,'TV',NULL,NULL,NULL),(11,'Wach','Doppelklick','Doppelklick','Media_aus','Wohnzimmer_hell','TV','DRS3','Alles_aus','Alles_ein'),(12,'Am Schlafen gehen',NULL,NULL,NULL,NULL,NULL,NULL,'Alles_aus','Alles_ein');
/*!40000 ALTER TABLE `Fern_Haupt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fern_Haustuer`
--

DROP TABLE IF EXISTS `Fern_Haustuer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Haustuer` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) DEFAULT NULL,
  `Fern_Haustuer_0` varchar(45) DEFAULT NULL,
  `Fern_Haustuer_1` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Haustuer`
--

LOCK TABLES `Fern_Haustuer` WRITE;
/*!40000 ALTER TABLE `Fern_Haustuer` DISABLE KEYS */;
INSERT INTO `Fern_Haustuer` VALUES (1,'Rest',NULL,NULL),(2,'Wach',NULL,'Tuer_auf_oL'),(3,'Am Gehen 1',NULL,'Tuer_auf_AG'),(4,'Am Gehen 2',NULL,'Tuer_auf_AG'),(5,'Am Gehen 3','Alles_aus_4',NULL),(6,'Schlafen',NULL,'Tuer_auf'),(7,'Urlaub',NULL,NULL),(8,'Gegangen',NULL,'Tuer_auf'),(9,'was_vergessen','Alles_aus_4',NULL),(10,'Abwesend',NULL,'Tuer_auf'),(11,'einer_wach',NULL,'Tuer_auf_oL'),(12,'Wecken',NULL,'Tuer_auf_oL'),(13,'Schlummern',NULL,'Tuer_auf'),(14,'Am Gehen','Alles_aus_5',NULL),(15,'Besuch',NULL,'Tuer_auf_oL');
/*!40000 ALTER TABLE `Fern_Haustuer` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Table structure for table `Fern_Schlafzi`
--

DROP TABLE IF EXISTS `Fern_Schlafzi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Schlafzi` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Szene` varchar(45) NOT NULL,
  `Fern_Schlafzi_1` varchar(45) DEFAULT NULL,
  `Fern_Schlafzi_2` varchar(45) DEFAULT NULL,
  `Fern_Schlafzi_3` varchar(45) DEFAULT NULL,
  `Fern_Schlafzi_4` varchar(45) DEFAULT NULL,
  `Fern_Schlafzi_5` varchar(45) DEFAULT NULL,
  `Fern_Schlafzi_6` varchar(45) DEFAULT NULL,
  `Fern_Schlafzi_7` varchar(45) DEFAULT NULL,
  `Fern_Schlafzi_8` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Szene_UNIQUE` (`Szene`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Schlafzi`
--

LOCK TABLES `Fern_Schlafzi` WRITE;
/*!40000 ALTER TABLE `Fern_Schlafzi` DISABLE KEYS */;
INSERT INTO `Fern_Schlafzi` VALUES (1,'Rest','Elchlampe','Schlafzimmer_aus','sn_Schlafzi_lauter','sn_Schlafzi_leiser',NULL,NULL,NULL,NULL),(2,'Am Schlafen gehen','Schlafen3','Schlafen3','Schlafen3','Schlafen3','sz_Romantisch','sz_Romantisch','sz_Romantisch','sz_Romantisch'),(3,'Schlafen','Elchlampe','Schlafzimmer_aus','sn_Schlafzi_lauter','sn_Schlafzi_leiser',NULL,NULL,'WeckerPhase1a','WeckerPhase1a'),(4,'Wecken','Schlummern15','Schlummern30','Schlummern60','Schlummern180','Schlummern240','WeckerAus','WeckerMute','WeckerMute'),(5,'Schlummern','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a'),(6,'einer_wach','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a','WeckerPhase1a'),(7,'Urlaub','Schlafzimmer_aus','Schlafzimmer_aus','Schlafzimmer_aus','Schlafzimmer_aus','Schlafzimmer_aus','Schlafzimmer_aus','Schlafzimmer_aus','Schlafzimmer_aus');
/*!40000 ALTER TABLE `Fern_Schlafzi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fern_Schluessel`
--

DROP TABLE IF EXISTS `Fern_Schluessel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fern_Schluessel` (
  `Id` int(11) NOT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `Schluessel_Christoph` varchar(45) DEFAULT NULL,
  `Schluessel_Sabina` varchar(45) DEFAULT NULL,
  `Schluessel_Christoph_neu` varchar(45) DEFAULT NULL,
  `Schluessel_Sabina_neu` varchar(45) DEFAULT NULL,
  `Szene` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id_UNIQUE` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fern_Schluessel`
--

LOCK TABLES `Fern_Schluessel` WRITE;
/*!40000 ALTER TABLE `Fern_Schluessel` DISABLE KEYS */;
INSERT INTO `Fern_Schluessel` VALUES (1,'Wach','1','1','1','0',NULL),(2,'Wach','1','1','0','1',NULL),(3,'Wach','1','0','1','1',NULL),(4,'Wach','0','1','1','1',NULL),(5,'Wach','1','1','0','0',NULL),(6,'Wach','1','0','0','0',NULL),(7,'Wach','0','1','0','0',NULL),(8,'Abwesend','0','0','1','1','Heimgekommen'),(9,'Abwesend','0','0','1','0','Heimgekommen'),(10,'Abwesend','0','0','0','1','Heimgekommen'),(11,'Abwesend','1','0','1','1','Heimgekommen'),(12,'Abwesend','0','1','1','1','Heimgekommen'),(21,'Schlafen','1','0','1','1','einer_heimgekommen'),(22,'Schlafen','0','1','1','1','einer_heimgekommen'),(23,'Schlafen','1','1','1','0','einer_weg'),(24,'Schlafen','1','1','0','0',NULL),(25,'Schlafen','1','0','0','0',NULL),(26,'Schlafen','0','1','0','0',NULL),(27,'Schlafen','1','1','0','1','einer_weg'),(31,'einer_wach','1','1','0','1','einer_weg'),(32,'einer_wach','1','1','1','0','einer_weg'),(33,'einer_wach','1','0','0','1','einer_weg'),(40,'Gegangen','1','1','0','0',NULL),(41,'Gegangen','1','0','0','0',NULL),(42,'Gegangen','0','1','0','0',NULL),(43,'Gegangen','0','0','1','0','Heimgekommen'),(44,'Gegangen','0','0','0','1','Heimgekommen'),(45,'Gegangen','0','1','1','0','Heimgekommen'),(46,'Gegangen','1','0','0','1','Heimgekommen'),(47,'Einbruch','0','0','1','0','Heimgekommen'),(48,'Einbruch','0','0','0','1','Heimgekommen'),(49,'Einbruch','0','1','1','0','Heimgekommen'),(50,'Einbruch','1','0','0','1','Heimgekommen'),(51,'Einbruch','0','1','1','1','einer_heimgekommen'),(52,'Einbruch','1','0','1','1','einer_heimgekommen');
/*!40000 ALTER TABLE `Fern_Schluessel` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Hue`
--

LOCK TABLES `Hue` WRITE;
/*!40000 ALTER TABLE `Hue` DISABLE KEYS */;
INSERT INTO `Hue` VALUES (1,'Wecker0',0,'0','1',254,1),(2,'Wecker1',5460,'0','1',254,1500),(3,'Wecker2',NULL,'254',NULL,NULL,1500),(4,'Wecker3',NULL,NULL,NULL,0,1500),(5,'Wecker4',39742,NULL,NULL,111,1500),(6,'Alarm_Rot',0,'254','1',254,1),(7,'Alarm_Blau',47124,'254','1',254,1),(9,'Hell',34534,'254','1',240,NULL),(10,'Aus',NULL,NULL,'0',NULL,NULL),(11,'Dunkelrot',0,'0','1',254,1),(12,'SZ_Aus',0,'0','0',254,1),(13,'SZ_hell',0,'254','1',0,NULL),(14,'SchlafziFenster',0,'0','False',254,NULL),(17,'Alarm_Gruen',25718,'254','1',254,1),(18,'Abends',12554,'254','1',254,1),(19,'1.0',0,'254','1',254,1),(20,'2.0',47124,'254','1',254,1),(21,'3.0',25718,'254','1',254,1),(22,'Romantisch',6000,'100','1',254,1),(23,'Wecker0_0',0,'0',NULL,254,1),(24,'Wecker1_0',5460,'0',NULL,254,1500),(25,'Halloween',9000,'254','1',254,1),(26,'Advent1',47124,'132','1',0,1500),(27,'Rot',0,'254','1',254,0),(28,'Orange',4000,'254','1',254,0),(29,'Advent0',47124,'0','1',0,0),(30,'App',54872,'255.0','1',254,NULL),(31,'Gemuetlich',12554,'176','1',225,NULL),(32,'Gemuetlich_1',12554,'60','1',255,NULL),(33,'Balkon_hell',12554,'180','1',255,0),(34,'Balkon_dunkel',12554,'0','1',255,0),(35,'WeckerRomantisch',6000,'100','1',254,60),(36,'Gruen_dunkel',25718,'50','1',254,0),(37,'AutoBel_Monaco',12554,'Monaco','1',254,2),(38,'AutoBel_Steh',12554,'Stehlampe','1',254,2),(39,'AutoBel_Stab',12554,'Stablampe','1',254,2),(40,'AutoBel_Kue',12554,'Kueche','1',254,2),(41,'AutoBel_Flur',12554,'FlurBoden','1',254,2),(42,'AutoBel_Monaco_Kino',12554,'Monaco_Kino','1',254,2),(43,'AutoBel_Steh_Kino',12554,'Stehlampe_Kino','1',254,2),(44,'AutoBel_Kue_Kino',12554,'Kueche_Kino','1',254,2),(45,'AutoBel_Flur_Kino',12554,'FlurBoden_Kino','1',254,2),(46,'AutoBel_Stab_Kino',12554,'Stablampe_Kino','1',254,2),(47,'Bad_hell',0,'254','1',0,NULL),(48,'Wecker6',12554,'254','1',111,600),(49,'Bad_dunkel',0,'20','1',254,0),(101,'LightstripKueche',NULL,NULL,NULL,NULL,NULL),(102,'Lightstrips 2',12554,'156','False',254,NULL),(103,'Stehlampe',12554,'157','False',254,0),(104,'BettSabina',NULL,NULL,NULL,NULL,NULL),(105,'BettChris',NULL,NULL,NULL,NULL,NULL),(106,'Monaco Lampe',NULL,NULL,NULL,NULL,NULL),(107,'Stablampe 1',12554,'156','False',254,NULL),(108,'Balkonlampe',NULL,NULL,NULL,NULL,NULL),(109,'Bad',0,'254','False',0,NULL),(110,'Stablampe 2',12554,'156','False',254,NULL),(111,'Buero',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Hue` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Table structure for table `LightstrSchlafzi`
--

DROP TABLE IF EXISTS `LightstrSchlafzi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LightstrSchlafzi` (
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
-- Dumping data for table `LightstrSchlafzi`
--

LOCK TABLES `LightstrSchlafzi` WRITE;
/*!40000 ALTER TABLE `LightstrSchlafzi` DISABLE KEYS */;
INSERT INTO `LightstrSchlafzi` VALUES (0,'Aus',0,0,0,0),(1,'Hell',255,255,255,0),(2,'SchlafziLangsamRot',255,0,0,600),(3,'Wecker1',50,0,0,150),(4,'Wecker2',132,0,0,50),(5,'Wecker3',156,156,0,50),(6,'Wecker4',200,200,200,50),(7,'Schlafen1',100,25,0,0),(8,'Schlafen2',0,0,0,60),(9,'Rot',255,0,0,0),(10,'Dunkerot',100,0,0,0),(11,'Romantisch',120,30,0,0),(12,'Wecker0a',10,0,0,300),(13,'WeckerRomantisch',120,30,0,60),(14,'WeckerSonntags0',100,0,0,1200),(15,'WeckerSonntags1',255,255,255,1200),(16,'Wecker6',255,255,255,600);
/*!40000 ALTER TABLE `LightstrSchlafzi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Marantz`
--

DROP TABLE IF EXISTS `Marantz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Marantz` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Power` varchar(45) DEFAULT NULL,
  `Volume` varchar(45) DEFAULT NULL,
  `Source` varchar(45) DEFAULT NULL,
  `Mute` varchar(45) DEFAULT NULL,
  `Display` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Marantz`
--

LOCK TABLES `Marantz` WRITE;
/*!40000 ALTER TABLE `Marantz` DISABLE KEYS */;
INSERT INTO `Marantz` VALUES (1,'An','True',NULL,NULL,NULL,NULL),(2,'Aus','False',NULL,NULL,NULL,NULL),(3,'TV','True','0-25','11',NULL,NULL),(4,'RaspBMC','True',NULL,'99',NULL,NULL),(5,'Return','True','0-30','CC','False',NULL),(6,'Sonos','True','0-30','CC',NULL,NULL),(7,'Stumm','True',NULL,NULL,'2',NULL),(8,'unStumm','True',NULL,NULL,'1',NULL),(9,'Aktuell','True','0-25','11','False',NULL),(10,'PS3','True','0-25','22',NULL,NULL),(11,'Durchsage','True','0-25','CC',NULL,NULL),(12,'DisplayAn',NULL,NULL,NULL,NULL,'1'),(13,'DisplayAus',NULL,NULL,NULL,NULL,'4');
/*!40000 ALTER TABLE `Marantz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Moisture`
--

DROP TABLE IF EXISTS `Moisture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Moisture` (
  `idMoisture` int(11) NOT NULL AUTO_INCREMENT,
  `Date` datetime DEFAULT NULL,
  `Value` decimal(4,0) DEFAULT NULL,
  PRIMARY KEY (`idMoisture`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Moisture`
--

LOCK TABLES `Moisture` WRITE;
/*!40000 ALTER TABLE `Moisture` DISABLE KEYS */;
/*!40000 ALTER TABLE `Moisture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Schlafzimmer_H`
--

DROP TABLE IF EXISTS `Schlafzimmer_H`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Schlafzimmer_H` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` decimal(3,1) DEFAULT NULL,
  `Date` datetime DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Schlafzimmer_H`
--

LOCK TABLES `Schlafzimmer_H` WRITE;
/*!40000 ALTER TABLE `Schlafzimmer_H` DISABLE KEYS */;
/*!40000 ALTER TABLE `Schlafzimmer_H` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Schlafzimmer_T`
--

DROP TABLE IF EXISTS `Schlafzimmer_T`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Schlafzimmer_T` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` decimal(3,1) DEFAULT NULL,
  `Date` datetime DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Schlafzimmer_T`
--

LOCK TABLES `Schlafzimmer_T` WRITE;
/*!40000 ALTER TABLE `Schlafzimmer_T` DISABLE KEYS */;
/*!40000 ALTER TABLE `Schlafzimmer_T` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Settings`
--

LOCK TABLES `Settings` WRITE;
/*!40000 ALTER TABLE `Settings` DISABLE KEYS */;
INSERT INTO `Settings` VALUES (0,'Alarmanlage','Ein',NULL,NULL),(1,'Anwesenheit','2',NULL,NULL),(2,'Status','Schlafen',NULL,NULL),(3,'Zusatz_Status','Leer',NULL,NULL),(4,'Autorestart','2015-11-20 17:27:29',NULL,NULL),(5,'Tempbereich','inactive',NULL,NULL),(6,'NumRestart','0',NULL,NULL),(7,'XS1_off','inactive',NULL,NULL),(8,'Laststart','2015-11-20 17:27:30',NULL,NULL),(9,'AV_cmd','1',NULL,NULL),(10,'Kommando','[\'DisplayAn\',\'Aus\']',NULL,NULL),(11,'Temp_Alarm','inactive',NULL,NULL),(12,'Durchsage','Wecker Morgen um 6 Uhr 15, das ist in 8 Stunden und 55 Minuten.',NULL,NULL),(13,'Beleuchtung','Aus',NULL,NULL),(14,'TempAlarmSchlafzi','20',NULL,NULL),(15,'Licht_Schlafzi','Aus',NULL,NULL),(16,'Wohnzimmer_Decke','fixed',NULL,NULL),(17,'Esszimmer','dunkler',NULL,NULL),(18,'Licht_Kueche','An',NULL,NULL),(19,'Meldung','Leer',NULL,NULL),(20,'TempSettingWohnziAnw','25.5',NULL,NULL),(21,'TempSettingWohnziAbw','23.5',NULL,NULL),(22,'Schluessel_Christoph','0',NULL,NULL),(23,'Schluessel_Sabina','0',NULL,NULL),(24,'Schluessel_Christoph_neu','0',NULL,NULL),(25,'Schluessel_Sabina_neu','0',NULL,NULL),(26,'TempSteuerung','Ein',1,'Temperatur Alarme'),(27,'Fern_Bett','Schlafen',NULL,NULL),(28,'Sideboard','Loop2',NULL,NULL),(29,'Schluessel_Besuch','0',NULL,NULL),(30,'Schluessel_Besuch_neu','0',NULL,NULL),(31,'Einbruch','False',NULL,NULL),(32,'Balkontuer','0.0',NULL,NULL),(33,'Next_alarm','Wecker Morgen um 6 Uhr 15, das ist in 8 Stunden und 55 Minuten.',NULL,NULL),(34,'Christoph_anwesend','1',NULL,NULL),(35,'Sabina_anwesend','1',NULL,NULL),(36,'AutoLicht','Ein',1,'Automatische Lichtszenen'),(37,'Temperatur_Wohnzi','24.7',NULL,NULL),(38,'Temperatur_Schlafzi','24.8',NULL,NULL),(39,'T_Wohnzi_T_Balkon','less',NULL,NULL),(40,'T_Schlafzi_T_Balkon','less',NULL,NULL),(41,'Notify_Sabina','Ein',1,'Nachrichten an Sabinas Handy'),(42,'Notify_Christoph','Ein',NULL,NULL),(43,'Notification_Visuell','Aus',1,'Lichter blinken bei Nachrichten'),(44,'LightstripKueche','1',NULL,NULL),(45,'Sideb_OR','0',NULL,NULL),(46,'Sideb_OM','0',NULL,NULL),(47,'Sideb_OL','0',NULL,NULL),(48,'Helligkeit','0',NULL,NULL),(49,'Restart_PIs','Aus',1,'Restart also PIs'),(50,'Halloween','Aus',1,'Halloween Beleuchtung'),(51,'Kino_Beleuchtung','Aus',1,'Kino Beleuchtung'),(52,'Kino_Beleuchtung_Auto','Aus',1,'Auto Kino Beleuchtung'),(53,'AV_mode','Aus',NULL,NULL),(54,'Kuechentuer','0.0',NULL,NULL),(55,'Haustuer','0',NULL,NULL),(57,'T_WohnZi','normal',NULL,NULL),(58,'T_SchlafZi','normal',NULL,NULL),(59,'Fenster_override','Aus',NULL,NULL),(60,'Frostalarm','Ein',1,'Frostalarm'),(61,'SchlafZiFenster','0',NULL,NULL),(62,'Heizung_eins','Aus',1,'Heizung aussgeschaltet'),(63,'Heizung_auss','Aus',1,'Heizung eingeschaltet');
/*!40000 ALTER TABLE `Settings` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sideboard`
--

LOCK TABLES `Sideboard` WRITE;
/*!40000 ALTER TABLE `Sideboard` DISABLE KEYS */;
INSERT INTO `Sideboard` VALUES (1,'Aus','set_one_color','[0,15,30]',0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'Halloween','set_one_color','[0,15,30]',255,50,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'LefToRight','flash','[0,15,30]',255,255,0,'False','0.01','False','True',255,255,0),(4,'Rot','set_one_color','[0,15,30]',255,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'RightToLeft','flash','[30,15,0]',0,255,0,'False','0.01','False','True',0,255,0),(6,'Hell','set_one_color','[0,15,30]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,'Loop0','set_one_color','[0,15,30]',0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8,'Loop1','set_one_color','[0,15,30]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(9,'Loop2','set_one_color','[0,15,30]',255,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(10,'Loop3','set_one_color','[0,15,30]',0,255,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(11,'Loop4','set_one_color','[0,15,30]',0,0,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(12,'Loop5','set_one_color','[0,15,30]',0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(13,'Loop6','set_one_color','[15]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(14,'Loop7','flash','[0]',0,255,0,'False','0.01','False','True',255,255,255),(15,'Loop8','flash','[30]',0,255,0,'True','0.01','False','True',255,255,255),(16,'Abends','set_one_color','[0,15,30]',255,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(17,'Weiss50','set_one_color','[0,15,30]',50,50,50,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(18,'Weiss','set_one_color','[0,15,30]',255,255,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,'Weiss25','set_one_color','[0,15,30]',25,25,25,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,'Blau','set_one_color','[0,15,30]',0,0,255,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(21,'App','set_one_color','[0,15,30]',0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(22,'LinksAn1','flash','[0,15]',255,255,255,'False','0.05','True','False',NULL,NULL,NULL),(23,'Rot125','set_one_color','[0,15,30]',70,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(24,'Weiss12','set_one_color','[0,15,30]',5,5,5,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(25,'LinksAn2','flash','[30]',255,255,255,'False','0.05','False',NULL,NULL,NULL,NULL),(26,'Kino','set_one_color','[0,15,30]',25,5,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,'Kino_Mitte','set_one_color','[0,15,30]',10,2,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Sideboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sonos`
--

DROP TABLE IF EXISTS `Sonos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sonos` (
  `Name` varchar(20) NOT NULL,
  `MasterZone` varchar(35) DEFAULT NULL,
  `Pause` int(11) DEFAULT NULL,
  `Sender` varchar(300) DEFAULT NULL,
  `Radio` int(11) DEFAULT NULL,
  `TitelNr` int(11) DEFAULT NULL,
  `Time` varchar(45) DEFAULT NULL,
  `PlayListNr` varchar(45) DEFAULT NULL,
  `Volume` int(11) DEFAULT NULL,
  PRIMARY KEY (`Name`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sonos`
--

LOCK TABLES `Sonos` WRITE;
/*!40000 ALTER TABLE `Sonos` DISABLE KEYS */;
INSERT INTO `Sonos` VALUES ('Bad','RINCON_000E5830220001400',0,'',0,0,'','34',20),('Chris','Own',0,NULL,0,1,'0:00:00','44',NULL),('ChrisAktuell','Own',0,'x-file-cifs://SERVER/Musik/Neuer%20Ordner/Podcasts/rj_russisch_lektion_036.mp3',0,36,'0:02:53','51',35),('DRS3','Own',0,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,NULL,NULL,NULL,NULL),('Duschen','Own',0,NULL,0,1,'0:00:00','43',40),('InputWohnZi','Own',0,'x-rincon-stream:RINCON_000E58232A2601400',1,NULL,NULL,NULL,NULL),('Klingelton','Own',0,NULL,0,1,'0:00:00','45',NULL),('Kueche','Own',1,'',1,0,'0:00:00','40',16),('MasterBad','RINCON_000E583138BA01400',0,NULL,NULL,NULL,NULL,NULL,NULL),('MasterSchlafZi','RINCON_000E5830220001400',0,NULL,NULL,NULL,NULL,NULL,20),('MasterSchlafZiWecken','RINCON_000E5830220001400',0,NULL,NULL,NULL,NULL,NULL,12),('MasterWohnZi','RINCON_000E58232A2601400',0,NULL,NULL,NULL,NULL,NULL,NULL),('Nachrichtenton','Own',0,NULL,0,1,'0:00:00','46',NULL),('Romantisch','Own',0,'x-rincon-mp3radio://pub5.radiotunes.com:80/radiotunes_mellowsmoothjazz',1,0,'0:00:00',NULL,10),('SabinaBeeil','Own',0,'x-rincon-mp3radio://translate.google.com/translate_tts?tl=de&amp;q=es+sind+noch+10+minuten',1,0,'0:00:00',NULL,30),('Schlafen','Own',0,'aac://stream.srg-ssr.ch/m/rsp/aacp_96',1,NULL,NULL,NULL,20),('SchlafZi','Own',1,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,1,'0:00:00','35',12),('Stumm',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0),('Swisspop','Own',0,'aac://stream.srg-ssr.ch/m/rsp/aacp_96',1,1,'0:00:00',NULL,NULL),('TextToSonos','Own',0,NULL,0,1,'0:00:00','47',NULL),('unStumm',NULL,NULL,NULL,NULL,NULL,NULL,NULL,20),('VolDurchsage',NULL,NULL,NULL,NULL,NULL,NULL,NULL,35),('VolMorgens',NULL,NULL,NULL,NULL,NULL,NULL,NULL,10),('VolMorgensBad',NULL,NULL,NULL,NULL,NULL,NULL,NULL,25),('VolMorgensKu',NULL,NULL,NULL,NULL,NULL,NULL,NULL,20),('VolWohnzi',NULL,NULL,NULL,NULL,NULL,NULL,NULL,80),('Wecker1','Own',0,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,1,'0:00:00','41',5),('Wecker2','Own',0,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,1,'0:00:00','42',NULL),('WeckerAlternative','Own',0,NULL,0,0,'0:00:00','44',NULL),('WeckerPhase0','Own',0,'aac://stream.srg-ssr.ch/m/rsp/aacp_96',1,0,'0:00:00',NULL,5),('WeckerPhase0a','Own',0,'aac://stream.srg-ssr.ch/m/rsp/aacp_96',1,0,'0:00:00',NULL,0),('WeckerPhase1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,6),('WeckerPhase2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,7),('WeckerPhase3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,8),('WeckerPhase4','Own',0,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,0,'0:00:00',NULL,12),('WeckerRomantisch','Own',0,'x-rincon-mp3radio://pub5.radiotunes.com:80/radiotunes_mellowsmoothjazz',1,0,'0:00:00',NULL,6),('Weihnachten','Own',0,'x-rincon-mp3radio://pub6.radiotunes.com:80/radiotunes_christmas',1,1,'0:00:00',NULL,21),('WohnZi','RINCON_000E58232A2601400',0,'',0,0,'','33',80);
/*!40000 ALTER TABLE `Sonos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Szenen`
--

DROP TABLE IF EXISTS `Szenen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Szenen` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Priority` varchar(45) DEFAULT '0',
  `Beschreibung` text,
  `Durchsage` text,
  `Gruppe` varchar(45) DEFAULT 'Intern',
  `AppSzene` int(11) DEFAULT '0',
  `TV` varchar(45) DEFAULT NULL,
  `Amp` varchar(45) DEFAULT NULL,
  `SonosWohnZi` varchar(45) DEFAULT NULL,
  `SonosKueche` varchar(45) DEFAULT NULL,
  `SonosBad` varchar(45) DEFAULT NULL,
  `SonosSchlafZi` varchar(45) DEFAULT NULL,
  `Wohnzimmer_Decke` text,
  `Stablampe 1` varchar(45) DEFAULT NULL,
  `Stablampe 2` varchar(45) DEFAULT NULL,
  `Stehlampe` varchar(45) DEFAULT NULL,
  `Sideboard` varchar(45) DEFAULT NULL,
  `Sideb_oben` varchar(45) DEFAULT NULL,
  `Sideb_links` varchar(45) DEFAULT NULL,
  `Sideb_mitte` varchar(45) DEFAULT NULL,
  `Sideb_rechts` varchar(45) DEFAULT NULL,
  `Kueche` varchar(45) DEFAULT NULL,
  `LightstripKueche` varchar(45) DEFAULT NULL,
  `Esszimmer` text,
  `Bad` varchar(45) DEFAULT NULL,
  `Buero` varchar(45) DEFAULT NULL,
  `Monaco Lampe` varchar(45) DEFAULT NULL,
  `Diele` varchar(45) DEFAULT NULL,
  `Reduit` text,
  `Schlafzimmer` varchar(45) DEFAULT NULL,
  `LightstripSchlafzi` varchar(45) DEFAULT NULL,
  `BettSabina` varchar(45) DEFAULT NULL,
  `BettChris` varchar(45) DEFAULT NULL,
  `Elchlampe` varchar(45) DEFAULT NULL,
  `LightStrips 2` varchar(45) DEFAULT NULL,
  `Adventslichter` varchar(45) DEFAULT NULL,
  `Balkonlampe` varchar(45) DEFAULT NULL,
  `Weihnachtsbaum` varchar(45) DEFAULT NULL,
  `Video_Audio` varchar(45) DEFAULT NULL,
  `Lattenrost` varchar(45) DEFAULT NULL,
  `RaspberryPi` enum('100','0') DEFAULT NULL,
  `PC_Peripherie` varchar(45) DEFAULT NULL,
  `Webcams` varchar(45) DEFAULT NULL,
  `Saugstauber` varchar(45) DEFAULT NULL,
  `Pflanzen` varchar(45) DEFAULT NULL,
  `Urlaub` int(11) DEFAULT NULL,
  `AV_mode` varchar(45) DEFAULT NULL,
  `TuerSPi` varchar(45) DEFAULT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `Zusatz_Status` text,
  `Szene_folgt` text,
  `folgt_nach` varchar(45) DEFAULT NULL,
  `Bedingung` text,
  `XS1_Bedingung` text,
  `Zusatz_Bedingung` text,
  `Auto_Mode` varchar(45) DEFAULT NULL,
  `set_Task` varchar(45) DEFAULT NULL,
  `set_Task_zuhause` varchar(45) DEFAULT NULL,
  `Interner_Befehl` text,
  `LastUsed` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=9013 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Szenen`
--

LOCK TABLES `Szenen` WRITE;
/*!40000 ALTER TABLE `Szenen` DISABLE KEYS */;
INSERT INTO `Szenen` VALUES (0,'Device_Typ','0',NULL,NULL,'Intern',0,'TV','Amp','Sonos','Sonos','Sonos','Sonos','EZControl','Hue','Hue','Hue','EZControl','TF_LEDs','TF_LEDs','TF_LEDs','TF_LEDs','EZControl','Hue','EZControl','Hue','Hue','Hue','EZControl','EZControl','EZControl','LightstripSchlafzi','Hue','Hue','EZControl','Hue','EZControl','Hue','EZControl','EZControl','EZControl','','EZControl','EZControl','EZControl','EZControl',NULL,NULL,'TuerSPi',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(1,'Auto_Mode','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'auto','auto','auto',NULL,'auto','auto','auto','auto',NULL,'auto',NULL,NULL,NULL,'auto',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'auto',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'Alles_ein','0','Alles ein',NULL,'Makros',10,NULL,NULL,'An','An','An','An',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100','100',NULL,'100','0',NULL,NULL,NULL,NULL,'Wach','Wach','{\'AutoLicht\':\'Ein\',\'Fern_Bett\':\'Wach\',\'Zusatz_Status\':\'Leer\',\'Alarmanlage\':\'Aus\',\'Fenster_override\':\'Aus\'}','[\'Webcam_aus\',\'AutoBeleuchtung\']','[10,0]','{\'Einbruch\':\'False\'}',NULL,NULL,NULL,'Unlock','Tag','activate_usb_keys','2015-11-20 17:30:41'),(3,'Alles_aus','0','Alles aus',NULL,'Makros',20,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100','100',NULL,NULL,NULL,NULL,NULL,'Alarm_Blau',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AmGehen','Am Gehen',NULL,'[\'TuerFensterCheck\',\'Alles_aus_1\',\'Alles_aus_5\']','[0,0,600]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 07:02:45'),(4,'Alles_aus_1','0',NULL,NULL,'Intern',0,'KEY_POWEROFF','[\'DisplayAn\',\'Aus\']','Aus','Aus','Aus','Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'Alles_aus_2\']','[2]','{\'Balkontuer\':\'0.0\',\'Kuechentuer\':\'0.0\',\'SchlafZiFenster\':\'0.0\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 07:02:47'),(5,'Alles_aus_2','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,'0',NULL,NULL,'Aus','0',NULL,'Aus','Aus','Aus','0','[\'auto\',\'Aus\']','0','Aus','Aus','Aus',NULL,NULL,'0','Aus','SZ_Aus','SZ_Aus','0','Gruen_dunkel',NULL,'Aus',NULL,'0',NULL,NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL,'Am Gehen',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 07:02:49'),(6,'Alles_aus_3','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Alarm_Gruen',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Am Gehen',NULL,NULL,NULL,'{\'Status\':[\'Am Gehen\'], \'Balkontuer\':\'0.0\',\'Kuechentuer\':\'0.0\',\'SchlafZiFenster\':\'0.0\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 07:02:59'),(7,'Alles_aus_4','0','Gegangen',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0','0',NULL,NULL,NULL,NULL,NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,NULL,NULL,'Gegangen','Gegangen',NULL,'[\'Alles_aus_5\']','[600]',NULL,NULL,NULL,NULL,'Lock',NULL,NULL,'2015-11-20 07:03:05'),(8,'Alles_aus_5','0','Alles aus Alarmanlage scharf',NULL,'Intern',0,'KEY_POWEROFF','[\'DisplayAn\',\'Aus\']','Aus','Aus','Aus','Aus','0',NULL,NULL,'Aus','0',NULL,'Aus','Aus','Aus','0','[\'auto\',\'Aus\']','0',NULL,NULL,'Aus','0','0','0','Aus','SZ_Aus','SZ_Aus','0','Aus',NULL,'Aus',NULL,'0',NULL,NULL,'0','100',NULL,NULL,NULL,NULL,'Alarmanlage_weg','Abwesend','{\'Fern_Bett\':\'Abwesend\',\'Zusatz_Status\':\'Leer\',\'Alarmanlage\':\'Ein\'}',NULL,NULL,'{\'Status\':[\'Gegangen\',\'Am Gehen\',\'Abwesend\']}',NULL,NULL,NULL,NULL,NULL,'deactivate_usb_keys','2015-11-20 17:28:41'),(9,'was_vergessen','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100','100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-15 15:25:46'),(11,'einer_weg','0','leer',NULL,'Makros',0,'KEY_POWEROFF','[\'DisplayAn\',\'Aus\']','Pause','Pause','Pause',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0','[\'auto\',\'Aus\']','0','Aus','Aus',NULL,'0','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0',NULL,NULL,'0',NULL,NULL,NULL,NULL,NULL,'einer_gegangen',NULL,'{\'Zusatz_Status\':\'Leer\'}','[\'einer_weg_2\']','[600]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-19 07:10:56'),(12,'einer_weg_2','0','leer',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,NULL,NULL,'Alarmanlage_nachts','Schlafen','{\'Fern_Bett\':\'Schlafen\',\'Alarmanlage\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-19 07:20:57'),(13,'Heimgekommen','0','Heimgekommen',NULL,'Makros',0,NULL,NULL,'Return','Return','Return','Return','0','Aus','Aus','Aus','0',NULL,'Aus','Aus','Aus','0','[\'auto\',\'Aus\']','0',NULL,NULL,'Aus',NULL,NULL,'0','Aus','Aus','Aus','0','Aus',NULL,NULL,NULL,'100','100',NULL,'100','0',NULL,NULL,NULL,NULL,'Wach','Wach','{\'Fern_Bett\':\'Wach\',\'Einbruch\':\'False\',\'Zusatz_Status\':\'Leer\',\'AutoLicht\':\'Ein\',\'Alarmanlage\':\'Aus\',\'Fenster_override\':\'Aus\'}','[\'AutoBeleuchtung\',\'keys_in_hub\']','[1,900]',NULL,NULL,NULL,NULL,NULL,NULL,'activate_usb_keys','2015-11-20 17:27:43'),(14,'Saugstauber','0','Staubsauger',NULL,'Makros',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'-1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-14 18:21:29'),(15,'Schlafen1','0','Schlafen','Am Schlafen gehen','Makros',0,NULL,NULL,NULL,NULL,'[\'Durchsage\',\'MasterSchlafZi\']','Schlafen',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Bad_hell',NULL,NULL,NULL,NULL,NULL,'Schlafen1',NULL,NULL,'100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Am Schlafen gehen','{\'Fern_Bett\':\'Am Schlafen gehen\',\'Kino_Beleuchtung\':\'Aus\'}','[\'TuerFensterCheck\',\'Schlafen2\']','[0,1]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 21:19:28'),(16,'Schlafen2','0','Schlafen 2',NULL,'Intern',0,'KEY_POWEROFF','[\'DisplayAn\',\'Aus\']','Pause','Pause',NULL,NULL,'0','Aus','Aus','Aus','0',NULL,'Aus','Aus','Aus','0','[\'auto\',\'Aus\']','0',NULL,NULL,'Aus','0','0',NULL,NULL,'SZ_Aus','SZ_Aus',NULL,'Aus','0','Aus','0','0','100',NULL,'0',NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Balkontuer\':\'0.0\',\'Kuechentuer\':\'0.0\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 21:19:31'),(17,'Schlafen3','0','Schlafen 3',NULL,'Intern',0,NULL,NULL,'Aus','Aus','Aus','WeckerAnsage','0','Aus','Aus','Aus','0',NULL,'Aus','Aus','Aus','0','[\'auto\',\'Aus\']','0','SZ_Aus','Aus','Aus','0','0','0','Schlafen2','SZ_Aus','SZ_Aus','0','Aus',NULL,'Aus',NULL,'0',NULL,NULL,NULL,'100',NULL,NULL,NULL,NULL,'Alarmanlage_nachts','Schlafen','{\'Fern_Bett\':\'Schlafen\',\'Alarmanlage\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Nacht',NULL,'2015-11-20 21:20:55'),(18,'TuerFensterCheck','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'BalkonTCheck\',\'KuechenTCheck\',\'SchlafziFCheck\']','[0,0,0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 21:19:28'),(19,'BalkonTCheck','2','Balkon Tuer noch auf',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Rot',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Balkontuer\':\'1.0\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-30 22:22:08'),(20,'KuechenTCheck','2','Fenster Kueche noch auf',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Rot',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Kuechentuer\':\'1.0\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-28 07:20:07'),(21,'SchlafziFCheck','2','Fenster Schlafzimmer noch auf',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Rot',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Status\':[\'Wach\',\'Gegangen\',\'Am Gehen\',\'Abwesend\',\'Urlaub\'],\'SchlafZiFenster\':\'1\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-13 06:49:05'),(22,'Webcam_aus','0','Webcam aus',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 17:30:51'),(23,'keys_in_hub','0','Pruefe of Schluessel an Platz',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'keys_in_hub','2015-11-20 17:42:44'),(24,'einer_heimgekommen','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0','Aus',NULL,NULL,'0',NULL,'100',NULL,'100','100',NULL,NULL,NULL,'0',NULL,NULL,NULL,NULL,'Gruen','einer_wach','{\'Fern_Bett\':\'einer_wach\',\'Einbruch\':\'False\',\'Zusatz_Status\':\'Abends\',\'Alarmanlage\':\'Aus\',\'Fenster_override\':\'Aus\'}','[\'AutoBeleuchtung\',\'Webcam_aus\',\'LedsAus\']','[0,10,5]',NULL,NULL,NULL,NULL,NULL,NULL,'activate_usb_keys','2015-11-18 21:10:51'),(27,'gemuetlich','0','Gemuetliches Licht',NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Gemuetlich','Gemuetlich','Gemuetlich','0',NULL,'Rot','Weiss25','Rot',NULL,NULL,NULL,NULL,NULL,'Gemuetlich',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Abends','100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Beleuchtung\':\'Abends\',\'Status\':\'Wach\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-16 16:18:12'),(28,'Wohnzimmer_hell','0','Wohnzimmer hell',NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,'100','[\'man\',\'Hell\']','[\'man\',\'Hell\']','[\'man\',\'Hell\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,NULL,'100',NULL,NULL,NULL,NULL,NULL,NULL,'[\'man\',\'Hell\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-07 18:09:37'),(29,'sz_Schlafen_stealth','0','Schlafen gehen ohne Licht',NULL,'App',25,'KEY_POWEROFF','[\'DisplayAn\',\'Aus\']','Aus','Aus','Aus','Pause','0','[\'auto\',\'Aus\']','[\'auto\',\'Aus\']','[\'auto\',\'Aus\']','0','[\'auto\',\'Aus\']',NULL,NULL,NULL,'0','[\'auto\',\'Aus\']','0',NULL,NULL,'Aus','0','0','0','Aus','Aus','Aus','0','Aus','0',NULL,'0','0',NULL,NULL,'0',NULL,NULL,NULL,NULL,NULL,'Alarmanlage_nachts','Schlafen','{\'Fern_Bett\':\'Schlafen\',\'Alarmanlage\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-18 21:24:06'),(31,'Alle_Lichter_Aus','0','Alle Lichter aus',NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,'0','[\'auto\',\'Aus\']','[\'auto\',\'Aus\']','[\'auto\',\'Aus\']','0','[\'auto\',\'Aus\']',NULL,NULL,NULL,'0','[\'auto\',\'Aus\']','0',NULL,NULL,'Aus','0','0','0','Aus','SZ_Aus','SZ_Aus','0','[\'auto\',\'Aus\']','0','Aus','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'AutoBeleuchtung\']','[0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-14 08:26:12'),(32,'Doppelklick','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Alarm_Gruen',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Doppelklick',NULL,'[\'Doppleklick_reset\']','[2.5]','{\'Status\':\'Wach\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 19:42:00'),(34,'Doppleklick_reset','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wach','Wach','{\'Fern_Bett\':\'Wach\',\'Alarmanlage\':\'Aus\',\'Fenster_override\':\'Aus\'}','[\'AutoBeleuchtung\']','[0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 19:42:03'),(35,'Besuch','0',NULL,NULL,'ToSort',0,NULL,NULL,'An','An','An','An',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,NULL,'0',NULL,NULL,NULL,NULL,NULL,'Besuch','{\'Fern_Bett\':\'Besuch\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'send_wc_pix',NULL),(37,'Bodenbel_ein','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'SZ_hell',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Diele\':\'100.0\'}',NULL,NULL,NULL,NULL,NULL,'2015-09-24 20:16:39'),(38,'Bodenbel_aus','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Beleuchtung\':\'Aus\'}','{\'Diele\':\'0.0\'}',NULL,NULL,NULL,NULL,NULL,'2015-09-24 22:47:28'),(39,'Bodenbel_gemu','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Abends',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Beleuchtung\':\'Abends\'}','{\'Diele\':\'0.0\'}',NULL,NULL,NULL,NULL,NULL,'2015-09-24 00:04:46'),(40,'AutoBeleuchtung','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'Gemuetlich_0\',\'Gemuetlich_1\',\'Gemuetlich_2\',\'Gemuetlich_3\',\'Halloween\',\'Kino_Beleuchtung\']','[0,0,0,0,0,0]',NULL,NULL,NULL,'True',NULL,NULL,NULL,'2015-11-20 21:19:00'),(41,'Gemuetlich_0','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AutoBel_Stab','AutoBel_Stab','AutoBel_Steh',NULL,NULL,'Aus','Aus','Aus',NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'AutoLicht\':\'Ein\',\'Helligkeit\':\'>60\'}',NULL,NULL,'True',NULL,NULL,NULL,'2015-11-16 15:30:14'),(42,'Gemuetlich_1','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AutoBel_Stab','AutoBel_Stab','AutoBel_Steh',NULL,NULL,'Aus','Aus','Aus',NULL,'AutoBel_Kue',NULL,NULL,NULL,'AutoBel_Monaco',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AutoBel_Flur',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'AutoLicht\':\'Ein\',\'Halloween\':\'Aus\',\'Kino_Beleuchtung\':\'Aus\',\'Helligkeit\':\'>34<59\'}',NULL,NULL,'True',NULL,NULL,NULL,'2015-11-20 19:58:12'),(43,'Gemuetlich_2','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AutoBel_Stab','AutoBel_Stab','AutoBel_Steh',NULL,NULL,'Rot','Weiss25','Rot',NULL,'AutoBel_Kue',NULL,NULL,NULL,'AutoBel_Monaco',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AutoBel_Flur',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'AutoLicht\':\'Ein\',\'Halloween\':\'Aus\',\'Kino_Beleuchtung\':\'Aus\',\'Helligkeit\':\'>22<35\'}',NULL,NULL,'True',NULL,NULL,NULL,'2015-11-16 16:39:00'),(44,'Gemuetlich_3','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AutoBel_Stab','AutoBel_Stab','AutoBel_Steh',NULL,NULL,'Rot','Weiss25','Rot',NULL,'AutoBel_Kue',NULL,NULL,NULL,'AutoBel_Monaco',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AutoBel_Flur',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'AutoLicht\':\'Ein\',\'Halloween\':\'Aus\',\'Kino_Beleuchtung\':\'Aus\',\'Helligkeit\':\'<19\'}',NULL,NULL,'True',NULL,NULL,NULL,'2015-11-20 21:19:00'),(45,'AutoBelAus','0','Auto Beleuchtung aus',NULL,'App',30,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','Aus','Aus',NULL,NULL,'Aus','Aus','Aus',NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'AutoLicht\':\'Aus\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-26 18:47:47'),(46,'AutoBelEin','0','Auto Beleuchtung ein',NULL,'App',31,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'auto','auto','auto',NULL,NULL,'auto','auto','auto',NULL,'auto',NULL,NULL,NULL,'auto',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'auto',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'AutoLicht\':\'Ein\',\'Kino_Beleuchtung\':\'Aus\'}','AutoBeleuchtung','0','{\'Status\':\'Wach\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 19:58:50'),(47,'sz_FindMe','0','Finde Handys',NULL,'App',32,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'FindMe',NULL,NULL,'2015-11-12 21:12:34'),(48,'WeckerPhase0a','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'[\'An\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker0a',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecken','{\'Fern_Bett\':\'Wecken\'}','WeckerPhase1','300','{\'Status\':[\'Schlafen\',\'Wecken\',\'Wach\',\'Schlummern\',\'einer_wach\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 05:25:02'),(49,'WeckerPhase1a','0',NULL,NULL,'ToSort',0,NULL,NULL,'An','An','An','[\'An\',\'WeckerPhase0\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker1','Wecker1_0','Wecker1_0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecken','{\'Fern_Bett\':\'Wecken\'}','WeckerPhase2','150','{\'Status\':[\'Schlafen\',\'Wecken\',\'Wach\',\'Schlummern\',\'einer_wach\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-10 07:25:59'),(50,'WeckerPhase0','0','Standard Wecker start',NULL,'ToSort',0,NULL,NULL,'An','An','An','An',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecken','{\'Fern_Bett\':\'Wecken\'}','WeckerPhase0a','60','{\'Status\':[\'Schlafen\',\'Wecken\',\'Wach\',\'Schlummern\',\'einer_wach\']}',NULL,NULL,NULL,NULL,'Wecker',NULL,'2015-11-20 05:24:01'),(51,'WeckerPhase1','0',NULL,NULL,'ToSort',0,NULL,NULL,'An','An','An','[\'An\',\'WeckerPhase0\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker1','Wecker1_0','Wecker1_0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecken','{\'Fern_Bett\':\'Wecken\'}','WeckerPhase2','150','{\'Status\':[\'Schlafen\',\'Wecken\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 05:30:03'),(52,'WeckerPhase2','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'WeckerPhase1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Abends\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker2','Wecker2','Wecker2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerPhase3','50','{\'Status\':[\'Wecken\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 05:32:33'),(53,'WeckerPhase3','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'[\'MasterSchlafZiWecken\',\'VolMorgens\']','[\'MasterSchlafZiWecken\',\'VolMorgens\']','WeckerPhase2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker3','Wecker3','Wecker3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerPhase4','50','{\'Status\':[\'Wecken\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 05:33:23'),(54,'WeckerPhase4','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'[\'MasterSchlafZiWecken\',\'VolMorgens\']','[\'MasterSchlafZiWecken\',\'VolMorgens\']','WeckerPhase3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker4','Wecker4','Wecker4',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerPhase5','50','{\'Status\':[\'Wecken\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 05:34:13'),(55,'WeckerPhase5','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'WeckerPhase4',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wetter',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerPhase6','40','{\'Status\':[\'Wecken\']}',NULL,NULL,NULL,NULL,'Tag',NULL,'2015-11-20 05:35:04'),(56,'WeckerPhase6','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'VolMorgensKu','VolMorgensBad',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Bad_hell',NULL,NULL,NULL,NULL,NULL,'Wecker6','Wecker6','Wecker6',NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,'100','0',NULL,NULL,NULL,NULL,'Wach','Wach','{\'Fern_Bett\':\'Wach\',\'Alarmanlage\':\'Aus\',\'Fenster_override\':\'Aus\'}','Bad_start_zeitansage','0','{\'Status\':[\'Wecken\']}',NULL,NULL,NULL,NULL,'Tag',NULL,'2015-11-20 05:35:45'),(57,'Schlummern30','0',NULL,'30 minuten schlummern','ToSort',0,NULL,NULL,NULL,NULL,NULL,'[\'Pause\',\'Durchsage\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','SZ_Aus','SZ_Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Schlummern','{\'Fern_Bett\':\'Schlummern\'}','WeckerPhase0a','1800',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-18 22:16:36'),(58,'Schlummern60','0',NULL,'60 minuten schlummern','ToSort',0,NULL,NULL,NULL,NULL,NULL,'[\'Pause\',\'Durchsage\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','SZ_Aus','SZ_Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Schlummern','{\'Fern_Bett\':\'Schlummern\'}','WeckerPhase0a','3600',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-16 06:50:26'),(59,'WeckerAus','0',NULL,'Wecker ausgeschaltet','ToSort',0,NULL,NULL,NULL,NULL,NULL,'[\'Pause\',\'Durchsage\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,'0','Aus','SZ_Aus','SZ_Aus','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Alarmanlage_nachts','Schlafen','{\'Fern_Bett\':\'Schlafen\',\'AutoLicht\':\'Ein\',\'Alarmanlage\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-08-26 06:45:57'),(60,'WeckerMute','0',NULL,'Einer aufgestanden','ToSort',0,NULL,NULL,NULL,'MasterBad','DRS3','[\'Pause\',\'VolDurchsage\',\'WeckerAnsage\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Abends\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','SZ_Aus','SZ_Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0',NULL,NULL,NULL,NULL,NULL,'einer_wach','{\'Fern_Bett\':\'einer_wach\',\'Zusatz_Status\':\'Morgens\',\'Alarmanlage\':\'Aus\',\'Fenster_override\':\'Aus\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-19 06:48:06'),(61,'Schlummern15','0',NULL,'15 minuten schlummern','ToSort',0,NULL,NULL,NULL,NULL,NULL,'[\'Pause\',\'Durchsage\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','SZ_Aus','SZ_Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Schlummern','{\'Fern_Bett\':\'Schlummern\'}','WeckerPhase0a','900',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-20 05:06:56'),(62,'Schlummern180','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','SZ_Aus','SZ_Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Schlummern','{\'Fern_Bett\':\'Schlummern\'}','WeckerPhase1a','7200',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-10 05:25:58'),(63,'Radio_einer_wach','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'MasterBad','DRS3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Abends\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Zusatz_Status\':\'ZeitBad\'}','TimeBad','2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-19 06:36:04'),(64,'Schlummern240','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','SZ_Aus','SZ_Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Schlummern','{\'Fern_Bett\':\'Schlummern\'}','WeckerPhase1a','10800',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(65,'WeckerAusWach','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'Pause','Pause','Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0','Aus','SZ_Aus','SZ_Aus','0',NULL,NULL,NULL,NULL,'100',NULL,NULL,'100','0',NULL,NULL,NULL,NULL,'Wach','Wach','{\'Fern_Bett\':\'Wach\',\'Alarmanlage\':\'Aus\',\'Fenster_override\':\'Aus\'}','[\'AutoBeleuchtung\']','[0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-10 07:26:43'),(70,'Romantisch','0','Romantisch',NULL,'App',0,'KEY_POWEROFF','Aus','Pause','Pause','Pause','Romantisch','0','Aus','Aus','Aus','0',NULL,'Aus','Aus','Aus','0',NULL,'0',NULL,NULL,'Aus','0','0','0','Romantisch','Romantisch','Romantisch','0','Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-01 08:38:00'),(80,'Einbruch_1','0','Einbruch 1',NULL,'ToSort',0,NULL,NULL,NULL,'An','An','An',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Orange',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Einbruch_2','60','{\'Status\':[\'Schlafen\',\'Urlaub\',\'Abwesend\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-21 06:28:44'),(81,'Einbruch_2','3','Einbruch',NULL,'ToSort',0,NULL,NULL,NULL,'VolDurchsage','VolDurchsage','VolDurchsage','100','Rot','Rot','Rot',NULL,'Rot',NULL,NULL,NULL,'100',NULL,'100',NULL,NULL,'Rot','100','100','100','Rot','Rot','Rot','100','Rot',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,NULL,NULL,NULL,'Einbruch',NULL,'Einbruch_3','1','{\'Alarmanlage\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,'send_wc_pix','2015-11-16 07:29:00'),(82,'Einbruch_3','0','Einbruch 3',NULL,'ToSort',0,NULL,NULL,NULL,'Alarm','Alarm','Alarm',NULL,'Aus','Aus','Aus',NULL,NULL,'Aus','Aus','Aus',NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,'Aus',NULL,NULL,NULL,'Aus','Aus','Aus',NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Einbruch_4','2','{\'Alarmanlage\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-16 07:29:04'),(83,'Einbruch_4','0','Einbruch 4',NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Rot','Rot','Rot',NULL,'Rot',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Rot',NULL,NULL,NULL,'Rot','Rot','Rot',NULL,'Rot',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Einbruch_3','1','{\'Alarmanlage\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-16 07:29:03'),(84,'Einbruch_Sofort','0','Einbruch alle da','Einbruch','Intern',0,NULL,NULL,NULL,'An','An','An',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Einbruch\':\'True\'}','Einbruch_2','0','{\'Christoph_anwesend\':\'1\',\'Sabina_anwesend\':\'1\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-16 07:28:40'),(85,'EinbruchFenster','3.3','Einbruch am Fenster',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Alarmanlage\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(86,'EinbruchTuer','0','Tuer auf Einbruch check',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100','100',NULL,NULL,NULL,NULL,NULL,'Rot',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Alarmanlage_cntdwn',NULL,'{\'Einbruch\':\'True\'}','[\'Einbruch_2\',\'Einbruch_Sofort\']','[20,0]','{\'Alarmanlage\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-19 16:53:52'),(87,'EinbruchFensterSchlafzi','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'EinbruchFenster','0','{\'Status\':[\'Wach\',\'Gegangen\',\'Am Gehen\',\'Abwesend\',\'Urlaub\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 06:55:08'),(88,'Fenster_override','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Fenster_override\':\'Ein\',\'Balkontuer\':\'0.0\',\'Kuechentuer\':\'0.0\',\'Haustuer\':\'0\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-31 18:59:44'),(90,'Einer_schlafengegangen','0','Einer wach, einer geht schlafen',NULL,'Intern',90,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Schlafen1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'einer_wach',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Nacht',NULL,'2015-10-19 21:05:15'),(92,'Wach','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,'100','0',NULL,NULL,NULL,NULL,'Wach','Wach','{\'Fern_Bett\':\'Wach\',\'Alarmanlage\':\'Aus\',\'Fenster_override\':\'Aus\'}',NULL,NULL,'{\'Status\':[\'Wecken\',\'Schlummern\']}',NULL,NULL,NULL,NULL,'Tag',NULL,'2015-10-25 10:29:15'),(94,'TV','0','Fernsehen',NULL,'ToSort',0,'KEY_TV','TV','[\'VolWohnzi\',\'InputWohnZi\']','Pause','Pause','Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 18:10:53'),(96,'Kino_Beleuchtung','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AutoBel_Stab_Kino','AutoBel_Stab_Kino','AutoBel_Steh_Kino',NULL,NULL,'Kino','Kino_Mitte','Kino',NULL,'AutoBel_Kue_Kino',NULL,NULL,NULL,'AutoBel_Monaco_Kino',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AutoBel_Flur_Kino',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'AutoLicht\':\'Ein\',\'Kino_Beleuchtung\':\'Ein\'}',NULL,NULL,'True',NULL,NULL,NULL,'2015-11-13 21:08:28'),(98,'Kino_BeleuchtungSet','0','Kino Beleuchtung',NULL,'Lichter',32,NULL,'DisplayAus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Kino_Beleuchtung\':\'Ein\'}','Kino_Beleuchtung','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-13 19:48:24'),(100,'Media_aus','0','Video Audio aus',NULL,'ToSort',0,'KEY_POWEROFF','Aus','InputWohnZi','Pause','Pause','Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 17:28:31'),(102,'Duschen','0','Musik beim Duschen, TV aus',NULL,'ToSort',0,'KEY_POWEROFF','Aus','Pause','Pause','Duschen','MasterBad',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(104,'sz_Stumm_aus','0','Stumm aus',NULL,'App',0,NULL,'unStumm','unStumm','unStumm','unStumm','unStumm',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(106,'sz_ChrisMusik','0','Christophs Musik',NULL,'App',0,NULL,'Sonos','Chris','MasterWohnZi','MasterWohnZi','MasterWohnZi',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(110,'sz_Mute','0','Alles Stumm',NULL,'App',0,NULL,'Stumm','Stumm','Stumm','Stumm','Stumm',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(118,'sn_Schlafzi_leiser','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'leiser',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-07-26 09:58:27'),(120,'sn_Schlafzi_lauter','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'lauter',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-07-26 09:58:31'),(122,'SonosReturn','0',NULL,NULL,'ToSort',0,NULL,'Return','Return','Return','Return','Return',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(124,'SonosSave','0',NULL,NULL,'ToSort',0,NULL,'Save','Save','Save','Save','Save',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(132,'Swisspop','0','Radio Swisspop',NULL,'Audio',0,'KEY_POWEROFF','Sonos','Swisspop','[\'MasterWohnZi\',\'unStumm\']','[\'MasterWohnZi\',\'unStumm\']','[\'MasterWohnZi\',\'unStumm\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-25 16:55:21'),(133,'DRS3','0','Radio DRS3',NULL,'Audio',0,'KEY_POWEROFF','Sonos','DRS3','[\'MasterWohnZi\',\'unStumm\']','[\'MasterWohnZi\',\'unStumm\']','[\'MasterWohnZi\',\'unStumm\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-18 06:17:39'),(134,'sz_RaspBMC','0','RaspBMC',NULL,'App',0,'KEY_HDMI','RaspBMC','Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'RaspBMC_ein','10',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-05 17:47:14'),(136,'RaspBMC_ein','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-05 17:47:24'),(137,'Christmas_Radio','0','Christmas Radio',NULL,'ToSort',0,'KEY_POWEROFF','Sonos','[\'Weihnachten\',\'VolWohnzi\']','[\'MasterWohnZi\',\'unStumm\']','[\'MasterWohnZi\',\'unStumm\']','[\'MasterWohnZi\',\'unStumm\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(138,'TimeBad','0','Zeitdurchsage Bad',NULL,'Audio',0,NULL,NULL,NULL,NULL,'[\'Time\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'TimeBad','600','{\'Zusatz_Status\':\'ZeitBad\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 07:05:48'),(140,'Bad_start_zeitansage','0','Start Zeitansage Bad',NULL,'App',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Zusatz_Status\':\'ZeitBad\'}','TimeBad','2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 05:35:46'),(142,'Bad_stop_zeitansage','0','Stop Zeitansage Bad',NULL,'App',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Zusatz_Status\':\'leer\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(144,'sz_BadDurchsage','0','Durchsage Bad',NULL,'App',0,NULL,NULL,NULL,NULL,'[\'Durchsage\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 19:19:54'),(148,'SonosBadInpWohnzi','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'InputWohnZi',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-14 17:55:15'),(150,'SonosBadSRF3','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'DRS3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-13 05:53:19'),(152,'SonosBadSwPop','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'Swisspop',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-13 05:53:08'),(154,'SonosBadMastWohnzi','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'MasterWohnZi',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-08-26 07:46:46'),(156,'SonosBadMastSchlafzi','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'MasterSchlafZi',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(158,'TV_Kopfh','0',NULL,NULL,'ToSort',0,'KEY_TV',NULL,'InputWohnZi',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(160,'InfoDurchsage','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'[\'VolDurchsage\',\'Durchsage\']','[\'VolDurchsage\',\'Durchsage\']','[\'VolDurchsage\',\'Durchsage\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(162,'sz_SaveChris','0','Speichere Sonos Chris',NULL,'App',0,NULL,NULL,'SaveChris','SaveChris','SaveChris','SaveChris',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(164,'sz_PlaySavedC','0','Gespeicherte Liste Chris',NULL,'App',0,NULL,NULL,'ChrisAktuell','[\'MasterWohnZi\',\'unStumm\']','[\'MasterWohnZi\',\'VolDurchsage\']','[\'MasterWohnZi\',\'unStumm\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(166,'VolMorgensBad','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'VolMorgensBad',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-20 05:16:10'),(168,'SonosBadVolUp','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'lauter',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-16 08:00:47'),(170,'SonosBadVolDown','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'leiser',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-04 06:40:49'),(180,'Marantz_lauter','0','Marantz lauter',NULL,'Audio',0,NULL,'lauter',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-15 10:02:05'),(185,'Marantz_leiser','0','Marantz leiser',NULL,'Audio',0,NULL,'leiser',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-15 10:40:42'),(201,'Dimm_WZ','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,'dimmen',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-19 21:54:45'),(202,'Elchlampe','0','Elchlampe',NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'-1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-24 23:20:30'),(204,'Schlafzimmer_aus','0','Schlafzimmer aus',NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,'0','Aus','SZ_Aus','SZ_Aus','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 21:21:14'),(206,'Alle_Lichter_Ein','0','Alle Lichter ein',NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,'100','Hell','Hell','Hell','0',NULL,NULL,NULL,NULL,'100',NULL,'100',NULL,NULL,'Hell','100','100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(207,'SchlafZi_alles_an','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100','Hell','SZ_hell','SZ_hell','100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Licht_Schlafzi\':\'SchlafziAn\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 19:27:27'),(208,'SchlafZi_alles_aus','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0','Aus','SZ_Aus','SZ_Aus','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Licht_Schlafzi\':\'Aus\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 21:14:04'),(210,'Dimm_EZ','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'dimmen',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(250,'LightstripKue_1','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'LightstripKueche1_hell\',\'LightstripKueche1_aus\']','[0.1,0.1]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-19 07:46:11'),(251,'LightstripKueche1_hell','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'man\',\'SZ_Hell\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Kueche\':\'100.0\'}',NULL,NULL,NULL,NULL,NULL,'2015-09-19 06:53:55'),(252,'LightstripKueche1_aus','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Kueche\':\'0.0\'}',NULL,NULL,NULL,NULL,NULL,'2015-09-19 07:46:11'),(253,'LightstripKueche_eigens','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Romantisch',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'LightstripKueche_1\',\'LightstripKueche_2\',\'LightstripKueche_0\']','[0,0,0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-12 18:26:26'),(254,'LightstripKueche_aus','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-24 18:19:39'),(255,'LightstripKueche_0','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'auto\',\'Aus\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'LightstripKueche\':\'0\'}',NULL,NULL,'{\'LightstripKueche\':\'2\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-12 18:26:29'),(256,'LightstripKueche_1','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Romantisch',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'LightstripKueche\':\'1\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-24 11:47:59'),(257,'LightstripKueche_2','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'man\',\'SZ_Hell\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'LightstripKueche\':\'2\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-24 11:41:41'),(300,'WeckerRomantisch','0','Wecken Romantisch',NULL,'Intern',0,'KEY_POWEROFF','Aus','Pause','Pause','Pause','WeckerRomantisch','0','Aus','Aus','Aus','0',NULL,'Aus','Aus','Aus','0',NULL,'0',NULL,NULL,'Aus','0','0','0','WeckerRomantisch','Romantisch','WeckerRomantisch','0','Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-08 10:11:27'),(350,'WeckerSonntags0','0','Sonntags Wecker nur Licht',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerSonntags0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecken',NULL,'[\'WeckerSonntags1\']','[1200]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-01 09:49:00'),(355,'WeckerSonntags1','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerSonntags1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'Wach\']','[1200]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-01 10:09:00'),(600,'Fern_Esszi_2','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'Wach\',\'Sonos_Kueche_TV\',\'Sonos_Kueche_Pause\']','[0,0,0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-27 06:14:43'),(601,'Sonos_Kueche_TV','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'InputWohnZi',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-17 18:41:08'),(602,'Sonos_Kueche_Pause','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'AV_mode\':\'TV\'}','{\'Kueche\':\'0.0\'}',NULL,NULL,NULL,NULL,NULL,NULL),(804,'az_Alles_aus_4','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'Alles_aus_4\']','[0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-19 16:54:06'),(900,'ChannelUp','0','TV Kanal hoch',NULL,'TV',0,'KEY_CHUP',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-06 17:40:31'),(901,'ChannelDown','0','TV Kanal runter',NULL,'TV',0,'KEY_CHDOWN',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-08 11:03:09'),(905,'Prev_Channel','0','Letzter Kanal',NULL,'TV',0,'KEY_PRECH',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-11 09:52:02'),(1000,'Reset','0','Alles ein Reset',NULL,'ToSort',0,NULL,'TV','An','An','An','An',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'1',NULL,NULL,'1','0','1',NULL,0,NULL,'Wach','Wach','{\'Fern_Bett\':\'Wach\',\'Einbruch\':\'False\',\'Alarmanlage\':\'Aus\',\'Fenster_override\':\'Aus\'}',NULL,NULL,NULL,NULL,NULL,NULL,'Unlock',NULL,NULL,NULL),(1001,'Tuer_auf','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100','100',NULL,NULL,NULL,NULL,NULL,'Alarm_Blau',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'Alles_aus_3\']','[0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-14 17:01:20'),(1002,'Tuer_auf_oL','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'Alles_aus_3\']','[0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-17 17:00:44'),(1003,'Tuer_auf_AG','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100','100',NULL,NULL,NULL,NULL,NULL,'Alarm_Gruen',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'Alles_aus_3\']','[0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 07:02:59'),(1005,'sz_AbendBelEin','0','Abend Beleuchtung ein',NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Gemuetlich','Gemuetlich',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'gemuetlich\']','[0]',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-19 16:15:42'),(1006,'sz_AbendBelAus','0','Abend Beleuchtung aus',NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','Aus','Aus',NULL,NULL,'Aus','Aus','Aus',NULL,NULL,NULL,NULL,NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','0','Aus','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Status\':[\'Wach\',\'Schlafen\',\'Gegangen\',\'Am Gehen\',\'Abwesend\',\'Urlaub\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 01:04:47'),(1007,'sz_MorgenBelEin','0','Morgen Beleuchtung ein',NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,'100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 06:38:54'),(1008,'sz_MorgenBelAus','0','Morgen Beleuchtung aus',NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0','Aus','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 07:38:54'),(1013,'az_Urlaub','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Urlaub','{\'Fern_Bett\':\'Urlaub\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-08-10 16:04:11'),(1014,'Bettlampe_Chris','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'sz_toggle',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-15 22:55:23'),(1015,'Bettlampe_Sabina','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'sz_toggle',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-08 11:44:55'),(1016,'Bettlampe_Chris_hell','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Hell',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-07 18:32:44'),(1017,'Halloween','0','Halloween',NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Halloween','Halloween','Halloween','0',NULL,'Halloween','Halloween','Halloween',NULL,'Halloween',NULL,NULL,NULL,'Halloween',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Halloween',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Halloween\':\'Ein\',\'Helligkeit\':\'<50\',\'Kino_Beleuchtung\':\'Aus\'}',NULL,NULL,'True',NULL,NULL,NULL,'2015-10-29 20:23:00'),(1500,'Bad','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'toggle',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-18 21:23:51'),(1501,'Bad_hell','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Bad_hell',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-15 15:20:22'),(1502,'Bad_dunkel','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Bad_dunkel',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-18 21:13:22'),(1600,'Buero_hell','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Hell',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-07 16:19:03'),(1601,'Buero','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'toggle',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 19:43:47'),(1602,'Buero_romantisch','0',NULL,NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Romantisch',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-18 17:40:32'),(2000,'Bett_Chris_dunkel_1','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Dunkelrot',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Fern_Bett\':\'Bett_Chris_dunkel_1\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-08-22 08:58:05'),(2001,'Bett_Chris_aus_1','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'SZ_Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Fern_Bett\':\'Schlafen\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-08-22 08:58:11'),(2003,'Stablampe','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'toggle','toggle',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-19 19:15:10'),(2004,'Eingang','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'toggle',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-27 14:00:12'),(2005,'Weihnachtsbaum','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'-1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2006,'Balkonlampe','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'toggle',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-31 19:51:46'),(2007,'Stehlampe','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'toggle',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-12 18:32:51'),(2008,'Monaco','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'toggle',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-12 18:32:43'),(2009,'SchlafziFe','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-27 10:24:02'),(2010,'Sideb_Aus','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-14 12:20:35'),(2011,'Sideb_An','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-14 12:20:28'),(2012,'Sideb_OR_Aus','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'auto',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Sideb_OR\':\'0\'}','[\'Autobeleuchtung\']','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-25 13:19:44'),(2013,'Sideb_OR_An','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'man\',\'Hell\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Sideb_OR\':\'1\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-25 13:19:22'),(2016,'Sideb_OM_Aus','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'auto',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Sideb_OM\':\'0\'}','[\'Autobeleuchtung\']','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-25 16:45:51'),(2017,'Sideb_OM_An','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'man\',\'Hell\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Sideb_OM\':\'1\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-25 16:45:47'),(2020,'Sideb_OL_Aus','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'auto',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Sideb_OL\':\'0\'}','[\'Autobeleuchtung\']','0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 17:34:25'),(2021,'Sideb_OL_An','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[\'man\',\'Hell\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Sideb_OL\':\'1\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 17:34:24'),(2031,'Sideb_OL_An_1a','0',NULL,'Sideb_OL_An_1a','Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'LinksAn1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Sideb_OL\':\'1\'}','Sideb_OL_An_1b','1.5',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-22 22:12:17'),(2032,'Sideb_OL_An_1b','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'LinksAn2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Sideb_OL\':\'1\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-22 22:12:19'),(2050,'SchlafZiPlay','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'Play',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-24 11:31:41'),(2051,'SchlafZiPause','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,'Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-24 11:31:39'),(2052,'BadPlay','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'Play',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-09 06:06:33'),(2053,'BadPause','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,'Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-18 18:49:01'),(2054,'KitPause','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'Pause',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2055,'KitPlay','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,'Play',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-09 06:06:27'),(2100,'Balkon_1','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Balkon_hell',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-25 18:38:49'),(2101,'Balkon_2','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Balkon_dunkel',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-28 19:39:41'),(2150,'Kueche','0','Kueche',NULL,'Lichter',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'-1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 19:45:31'),(2511,'ZDF','0','ZDF',NULL,'TV',0,'[\'KEY_1\',\'KEY_1\',\'KEY_ENTER\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-11 09:52:35'),(2516,'ProSieben','0','ProSieben',NULL,'TV',0,'[\'KEY_1\',\'KEY_6\',\'KEY_ENTER\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 18:12:11'),(2560,'Arte','0','Arte',NULL,'TV',0,'[\'KEY_6\',\'KEY_0\',\'KEY_ENTER\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-11 09:51:49'),(3000,'Feueralarm','3.3','Feueralarm','Feueralarm','ToSort',0,NULL,NULL,'[\'VolDurchsage\',\'Durchsage\']','[\'VolDurchsage\',\'Durchsage\']','[\'VolDurchsage\',\'Durchsage\']','[\'VolDurchsage\',\'Durchsage\']','100','Hell','Hell','Hell',NULL,'Hell',NULL,NULL,NULL,'100',NULL,'100',NULL,NULL,NULL,'100','100','100','Hell','Hell','Hell','100','Hell',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-20 09:58:08'),(4001,'WeckerN1','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerN2','20',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4002,'WeckerN2','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerN3','300',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4003,'WeckerN3','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'WeckerN4','600',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4004,'WeckerN4','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wecker4',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4005,'Wetter','0',NULL,NULL,'ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Wetter',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Status\':[\'Wecken\',\'Wach\']}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-25 07:29:07'),(4010,'Pflanzen_ein','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'100',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 07:00:00'),(4011,'Pflanzen_aus','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 19:00:00'),(5000,'Schlafzi_fenster_auf','2','Fenster im Schlafzimmer oeffnen','Fenster im Schlafzimmer oeffnen','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_Schlafzi_T_Balkon\':\'less\'}',NULL,NULL,'{\'T_Schlafzi_T_Balkon\':\'greater\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-14 15:55:12'),(5001,'Schlafzi_fenster_zu','2','Fenster im Schlafzimmer schliessen','Fenster im Schlafzimmer schliessen','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_Schlafzi_T_Balkon\':\'greater\'}',NULL,NULL,'{\'T_Schlafzi_T_Balkon\':\'less\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-14 15:42:08'),(5002,'Wohnzi_fenster_auf','2','Fenster im Wohnzimmer oeffnen','Fenster im Wohnzimmer oeffnen','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_Wohnzi_T_Balkon\':\'less\'}',NULL,NULL,'{\'T_Wohnzi_T_Balkon\':\'greater\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-13 16:58:17'),(5003,'Wohnzi_fenster_zu','2','Fenster im Wohnzimmer schliessen','Fenster im Wohnzimmer schliessen','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_Wohnzi_T_Balkon\':\'greater\'}',NULL,NULL,'{\'T_Wohnzi_T_Balkon\':\'less\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-13 16:01:07'),(5004,'Schlafzi_normal','-1','T Schlafzimmer normalisiert','T Schlafzimmer normalisiert','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_SchlafZi\':\'normal\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 21:18:49'),(5005,'Schlafzi_lueften','2','Schlafzimmer warm, lueften.','Schlafzimmer warm, lueften.','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_SchlafZi\':\'warm\'}',NULL,NULL,'{\'T_SchlafZi\':\'normal\',\'TempSteuerung\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-09-14 15:55:12'),(5006,'Schlafzi_kalt','2','Schlafzimmer kalt, Fenster schliessen.','Schlafzimmer kalt, Fenster schliessen.','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_SchlafZi\':\'kalt\'}',NULL,NULL,'{\'T_SchlafZi\':\'normal\',\'TempSteuerung\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-19 21:15:47'),(5007,'Wohnzi_normal','-1','T Wohnzimmer normalisiert','T Wohnzimmer normalisiert','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_WohnZi\':\'normal\'}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 21:18:52'),(5008,'Wohnzi_lueften','2','Wohnzimmer warm, lueften.','Wohnzimmer warm, lueften.','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_WohnZi\':\'warm\'}',NULL,NULL,'{\'T_WohnZi\':\'normal\',\'TempSteuerung\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-18 19:50:51'),(5009,'Wohnzi_kalt','2','Wohnzimmer kalt, Fenster schliessen.','Wohnzimmer kalt, Fenster schliessen.','ToSort',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'T_WohnZi\':\'kalt\'}',NULL,NULL,'{\'T_WohnZi\':\'normal\',\'TempSteuerung\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-07 22:08:25'),(5010,'Frostalarm','2','Aussentemp unter 3, Frostalarm.',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Frostalarm\':\'Aus\'}',NULL,NULL,'{\'Frostalarm\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-15 20:09:58'),(5050,'Heizung_eins','2','Heizung einschalten',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Heizung_eins\':\'Aus\'}',NULL,NULL,'{\'Heizung_eins\':\'Ein\',\'Balkontuer\':\'0.0\',\'Kuechentuer\':\'0.0\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 05:58:25'),(5051,'Heizung_auss','2','Heizung ausschalten',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\'Heizung_auss\':\'Aus\'}',NULL,NULL,'{\'Heizung_auss\':\'Ein\'}',NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-18 13:23:54'),(6000,'FalscherSchluessel','0',NULL,NULL,'Tuer',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Rot',NULL,NULL,'LedsAus','5',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-07 14:13:42'),(6001,'LedsAus','0',NULL,NULL,'Tuer',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AlleAus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-18 21:10:56'),(8001,'close_fw_tv','0','Schliesse Firewall TV',NULL,'Net',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'firew_TV_close','2015-10-01 15:08:36'),(8002,'op_fw_tv','0','Oeffne Firewall TV',NULL,'Net',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'firew_TV_open','2015-11-20 20:00:23'),(9000,'Test','0','Test',NULL,'Intern',500,NULL,NULL,NULL,NULL,'[\'Time\']',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-30 06:26:42'),(9001,'Test2','0','Test2',NULL,'Intern',0,NULL,'leiser',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'AlleAus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-23 16:03:54'),(9003,'Restart_Homecontrol','0','Restart Homecontrol Service',NULL,'Intern',550,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'restart_homecontrol','2015-11-16 18:50:28'),(9004,'Wecker1Test','0','Wecker Test 1',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 05:24:00'),(9005,'Wecker2Test','0','Wecker Test 2',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-01 09:49:00'),(9007,'Sonnenaufgang','0','Sonnenaufgang',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-19 08:29:00'),(9008,'Sonnenuntergang','0','Sonnenuntergang',NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-11-20 17:47:00'),(9010,'Hue_Test','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Aus','Aus','Aus',NULL,NULL,NULL,NULL,NULL,NULL,'Aus',NULL,'Aus','Aus','Aus',NULL,NULL,NULL,NULL,'Aus','Aus',NULL,'Aus',NULL,'Aus',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-25 09:19:18'),(9012,'Halloween_Balkon','0',NULL,NULL,'Intern',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Halloween',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2015-10-31 18:49:56');
/*!40000 ALTER TABLE `Szenen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TuerSPiLED`
--

DROP TABLE IF EXISTS `TuerSPiLED`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TuerSPiLED` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Rot` varchar(45) DEFAULT NULL,
  `Gelb` varchar(45) DEFAULT NULL,
  `Gruen` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Id_UNIQUE` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TuerSPiLED`
--

LOCK TABLES `TuerSPiLED` WRITE;
/*!40000 ALTER TABLE `TuerSPiLED` DISABLE KEYS */;
INSERT INTO `TuerSPiLED` VALUES (1,'AllesEin','An','An','An'),(2,'AlleAus','Aus','Aus','Aus'),(3,'Gruen','Aus','Aus','An'),(4,'Rot','F2','Aus','Aus'),(5,'Alarmanlage_weg','F3','Aus','Aus'),(6,'Alarmanlage_nachts','F3','F3','Aus'),(7,'Wach','Aus','Aus','F4'),(8,'AmGehen','Aus','F2','Aus'),(9,'Gegangen','Aus','F1','Aus'),(10,'Einer_aufgestanden','Aus','F3','Aus'),(11,'einer_gegangen','Aus','F1','Aus'),(12,'Alarmanlage_cntdwn','F1',NULL,'Aus');
/*!40000 ALTER TABLE `TuerSPiLED` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Wecker`
--

DROP TABLE IF EXISTS `Wecker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Wecker` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) DEFAULT NULL,
  `Enabled` tinyint(1) DEFAULT NULL,
  `Mo` tinyint(1) DEFAULT NULL,
  `Tu` tinyint(1) DEFAULT NULL,
  `Wed` tinyint(1) DEFAULT NULL,
  `Th` tinyint(1) DEFAULT NULL,
  `Fr` tinyint(1) DEFAULT NULL,
  `Sa` tinyint(1) DEFAULT NULL,
  `Su` tinyint(1) DEFAULT NULL,
  `Hour` tinyint(4) DEFAULT NULL,
  `Min` tinyint(4) DEFAULT NULL,
  `Licht` tinyint(1) DEFAULT NULL,
  `Audio` tinyint(1) DEFAULT NULL,
  `Permanent` tinyint(4) DEFAULT NULL,
  `Bedingung` tinyint(4) DEFAULT NULL,
  `Szene` varchar(45) DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Offset` time DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Wecker`
--

LOCK TABLES `Wecker` WRITE;
/*!40000 ALTER TABLE `Wecker` DISABLE KEYS */;
INSERT INTO `Wecker` VALUES (1,'Wochentags1',1,0,1,1,1,1,0,0,6,20,1,1,1,NULL,'Wecker1Test','06:20:00','00:11:00'),(2,'Wochentags2',1,1,0,0,0,0,0,0,7,0,1,1,1,NULL,'Wecker1Test','07:00:00','00:11:00'),(3,'Wochentags3',0,0,0,0,0,0,0,0,8,0,1,1,1,NULL,'Wecker1Test','08:00:00','00:11:00'),(4,'Samstags',1,0,0,0,0,0,1,0,6,15,1,1,1,NULL,'Wecker1Test','06:15:00','00:11:00'),(5,'Sonntags',0,0,0,0,0,0,0,1,10,0,1,0,1,NULL,'Wecker2Test','10:00:00','00:11:00');
/*!40000 ALTER TABLE `Wecker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Wohnzimmer_H`
--

DROP TABLE IF EXISTS `Wohnzimmer_H`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Wohnzimmer_H` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` decimal(3,1) DEFAULT NULL,
  `Date` datetime DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Wohnzimmer_H`
--

LOCK TABLES `Wohnzimmer_H` WRITE;
/*!40000 ALTER TABLE `Wohnzimmer_H` DISABLE KEYS */;
/*!40000 ALTER TABLE `Wohnzimmer_H` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Wohnzimmer_T`
--

DROP TABLE IF EXISTS `Wohnzimmer_T`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Wohnzimmer_T` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Value` decimal(3,1) DEFAULT NULL,
  `Steuerwert` decimal(4,3) DEFAULT NULL,
  `Date` datetime DEFAULT NULL,
  `RolAvg` decimal(5,3) DEFAULT NULL,
  `D1` decimal(5,3) DEFAULT NULL,
  `D2` decimal(5,3) DEFAULT NULL,
  `D3` decimal(5,3) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Wohnzimmer_T`
--

LOCK TABLES `Wohnzimmer_T` WRITE;
/*!40000 ALTER TABLE `Wohnzimmer_T` DISABLE KEYS */;
/*!40000 ALTER TABLE `Wohnzimmer_T` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alarm_events`
--

DROP TABLE IF EXISTS `alarm_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alarm_events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  `prio` int(11) NOT NULL DEFAULT '0',
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `acknowledged` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarm_events`
--

LOCK TABLES `alarm_events` WRITE;
/*!40000 ALTER TABLE `alarm_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `alarm_events` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cron`
--

LOCK TABLES `cron` WRITE;
/*!40000 ALTER TABLE `cron` DISABLE KEYS */;
INSERT INTO `cron` VALUES (1,'Pflanzen_ein','07:00:00',NULL,1,1,1,1,1,1,1,1,1,NULL,NULL,NULL,NULL),(2,'Pflanzen_aus','19:00:00',NULL,1,1,1,1,1,1,1,1,1,NULL,NULL,NULL,NULL),(3,'Sonnenaufgang','08:32:00',NULL,1,1,1,1,1,1,1,1,1,'rise',NULL,NULL,NULL),(4,'Sonnenuntergang','17:46:00',NULL,1,1,1,1,1,1,1,1,1,'set',NULL,NULL,NULL),(5,'Buero','10:57:00',NULL,1,1,1,1,1,1,1,1,0,NULL,'-30','90','10:00:00');
/*!40000 ALTER TABLE `cron` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gcm_users`
--

DROP TABLE IF EXISTS `gcm_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gcm_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gcm_regid` varchar(255) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `vorname` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `IP` varchar(45) DEFAULT NULL,
  `anwesend` tinyint(4) DEFAULT NULL,
  `sende` tinyint(4) DEFAULT NULL,
  `Schluessel` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gcm_regid_UNIQUE` (`gcm_regid`)
) ENGINE=InnoDB AUTO_INCREMENT=330 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gcm_users`
--

LOCK TABLES `gcm_users` WRITE;
/*!40000 ALTER TABLE `gcm_users` DISABLE KEYS */;
INSERT INTO `gcm_users` VALUES (84,'APA91bH4VyIfcGNndKzfu7AHwM5vdKO9awxnnrNIFPJK3xY5rTq2rHTUzbLzP6pSKqlgCGwrqVrjaS7ado7Y4pKgvYrRRAGRWKgeyKO0Z7QeYhh42wLoUwtUO_M9ls_eoTQBx-YYLphe3CM6S-6zryrZbzGY90Trlw','3e813a88e8ae377a','tf201','2014-11-03 19:08:36',NULL,5,1,NULL,''),(118,'APA91bGcFLqRzxUMyPev4NqwO3i7-1arkT03p-fB_ifnZ_GFhtyQoyaoHR6uBedY4d-buRWH68WUhXKCnWcarBrQhTtzjGENxU0IoqBJW9tc4nMlXyne_jxtx-27g3phBzE1FuI5xrTM','6dddd195b1ea4c7','Sabina','2015-06-29 11:39:05','192.168.192.22',0,1,NULL,''),(315,'APA91bGBBCI6iLK9HouXy8yR-kn8V0-2dh-f1-EmvoeEqg93_5lEK8G31qptrvkq4pi_EVJ0uvE5krLA3N_4aBGR4Uy-l_dV_S6m8AfjBuSy-zIo6kLdElIMwxeJvfmkkUq-gy8drmeQ','26da615f40462af6','Christoph','2015-10-10 10:41:14',NULL,NULL,NULL,NULL,''),(323,'APA91bEjQYnXU6rPVlYkpB8RobNbAgJ8Do7hV6AnHlPMH5kzGZCZfdKhZrPchPg9LxC4n4aCjLzNkbuvr96tLkJWG7pKmgxlYKj8CIQ0aoy7s3iN3OFrrry1oKPtXk3VUV1J1e5PU4Rw','6dddd195b1ea4c7',NULL,'2015-10-17 03:45:08',NULL,NULL,NULL,NULL,''),(328,'APA91bFZYPUccqA294LEVs0x6zBwO5Q82SElmmQ4PhqiidizjXp1dk4xKTbKaXjCJmhVElLPqqgxOVwtHCHKB7H3p5BpQr1pyOShv8hkyTh1p7aJyCEEW0g1eaDKj95jYp4zbl8Sv0PG','3e813a88e8ae377a',NULL,'2015-10-18 10:30:11',NULL,NULL,NULL,NULL,'');
/*!40000 ALTER TABLE `gcm_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hue_autolicht`
--

DROP TABLE IF EXISTS `hue_autolicht`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hue_autolicht` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `offset` int(11) DEFAULT NULL,
  `min` int(11) DEFAULT NULL,
  `max` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hue_autolicht`
--

LOCK TABLES `hue_autolicht` WRITE;
/*!40000 ALTER TABLE `hue_autolicht` DISABLE KEYS */;
INSERT INTO `hue_autolicht` VALUES (1,'Stehlampe',40,100,160),(2,'Monaco',60,20,160),(3,'Stablampe',80,0,160),(4,'Kueche',70,160,254),(5,'FlurBoden',80,0,160),(6,'Stehlampe_Kino',40,1,1),(7,'Monaco_Kino',60,0,25),(8,'Kueche_Kino',70,50,80),(9,'FlurBoden_Kino',80,0,80),(10,'Stablampe_Kino',80,1,1);
/*!40000 ALTER TABLE `hue_autolicht` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tc_abwesend`
--

DROP TABLE IF EXISTS `tc_abwesend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_abwesend` (
  `idtc_table` int(11) NOT NULL AUTO_INCREMENT,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` int(11) DEFAULT NULL,
  `tc_value_gt` int(11) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(11) DEFAULT NULL,
  `tc_value_eq` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtc_table`),
  UNIQUE KEY `idtc_table` (`idtc_table`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_abwesend`
--

LOCK TABLES `tc_abwesend` WRITE;
/*!40000 ALTER TABLE `tc_abwesend` DISABLE KEYS */;
/*!40000 ALTER TABLE `tc_abwesend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tc_am_gehen`
--

DROP TABLE IF EXISTS `tc_am_gehen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_am_gehen` (
  `idtc_table` int(11) NOT NULL AUTO_INCREMENT,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` int(11) DEFAULT NULL,
  `tc_value_gt` int(11) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(11) DEFAULT NULL,
  `tc_value_eq` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtc_table`),
  UNIQUE KEY `idtc_table` (`idtc_table`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_am_gehen`
--

LOCK TABLES `tc_am_gehen` WRITE;
/*!40000 ALTER TABLE `tc_am_gehen` DISABLE KEYS */;
INSERT INTO `tc_am_gehen` VALUES (1,'Haustuer',NULL,NULL,'Tuer_auf_AG',1,1),(2,'Haustuer',NULL,NULL,'Alles_aus_4',1,0);
/*!40000 ALTER TABLE `tc_am_gehen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tc_einer_wach`
--

DROP TABLE IF EXISTS `tc_einer_wach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_einer_wach` (
  `idtc_table` int(11) NOT NULL,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` int(11) DEFAULT NULL,
  `tc_value_gt` int(11) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(11) DEFAULT NULL,
  `tc_value_eq` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtc_table`),
  UNIQUE KEY `idtc_table` (`idtc_table`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_einer_wach`
--

LOCK TABLES `tc_einer_wach` WRITE;
/*!40000 ALTER TABLE `tc_einer_wach` DISABLE KEYS */;
INSERT INTO `tc_einer_wach` VALUES (1,'Bett_1',NULL,NULL,'Schlafzimmer_aus',1,1);
/*!40000 ALTER TABLE `tc_einer_wach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tc_gegangen`
--

DROP TABLE IF EXISTS `tc_gegangen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_gegangen` (
  `idtc_table` int(11) NOT NULL AUTO_INCREMENT,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` int(11) DEFAULT NULL,
  `tc_value_gt` int(11) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(11) DEFAULT NULL,
  `tc_value_eq` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtc_table`),
  UNIQUE KEY `idtc_table` (`idtc_table`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_gegangen`
--

LOCK TABLES `tc_gegangen` WRITE;
/*!40000 ALTER TABLE `tc_gegangen` DISABLE KEYS */;
INSERT INTO `tc_gegangen` VALUES (1,'Haustuer',NULL,NULL,'was_vergessen',1,1),(2,'Haustuer',NULL,NULL,'Alles_aus_4',1,0);
/*!40000 ALTER TABLE `tc_gegangen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tc_immer`
--

DROP TABLE IF EXISTS `tc_immer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_immer` (
  `idtc_table` int(11) NOT NULL,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` varchar(10) DEFAULT NULL,
  `tc_value_eq` varchar(10) DEFAULT NULL,
  `tc_value_gt` varchar(10) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(1) DEFAULT NULL,
  PRIMARY KEY (`idtc_table`),
  UNIQUE KEY `idtc_table` (`idtc_table`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_immer`
--

LOCK TABLES `tc_immer` WRITE;
/*!40000 ALTER TABLE `tc_immer` DISABLE KEYS */;
INSERT INTO `tc_immer` VALUES (0,'WonziRauchm',NULL,'100',NULL,'Feueralarm',1),(1,'Balkontuer',NULL,'1',NULL,'EinbruchFenster',1),(2,'Haustuer',NULL,'1',NULL,'EinbruchTuer',1),(3,'Kuechentuer',NULL,'1',NULL,'EinbruchFenster',1),(4,'SchlafZiFenster',NULL,'1',NULL,'EinbruchFensterSchlafzi',1),(50,'Temperatur_Balkon','3',NULL,NULL,'Frostalarm',1),(70,'Temperatur_Wohnzi','24.7',NULL,NULL,'Heizung_eins',1),(71,'Temperatur_Wohnzi',NULL,NULL,'25.7','Heizung_auss',1),(121,'Wand_Buero_1',NULL,'100',NULL,'Buero',1);
/*!40000 ALTER TABLE `tc_immer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tc_schlafen`
--

DROP TABLE IF EXISTS `tc_schlafen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_schlafen` (
  `idtc_table` int(11) NOT NULL,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` int(11) DEFAULT NULL,
  `tc_value_eq` int(11) DEFAULT NULL,
  `tc_value_gt` int(11) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(1) DEFAULT NULL,
  PRIMARY KEY (`idtc_table`),
  UNIQUE KEY `idtc_table` (`idtc_table`),
  UNIQUE KEY `idtc_table_UNIQUE` (`idtc_table`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_schlafen`
--

LOCK TABLES `tc_schlafen` WRITE;
/*!40000 ALTER TABLE `tc_schlafen` DISABLE KEYS */;
INSERT INTO `tc_schlafen` VALUES (1,'Beleuchtung_abends',NULL,100,1,'sz_AbendBelEin',1),(2,'Wand_Haupt_1',1,NULL,NULL,'Fern_Haupt_1',1),(3,'Wand_Haupt_1',NULL,100,NULL,'Fern_Haupt_2',1),(10,'Bett_1',NULL,1,NULL,'Schlafzimmer_aus',1),(14,'Bett_1',NULL,2,NULL,'WeckerPhase0a',1),(15,'Bett_1',NULL,3,NULL,'WeckerRomantisch',1),(100,'Haustuer',NULL,1,NULL,'Einbruch_Sofort',1),(101,'balkon_dt',0,NULL,NULL,'Einbruch_Sofort',1);
/*!40000 ALTER TABLE `tc_schlafen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tc_schlafen_gehen`
--

DROP TABLE IF EXISTS `tc_schlafen_gehen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_schlafen_gehen` (
  `idtc_table` int(11) NOT NULL,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` int(11) DEFAULT NULL,
  `tc_value_eq` int(11) DEFAULT NULL,
  `tc_value_gt` int(11) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtc_table`),
  UNIQUE KEY `idtc_table` (`idtc_table`),
  UNIQUE KEY `idtc_table_UNIQUE` (`idtc_table`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_schlafen_gehen`
--

LOCK TABLES `tc_schlafen_gehen` WRITE;
/*!40000 ALTER TABLE `tc_schlafen_gehen` DISABLE KEYS */;
INSERT INTO `tc_schlafen_gehen` VALUES (10,'Bett_1',NULL,1,NULL,'Schlafen3',1),(20,'Bett_1',NULL,3,NULL,'Romantisch',1);
/*!40000 ALTER TABLE `tc_schlafen_gehen` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Table structure for table `tc_status`
--

DROP TABLE IF EXISTS `tc_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_status` (
  `idtc_status` int(11) NOT NULL,
  `tc_value` varchar(45) DEFAULT NULL,
  `tc_table` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtc_status`),
  UNIQUE KEY `tc_status_UNIQUE` (`tc_value`),
  UNIQUE KEY `tc_table_UNIQUE` (`tc_table`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_status`
--

LOCK TABLES `tc_status` WRITE;
/*!40000 ALTER TABLE `tc_status` DISABLE KEYS */;
INSERT INTO `tc_status` VALUES (0,'Wach','tc_wach'),(1,'Schlafen','tc_schlafen'),(2,'Am Schlafen gehen','tc_schlafen_gehen'),(3,'Wecken','tc_wecken'),(4,'Schlummern','tc_schlummern'),(5,'einer_wach','tc_einer_wach'),(6,'Urlaub','tc_urlaub'),(7,'Gegangen','tc_gegangen'),(8,'Am Gehen','tc_am_gehen'),(9,'Abwesend','tc_abwesend');
/*!40000 ALTER TABLE `tc_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tc_urlaub`
--

DROP TABLE IF EXISTS `tc_urlaub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_urlaub` (
  `idtc_table` int(11) NOT NULL AUTO_INCREMENT,
  `tc_sensor` varchar(45) DEFAULT NULL,
  `tc_value_lt` int(11) DEFAULT NULL,
  `tc_value_gt` int(11) DEFAULT NULL,
  `tc_szene` varchar(45) DEFAULT NULL,
  `tc_enabled` int(11) DEFAULT NULL,
  `tc_value_eq` int(11) DEFAULT NULL,
  PRIMARY KEY (`idtc_table`),
  UNIQUE KEY `idtc_table` (`idtc_table`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tc_urlaub`
--

LOCK TABLES `tc_urlaub` WRITE;
/*!40000 ALTER TABLE `tc_urlaub` DISABLE KEYS */;
/*!40000 ALTER TABLE `tc_urlaub` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `tc_wach` VALUES (1,'Helligkeit',NULL,NULL,'-1','AutoBeleuchtung',1),(11,'a1',NULL,'0',NULL,'Sideb_Aus',1),(12,'a1',NULL,NULL,'0','Sideb_An',1),(13,'a2',NULL,'0',NULL,'Sideb_OR_Aus',1),(14,'a2',NULL,NULL,'0','Sideb_OR_An',1),(15,'a4',NULL,'0',NULL,'Sideb_Aus',1),(16,'a4',NULL,NULL,'0','Sideb_An',1),(17,'a8',NULL,'0',NULL,'Sideb_OM_Aus',1),(18,'a8',NULL,NULL,'0','Sideb_OM_An',1),(19,'a16',NULL,'0',NULL,'Sideb_Aus',1),(20,'a16',NULL,NULL,'0','Sideb_An',1),(21,'a32',NULL,'0',NULL,'Sideb_OL_Aus',1),(22,'a32',NULL,NULL,'0','Sideb_OL_An',1),(25,'Wand_Wohnzi_1',NULL,'100',NULL,'Kueche',1),(26,'Wand_Wohnzi_3',NULL,'100',NULL,'LightstripKueche_2',1),(27,'Wand_Wohnzi_3',NULL,'0',NULL,'LightstripKueche_aus',1),(30,'Wand_Haupt_3',NULL,'100',NULL,'DRS3',1),(80,'Wand_Wohnzi_5',NULL,'0',NULL,'Balkonlampe',1),(101,'Wand_Wohnzi_5',NULL,'100',NULL,'Sonos_Kueche_TV',1),(120,'Wand_Buero_1',NULL,'0',NULL,'Buero_hell',1),(121,'Wand_Buero_1',NULL,'100',NULL,'Buero',1),(130,'Wand_Buero_2',NULL,'0',NULL,'Buero_romantisch',1),(131,'Wand_Buero_2',NULL,'100',NULL,'Buero',1),(151,'Wand_Flur_5',NULL,'100',NULL,'SchlafZi_alles_an',1),(171,'Wand_Flur_7',NULL,'100',NULL,'SchlafZi_alles_aus',1),(191,'Wand_Flur_9',NULL,'0',NULL,'Einer_schlafengegangen',1),(192,'Wand_Flur_9',NULL,'100',NULL,'Wetter',1),(200,'balkon_dt',NULL,'1',NULL,'Monaco',0),(201,'balkon_dt',NULL,'-1',NULL,'Monaco',0),(400,'Bett_1',NULL,'1',NULL,'Schlafzimmer_aus',1),(401,'Bett_1',NULL,'3',NULL,'Romantisch',1),(402,'Bett_1',NULL,'2',NULL,'SchlafZi_alles_an',1),(500,'Temperatur_Balkon','Temperatur_Schlafzi',NULL,NULL,'Schlafzi_fenster_auf',1),(501,'Temperatur_Balkon',NULL,NULL,'Temperatur_Schlafzi','Schlafzi_fenster_zu',1),(502,'Temperatur_Balkon','Temperatur_Wohnzi',NULL,NULL,'Wohnzi_fenster_auf',1),(503,'Temperatur_Balkon',NULL,NULL,'Temperatur_Wohnzi','Wohnzi_fenster_zu',1),(504,'Temperatur_Schlafzi','23.5',NULL,NULL,'Schlafzi_kalt',1),(505,'Temperatur_Schlafzi','26',NULL,'24','Schlafzi_normal',1),(506,'Temperatur_Schlafzi',NULL,NULL,'26','Schlafzi_lueften',1),(507,'Temperatur_Wohnzi','24',NULL,NULL,'Wohnzi_kalt',1),(508,'Temperatur_Wohnzi','26',NULL,'24','Wohnzi_normal',1),(509,'Temperatur_Wohnzi',NULL,NULL,'26','Wohnzi_lueften',1),(600,'Balkontuer',NULL,'1',NULL,'Esszimmer',0),(601,'Balkontuer',NULL,'0',NULL,'Esszimmer',0);
/*!40000 ALTER TABLE `tc_wach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tc_wecken`
--

DROP TABLE IF EXISTS `tc_wecken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tc_wecken` (
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
-- Dumping data for table `tc_wecken`
--

LOCK TABLES `tc_wecken` WRITE;
/*!40000 ALTER TABLE `tc_wecken` DISABLE KEYS */;
INSERT INTO `tc_wecken` VALUES (10,'Bett_1',NULL,1,NULL,'Schlummern15',1),(12,'Bett_1',NULL,2,NULL,'WeckerMute',1),(14,'Bett_1',NULL,3,NULL,'WeckerRomantisch',1);
/*!40000 ALTER TABLE `tc_wecken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-11-21 13:51:08
