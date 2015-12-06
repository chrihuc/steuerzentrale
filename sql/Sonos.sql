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
INSERT INTO `Sonos` VALUES ('Bad','RINCON_000E5830220001400',0,'',0,0,'','34',25),('Chris','Own',0,NULL,0,1,'0:00:00','44',NULL),('ChrisAktuell','Own',0,'x-file-cifs://SERVER/Musik/Neuer%20Ordner/Podcasts/rj_russisch_lektion_036.mp3',0,36,'0:02:53','51',35),('DRS3','Own',0,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,NULL,NULL,NULL,NULL),('Duschen','Own',0,NULL,0,1,'0:00:00','43',40),('InputWohnZi','Own',0,'x-rincon-stream:RINCON_000E58232A2601400',1,NULL,NULL,NULL,NULL),('Klingelton','Own',0,NULL,0,1,'0:00:00','45',NULL),('Kueche','Own',1,'',1,0,'0:00:00','40',20),('MasterBad','RINCON_000E583138BA01400',0,NULL,NULL,NULL,NULL,NULL,NULL),('MasterSchlafZi','RINCON_000E5830220001400',0,NULL,NULL,NULL,NULL,NULL,20),('MasterSchlafZiWecken','RINCON_000E5830220001400',0,NULL,NULL,NULL,NULL,NULL,12),('MasterWohnZi','RINCON_000E58232A2601400',0,NULL,NULL,NULL,NULL,NULL,NULL),('Nachrichtenton','Own',0,NULL,0,1,'0:00:00','46',NULL),('Romantisch','Own',0,'x-rincon-mp3radio://pub5.radiotunes.com:80/radiotunes_mellowsmoothjazz',1,0,'0:00:00',NULL,10),('SabinaBeeil','Own',0,'x-rincon-mp3radio://translate.google.com/translate_tts?tl=de&amp;q=es+sind+noch+10+minuten',1,0,'0:00:00',NULL,30),('Schlafen','Own',0,'aac://stream.srg-ssr.ch/m/rsp/aacp_96',1,NULL,NULL,NULL,20),('SchlafZi','Own',1,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,1,'0:00:00','35',12),('Stumm',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0),('Swisspop','Own',0,'aac://stream.srg-ssr.ch/m/rsp/aacp_96',1,1,'0:00:00',NULL,NULL),('TextToSonos','Own',0,NULL,0,1,'0:00:00','47',NULL),('unStumm',NULL,NULL,NULL,NULL,NULL,NULL,NULL,20),('VolDurchsage',NULL,NULL,NULL,NULL,NULL,NULL,NULL,35),('VolMorgens',NULL,NULL,NULL,NULL,NULL,NULL,NULL,10),('VolMorgensBad',NULL,NULL,NULL,NULL,NULL,NULL,NULL,25),('VolMorgensKu',NULL,NULL,NULL,NULL,NULL,NULL,NULL,20),('VolWohnzi',NULL,NULL,NULL,NULL,NULL,NULL,NULL,80),('Wecker1','Own',0,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,1,'0:00:00','41',5),('Wecker2','Own',0,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,1,'0:00:00','42',NULL),('WeckerAlternative','Own',0,NULL,0,0,'0:00:00','44',NULL),('WeckerPhase0','Own',0,'aac://stream.srg-ssr.ch/m/rsp/aacp_96',1,0,'0:00:00',NULL,5),('WeckerPhase0a','Own',0,'aac://stream.srg-ssr.ch/m/rsp/aacp_96',1,0,'0:00:00',NULL,0),('WeckerPhase1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,6),('WeckerPhase2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,7),('WeckerPhase3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,8),('WeckerPhase4','Own',0,'aac://stream.srg-ssr.ch/m/drs3/aacp_96',1,0,'0:00:00',NULL,12),('WeckerRomantisch','Own',0,'x-rincon-mp3radio://pub5.radiotunes.com:80/radiotunes_mellowsmoothjazz',1,0,'0:00:00',NULL,6),('Weihnachten','Own',0,'x-rincon-mp3radio://pub6.radiotunes.com:80/radiotunes_christmas',1,1,'0:00:00',NULL,21),('WohnZi','RINCON_000E58232A2601400',0,'',0,0,'','33',80);
/*!40000 ALTER TABLE `Sonos` ENABLE KEYS */;
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
