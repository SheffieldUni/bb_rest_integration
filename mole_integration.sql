-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.3.5-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.5.0.5264
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for mole_integration
DROP DATABASE IF EXISTS `mole_integration`;
CREATE DATABASE IF NOT EXISTS `mole_integration` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `mole_integration`;

-- Dumping structure for table mole_integration.error_record
DROP TABLE IF EXISTS `error_record`;
CREATE TABLE IF NOT EXISTS `error_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endpoint` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `error_message` varchar(120) NOT NULL,
  `status` int(11) NOT NULL,
  `xml_body` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table mole_integration.transaction_record
DROP TABLE IF EXISTS `transaction_record`;
CREATE TABLE IF NOT EXISTS `transaction_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endpoint` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `status` int(11) NOT NULL,
  `xml_body` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
