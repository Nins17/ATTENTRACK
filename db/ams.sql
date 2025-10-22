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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_logs`
--

LOCK TABLES `attendance_logs` WRITE;
/*!40000 ALTER TABLE `attendance_logs` DISABLE KEYS */;
INSERT INTO `attendance_logs` VALUES (5,6,'Grade3SectionBScienceMonday_08_12_25_Attendance.csv','static/attendance_csv/Grade3SectionBScienceMonday_08_12_25_Attendance.csv',1),(7,6,'Grade3SectionBScienceMonday_09_23_25_Attendance.csv','static/attendance_csv/Grade3SectionBScienceMonday_09_23_25_Attendance.csv',1),(8,9,'Grade1SectionAEnglishWednesday_10_23_25_Attendance.csv','static/attendance_csv/Grade1SectionAEnglishWednesday_10_23_25_Attendance.csv',117);
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
  PRIMARY KEY (`schedule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_schedules`
--

LOCK TABLES `class_schedules` WRITE;
/*!40000 ALTER TABLE `class_schedules` DISABLE KEYS */;
INSERT INTO `class_schedules` VALUES (6,'Grade 3','Section B','Science','Monday','09:30','10:30',0,'Janin Anne',1),(8,'Grade 5','Section A','English','Thursday','07:30','09:00',0,'alup, Ninn Jan ',2),(9,'Grade 1','Section A','English','Wednesday','13:00','14:00',1,'Silvias, Janin Pula ',117);
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
INSERT INTO `student_info` VALUES (4,'static/known_faces/04-2122-2222.jpg','Armond','D.','Sinalsal','','21','Si mama mo','09123456789','Grade 3',''),(112113,'static/known_faces/112113.jpg','Janin','Pula','Silvias','','5','mama','0909876578','Grade 1',''),(112114,'static/known_faces/112114.jpg','dump','Pula','Silvias','','5','mam','0909876578','Grade 3',''),(1234567,'static/known_faces/1234567.jpg','rhaiza','baldoza','barzo','','21','maerts','0909875678','Grade 5','');
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
  PRIMARY KEY (`enrollment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_schedule_enrollments`
--

LOCK TABLES `student_schedule_enrollments` WRITE;
/*!40000 ALTER TABLE `student_schedule_enrollments` DISABLE KEYS */;
INSERT INTO `student_schedule_enrollments` VALUES (13,112113,9,'Janin Pula Silvias',117);
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
) ENGINE=InnoDB AUTO_INCREMENT=11511235 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_accounts`
--

LOCK TABLES `teacher_accounts` WRITE;
/*!40000 ALTER TABLE `teacher_accounts` DISABLE KEYS */;
INSERT INTO `teacher_accounts` VALUES (1,'static/ADMIN/teacher_profpic/pic1.jpg','test','teacher','one','.jr','12345'),(2,'static/ADMIN/teacher_profpic\\2.png','Ninn','Jan','alup','','Janin@123'),(117,'static/ADMIN/teacher_profpic\\0117.jpg','Janin','Pula','Silvias','','Janin@117');
/*!40000 ALTER TABLE `teacher_accounts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-23  7:16:47
