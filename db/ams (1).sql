CREATE DATABASE  IF NOT EXISTS `ams` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ams`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: ams
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `admin_account`
--

DROP TABLE IF EXISTS `admin_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_account` (
  `admin_ID` int NOT NULL,
  `admin_photo` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `admin_fname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `admin_mname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `admin_lname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `admin_password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`admin_ID`),
  UNIQUE KEY `admin_ID` (`admin_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_account`
--

LOCK TABLES `admin_account` WRITE;
/*!40000 ALTER TABLE `admin_account` DISABLE KEYS */;
INSERT INTO `admin_account` VALUES (116111,'-','Admin','Test','TestAdmin','12345678');
/*!40000 ALTER TABLE `admin_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_logs`
--

DROP TABLE IF EXISTS `attendance_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `schedule_id` int NOT NULL,
  `filename` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `csv_path` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `schedule_id` (`schedule_id`),
  CONSTRAINT `attendance_logs_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher_accounts` (`teacher_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `attendance_logs_ibfk_2` FOREIGN KEY (`schedule_id`) REFERENCES `class_schedules` (`schedule_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=298 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_logs`
--

LOCK TABLES `attendance_logs` WRITE;
/*!40000 ALTER TABLE `attendance_logs` DISABLE KEYS */;
INSERT INTO `attendance_logs` VALUES (8,9,'Grade1SectionAEnglishWednesday_10_23_25_Attendance.csv','static/attendance_csv/Grade1SectionAEnglishWednesday_10_23_25_Attendance.csv',193800117),(9,9,'Grade1SectionAEnglishWednesday_10_23_25_Attendance.csv','attendance_csv/Grade1SectionAEnglishWednesday_10_23_25_Attendance.csv',193800117),(10,10,'Grade3Section-AdelfaMathThursday_10_23_25_Attendance.csv','attendance_csv/Grade3Section-AdelfaMathThursday_10_23_25_Attendance.csv',193800117),(11,10,'Grade3Section-AdelfaMathThursday_10_23_25_Attendance.csv','static\\attendance_csv\\Grade3Section-AdelfaMathThursday_10_23_25_Attendance.csv',193800117),(12,10,'Grade3Section-AdelfaMathThursday_10_24_25_Attendance.csv','static\\attendance_csv\\Grade3Section-AdelfaMathThursday_10_24_25_Attendance.csv',193800117),(13,9,'Grade1SectionAEnglishWednesday_10_24_25_Attendance.csv','static\\attendance_csv\\Grade1SectionAEnglishWednesday_10_24_25_Attendance.csv',193800117),(14,9,'Grade1SectionAEnglishWednesday_10_25_25_Attendance.csv','static\\attendance_csv\\Grade1SectionAEnglishWednesday_10_25_25_Attendance.csv',193800117),(15,10,'Grade3Section-AdelfaMathThursday_10_25_25_Attendance.csv','static\\attendance_csv\\Grade3Section-AdelfaMathThursday_10_25_25_Attendance.csv',193800117),(16,10,'Grade3Section-AdelfaMathThursday_10_26_25_Attendance.csv','static\\attendance_csv\\Grade3Section-AdelfaMathThursday_10_26_25_Attendance.csv',193800117),(17,11,'Grade3sectioncenglishMonday_10_26_25_Attendance.csv','static\\attendance_csv\\Grade3sectioncenglishMonday_10_26_25_Attendance.csv',193800117),(18,11,'Grade3sectioncenglishMonday_10_27_25_Attendance.csv','static\\attendance_csv\\Grade3sectioncenglishMonday_10_27_25_Attendance.csv',193800117),(19,10,'Grade3Section-AdelfaMathThursday_10_27_25_Attendance.csv','static\\attendance_csv\\Grade3Section-AdelfaMathThursday_10_27_25_Attendance.csv',193800117),(20,10,'Grade3Section-AdelfaMathThursday_10_28_25_Attendance.csv','static\\attendance_csv\\Grade3Section-AdelfaMathThursday_10_28_25_Attendance.csv',193800117),(21,14,'Grade3Section1MAthTuesday_10_28_25_Attendance.csv','static\\attendance_csv\\Grade3Section1MAthTuesday_10_28_25_Attendance.csv',193800117),(22,10,'Grade3Section-AdelfaMathThursday_10_29_25_Attendance.csv','static\\attendance_csv\\Grade3Section-AdelfaMathThursday_10_29_25_Attendance.csv',193800117),(23,9,'Grade1SectionAEnglishWednesday_10_29_25_Attendance.csv','static\\attendance_csv\\Grade1SectionAEnglishWednesday_10_29_25_Attendance.csv',193800117),(24,11,'Grade3sectioncenglishMonday_11_10_25_Attendance.csv','static\\attendance_csv\\Grade3sectioncenglishMonday_11_10_25_Attendance.csv',193800117),(25,11,'Grade3sectioncenglishMonday_11_17_25_Attendance.csv','static\\attendance_csv\\Grade3sectioncenglishMonday_11_17_25_Attendance.csv',193800117);
/*!40000 ALTER TABLE `attendance_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_schedules`
--

DROP TABLE IF EXISTS `class_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_schedules` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `grade_level` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `section` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `subject` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `schedule` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `start_time` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `end_time` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `number_of_students` int NOT NULL,
  `teacher` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_id` int NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `fk_teacherid_idx` (`teacher_id`),
  CONSTRAINT `fk_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teacher_accounts` (`teacher_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_schedules`
--

LOCK TABLES `class_schedules` WRITE;
/*!40000 ALTER TABLE `class_schedules` DISABLE KEYS */;
INSERT INTO `class_schedules` VALUES (9,'Grade 1','Section A','English','Wednesday','13:00','14:00',1,'Silvias, Janin Pula ',193800117),(10,'Grade 3','Section -Adelfa','Math','Thursday','18:05','19:05',3,'Silvias, Janin Pula ',193800117),(11,'Grade 3','section c','english','Monday','22:23','00:23',1,'Silvias, Janin Pula ',193800117),(14,'Grade 3','Section 1','MAth','Tuesday','10:04','11:04',1,'Silvias, Janin Pula ',193800117);
/*!40000 ALTER TABLE `class_schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_info`
--

DROP TABLE IF EXISTS `student_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_info` (
  `student_id` int NOT NULL,
  `student_image_path` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `student_first_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `student_middle_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `student_last_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `student_suffix` varchar(255) COLLATE utf8mb4_general_ci DEFAULT '-',
  `student_age` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `student_guardian` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `guardian_contact` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `current_grade_level` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `section` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_info`
--

LOCK TABLES `student_info` WRITE;
/*!40000 ALTER TABLE `student_info` DISABLE KEYS */;
INSERT INTO `student_info` VALUES (112332,'static/known_faces/112332/1.jpg','Janaele','Angel','Silvias','','6','Si mama na','09457001103','Grade 1','Section A'),(1133225,'static/known_faces/1133225/1.jpg','Juswani','Walana','Iba','','10','Si mama mo','0909198979','Grade 3','Section -Adelfa'),(123455678,'static/known_faces/123455678/1.jpg','Ren','Joseph','lumogdang5','','5','guardian','09190028340','Grade 3','Section -Adelfa'),(123456789,'static/known_faces/123456789/1.jpg','Janin','Pula','Silvias','','8','Si mama mo','09171449691','Grade 3','Section B');
/*!40000 ALTER TABLE `student_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_schedule_enrollments`
--

DROP TABLE IF EXISTS `student_schedule_enrollments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_schedule_enrollments` (
  `enrollment_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `schedule_id` int NOT NULL,
  `student_name` varchar(255) NOT NULL,
  `teacher_id` int DEFAULT '0',
  PRIMARY KEY (`enrollment_id`),
  KEY `_idx` (`student_id`),
  CONSTRAINT `fk_student_enrollment` FOREIGN KEY (`student_id`) REFERENCES `student_info` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_schedule_enrollments`
--

LOCK TABLES `student_schedule_enrollments` WRITE;
/*!40000 ALTER TABLE `student_schedule_enrollments` DISABLE KEYS */;
INSERT INTO `student_schedule_enrollments` VALUES (18,123456789,6,'Janin Pula Silvias',1),(19,123456789,10,'Janin Pula Silvias',117),(21,112332,9,'Janaele Angel Silvias',117),(22,1133225,10,'Juswani Walana Iba',117),(23,123456789,11,'Janin Pula Silvias',117),(24,123455678,10,'Ren Joseph lumogdang5',193800117),(25,123455678,14,'Ren Joseph lumogdang5',193800117);
/*!40000 ALTER TABLE `student_schedule_enrollments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_accounts`
--

DROP TABLE IF EXISTS `teacher_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher_accounts` (
  `teacher_ID` int NOT NULL AUTO_INCREMENT,
  `teacher_profile` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_fname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_mname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_lname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_suffix` varchar(4) COLLATE utf8mb4_general_ci NOT NULL,
  `teacher_password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`teacher_ID`),
  UNIQUE KEY `teacher_ID` (`teacher_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1938001178 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_accounts`
--

LOCK TABLES `teacher_accounts` WRITE;
/*!40000 ALTER TABLE `teacher_accounts` DISABLE KEYS */;
INSERT INTO `teacher_accounts` VALUES (193800117,'static/ADMIN/teacher_profpic/193800117.jpg','Janin','Pula','Silvias','','Janin@117'),(1234567899,'static/ADMIN/teacher_profpic\\1234567899.jpg','test','teach','teacher','','1234567899');
/*!40000 ALTER TABLE `teacher_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_in_out_record_paths`
--

DROP TABLE IF EXISTS `time_in_out_record_paths`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `time_in_out_record_paths` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `csv_path` varchar(255) DEFAULT NULL,
  `date` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_in_out_record_paths`
--

LOCK TABLES `time_in_out_record_paths` WRITE;
/*!40000 ALTER TABLE `time_in_out_record_paths` DISABLE KEYS */;
INSERT INTO `time_in_out_record_paths` VALUES (1,'static/time_in_out__csv/TimeIN_OUT(11_19_25)_Record.csv','2025-11-19 18:49:45.609469'),(2,'static/time_in_out__csv/TimeIN_OUT(11_19_25)_Record.csv','11_19_25');
/*!40000 ALTER TABLE `time_in_out_record_paths` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-20 13:34:06
