-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: dbhotelapp
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bill`
--

DROP TABLE IF EXISTS `bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_of_payment` int(11) NOT NULL,
  `total_value` int(11) NOT NULL,
  `into_money` int(11) NOT NULL,
  `rentSlip_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rentSlip_id` (`rentSlip_id`),
  CONSTRAINT `bill_ibfk_1` FOREIGN KEY (`rentSlip_id`) REFERENCES `rentalslip` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill`
--

LOCK TABLES `bill` WRITE;
/*!40000 ALTER TABLE `bill` DISABLE KEYS */;
INSERT INTO `bill` VALUES (1,15,54100000,54100000,1);
/*!40000 ALTER TABLE `bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `change_the_rules`
--

DROP TABLE IF EXISTS `change_the_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `change_the_rules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_change` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `contents` varchar(300) COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `change_the_rules_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `change_the_rules`
--

LOCK TABLES `change_the_rules` WRITE;
/*!40000 ALTER TABLE `change_the_rules` DISABLE KEYS */;
INSERT INTO `change_the_rules` VALUES (1,'Quy định 1','Khách sạn quy định về loại phòng, khách sạn sẽ chỉ gồm có 3 loại phòng: loại A, loại B và loại C . Có thể tùy thiết lập loại giường và dịch vụ cho từng phòng theo chuẩn của loại phòng.. ',1);
/*!40000 ALTER TABLE `change_the_rules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custommer_type`
--

DROP TABLE IF EXISTS `custommer_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `custommer_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_type_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `coefficient` float NOT NULL,
  `note` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custommer_type`
--

LOCK TABLES `custommer_type` WRITE;
/*!40000 ALTER TABLE `custommer_type` DISABLE KEYS */;
INSERT INTO `custommer_type` VALUES (1,'Nội địa',0,'Chỉ áp dụng cho các khách hàng trong nước.'),(2,'Nước ngoài',1.5,'Chỉ áp dụng cho các khách hàng ngoài nước.');
/*!40000 ALTER TABLE `custommer_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kindsofroom`
--

DROP TABLE IF EXISTS `kindsofroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kindsofroom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kor_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `kor_quality` enum('STD','SUP','DLX','SUT') COLLATE utf8_unicode_ci NOT NULL,
  `interior_design_style` enum('ModernAndSimple','ModernAndLuxurious','ClassicAndLuxurious','NewClassical','Classic') COLLATE utf8_unicode_ci DEFAULT NULL,
  `kor_rates` int(11) NOT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kindsofroom`
--

LOCK TABLES `kindsofroom` WRITE;
/*!40000 ALTER TABLE `kindsofroom` DISABLE KEYS */;
INSERT INTO `kindsofroom` VALUES (1,'Loại A','STD','ModernAndSimple',150000,'Phòng loại A là phòng được thiết lập theo chất lượng tiêu chuẩn của khách sạn, kiểu thiết kế theo phong cách hiện đại và tối giản.'),(2,'Loại B','SUP','ModernAndLuxurious',170000,'Phòng loại B là phòng được thiết lập theo chất lượng cao cấp hơn loại A, kiểu thiết kế theo phong cách hiện đại và sang trọng.'),(3,'Loại C','DLX','ClassicAndLuxurious',200000,'Phòng loại C là phòng được thiết lập theo chất lượng cao cấp hơn cả loại A và loại B, kiểu thiết kế theo phong cách cổ điển và sang trọng.');
/*!40000 ALTER TABLE `kindsofroom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rentalslip`
--

DROP TABLE IF EXISTS `rentalslip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rentalslip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `hire_start_date` datetime NOT NULL,
  `room_id` int(11) NOT NULL,
  `surcharge_id` int(11) NOT NULL,
  `customer_type_id` int(11) NOT NULL,
  `identity_card` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  KEY `surcharge_id` (`surcharge_id`),
  KEY `customer_type_id` (`customer_type_id`),
  CONSTRAINT `rentalslip_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`),
  CONSTRAINT `rentalslip_ibfk_2` FOREIGN KEY (`surcharge_id`) REFERENCES `surcharqe` (`id`),
  CONSTRAINT `rentalslip_ibfk_3` FOREIGN KEY (`customer_type_id`) REFERENCES `custommer_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rentalslip`
--

LOCK TABLES `rentalslip` WRITE;
/*!40000 ALTER TABLE `rentalslip` DISABLE KEYS */;
INSERT INTO `rentalslip` VALUES (1,'Trần Văn A','2020-12-01 06:38:00',1,1,1,'18510000001','1/1, phường 1, quận 1, thành phố Hồ Chí Minh');
/*!40000 ALTER TABLE `rentalslip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `kinds_of_room_id` int(11) NOT NULL,
  `type_of_bed_id` int(11) NOT NULL,
  `services_id` int(11) NOT NULL,
  `img_kor` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `img_tob` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `room_status` enum('isVacant','isOccupied') COLLATE utf8_unicode_ci DEFAULT NULL,
  `room_amount` int(11) NOT NULL,
  `notes` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `kinds_of_room_id` (`kinds_of_room_id`),
  KEY `type_of_bed_id` (`type_of_bed_id`),
  KEY `services_id` (`services_id`),
  CONSTRAINT `room_ibfk_1` FOREIGN KEY (`kinds_of_room_id`) REFERENCES `kindsofroom` (`id`),
  CONSTRAINT `room_ibfk_2` FOREIGN KEY (`type_of_bed_id`) REFERENCES `typeofbed` (`id`),
  CONSTRAINT `room_ibfk_3` FOREIGN KEY (`services_id`) REFERENCES `services` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (1,'DU01',1,1,1,'#img','#img','isVacant',3,'3 người lớn kèm 2 trẻ em (nếu có).'),(2,'DU02',1,2,1,'#img','#img','isVacant',3,'3 người lớn kèm 2 trẻ em (nếu có).'),(3,'DU03',1,3,1,'#img','#img','isVacant',3,'3 người lớn kèm 2 trẻ em (nếu có).'),(4,'DU04',1,4,1,'#img','#img','isVacant',3,'3 người lớn kèm 2 trẻ em (nếu có).'),(5,'DU05',1,1,2,'#img','#img','isVacant',3,'3 người lớn kèm 2 trẻ em (nếu có).'),(6,'DU06',1,1,2,'#img','#img','isVacant',3,'3 người lớn kèm 2 trẻ em (nếu có).'),(7,'DU07',1,1,3,'#img','#img','isVacant',3,'3 người lớn kèm 2 trẻ em (nếu có).'),(8,'DU08',1,1,2,'#img','#img','isVacant',3,'3 người lớn kèm 2 trẻ em (nếu có).'),(9,'DU09',1,2,3,'#img','#img','isVacant',3,'3 người lớn kèm 2 trẻ em (nếu có).'),(10,'DU10',2,1,1,'#img','#img','isVacant',4,'3 người lớn kèm 2 trẻ em (nếu có).'),(11,'DU11',2,1,2,'#img','#img','isVacant',4,'3 người lớn kèm 2 trẻ em (nếu có).'),(12,'DU12',2,1,3,'#img','#img','isVacant',4,'3 người lớn kèm 2 trẻ em (nếu có).'),(13,'DU13',2,2,1,'#img','#img','isVacant',4,'3 người lớn kèm 2 trẻ em (nếu có).'),(14,'DU14',2,4,3,'#img','#img','isVacant',4,'3 người lớn kèm 2 trẻ em (nếu có).'),(15,'DU15',3,1,1,'#img','#img','isVacant',5,'5 người lớn kèm 3 trẻ em (nếu có).'),(16,'DU16',3,3,2,'#img','#img','isVacant',5,'5 người lớn kèm 3 trẻ em (nếu có).'),(17,'DU17',3,2,2,'#img','#img','isVacant',5,'5 người lớn kèm 3 trẻ em (nếu có).'),(18,'DU18',3,4,3,'#img','#img','isVacant',5,'5 người lớn kèm 3 trẻ em (nếu có).'),(19,'DU19',3,1,3,'#img','#img','isVacant',5,'5 người lớn kèm 3 trẻ em (nếu có).'),(20,'DU20',3,2,3,'#img','#img','isVacant',5,'5 người lớn kèm 3 trẻ em (nếu có).');
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ser_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `ser_rates` int(11) NOT NULL,
  `description` varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'DV01',50000,'Dịch vụ ăn uống , hồ bơi, xe thuê, mạng internet riêng tư'),(2,'DV02',60000,'Dịch vụ ăn uống , hồ bơi, xe thuê, mạng internet riêng tư, tham dự tiệc và buổi dieenrr đặt biệt có ở khách sạn.'),(3,'DV03',70000,'Dịch vụ ăn uống , hồ bơi, xe thuê, mạng internet riêng tư, spa , tham dự tiệc nhà hàng với các đầu bếp tài năng ');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surcharqe`
--

DROP TABLE IF EXISTS `surcharqe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `surcharqe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `surcharge_rate` int(11) NOT NULL,
  `surcharge_amount` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surcharqe`
--

LOCK TABLES `surcharqe` WRITE;
/*!40000 ALTER TABLE `surcharqe` DISABLE KEYS */;
INSERT INTO `surcharqe` VALUES (1,0,1),(2,0,2),(3,25,3);
/*!40000 ALTER TABLE `surcharqe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `typeofbed`
--

DROP TABLE IF EXISTS `typeofbed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `typeofbed` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tob_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `tob_quality` enum('SGL','TWN','DBL','TRPL') COLLATE utf8_unicode_ci NOT NULL,
  `import_from_country` enum('England','France','Italian','Germany') COLLATE utf8_unicode_ci DEFAULT NULL,
  `tob_rates` int(11) NOT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typeofbed`
--

LOCK TABLES `typeofbed` WRITE;
/*!40000 ALTER TABLE `typeofbed` DISABLE KEYS */;
INSERT INTO `typeofbed` VALUES (1,'BED01','SGL','Germany',50000,'Loại giường được thiết kế, thiết lập theo chuẩn thiết kế của loại phòng hiện đại và tối giản. Do các nhà kỹ nghệ của Đức làm nên. '),(2,'BED02','TWN','Italian',60000,'Loại giường được thiết kế, thiết lập theo chuẩn thiết kế của loại phòng hiện đại và sang trọng. Do các nhà kỹ nghệ của Ý làm nên. '),(3,'BED03','DBL','France',70000,'Loại giường được thiết kế, thiết lập theo chuẩn thiết kế của loại phòng hiện đại và sang trọng. Do các nhà kỹ nghệ của Pháp làm nên. '),(4,'BED04','TRPL','England',80000,'Loại giường được thiết kế, thiết lập theo chuẩn thiết kế của loại phòng cổ điển và sang trọng. Do các nhà kỹ nghệ của Anh Quốc làm nên. ');
/*!40000 ALTER TABLE `typeofbed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `user_active` tinyint(1) DEFAULT NULL,
  `user_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `user_password` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `user_roles` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_chk_1` CHECK ((`user_active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Trần Thùy Dung',1,'DungIT','b2c3b75b24f611bde67921d19c8dffcd','Admin-(Quản trị viên)'),(2,'Phan Thị Thu Uyên',1,'UyenIT','ca0a908e85ac27b2cd0d2b82b3e374e5','Receptionlist-(Nhân viên tiếp tân)');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-17  3:51:59
