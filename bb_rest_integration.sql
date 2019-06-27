-- --------------------------------------------------------
-- Host:                         falstaff.shef.ac.uk
-- Server version:               10.0.36-MariaDB-0ubuntu0.16.04.1 - Ubuntu 16.04
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             9.5.0.5264
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for bb_rest_integration
DROP DATABASE IF EXISTS `bb_rest_integration`;
CREATE DATABASE IF NOT EXISTS `bb_rest_integration` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `bb_rest_integration`;

-- Dumping structure for table bb_rest_integration.error_record
DROP TABLE IF EXISTS `error_record`;
CREATE TABLE IF NOT EXISTS `error_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endpoint` varchar(255) NOT NULL,
  `method` varchar(10) NOT NULL,
  `timestamp` datetime NOT NULL,
  `error_message` varchar(120) NOT NULL,
  `status` int(11) NOT NULL,
  `xml_body` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table bb_rest_integration.transaction_record
DROP TABLE IF EXISTS `transaction_record`;
CREATE TABLE IF NOT EXISTS `transaction_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endpoint` varchar(255) NOT NULL,
  `method` varchar(10) NOT NULL,
  `timestamp` datetime NOT NULL,
  `status` int(11) NOT NULL,
  `xml_body` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
