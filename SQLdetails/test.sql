-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 09, 2021 at 09:36 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `bank`
--

CREATE TABLE `bank` (
  `AccountNumber` varchar(20) NOT NULL,
  `Name` text NOT NULL,
  `Type` text NOT NULL,
  `Balance` double(50,2) DEFAULT NULL,
  `lastt` datetime DEFAULT NULL,
  `CIF` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bank`
--

INSERT INTO `bank` (`AccountNumber`, `Name`, `Type`, `Balance`, `lastt`, `CIF`) VALUES
('00000000006', 'GANESH T S', 'Savings', 6233.38, '2021-05-10 00:45:42', '98765432006'),
('00000000011', 'MANAS KUMAR MISHRA', 'Savings', 9977718.08, '2021-05-10 00:42:13', '98765432011'),
('00000000026', 'KARTHIKA RAJESH', 'Savings', 9997.80, '2021-05-09 14:46:16', '98765432026');

-- --------------------------------------------------------

--
-- Table structure for table `bank2`
--

CREATE TABLE `bank2` (
  `AccountNumber` varchar(20) NOT NULL,
  `Name` text NOT NULL,
  `Type` text NOT NULL,
  `Balance` double(50,2) DEFAULT NULL,
  `lastt` datetime DEFAULT NULL,
  `CIF` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bank2`
--

INSERT INTO `bank2` (`AccountNumber`, `Name`, `Type`, `Balance`, `lastt`, `CIF`) VALUES
('90000000000001', 'Income Tax Authority', 'Current', 17411.00, '2021-05-10 00:42:13', '98765431000'),
('90000000000002', 'Amazon', 'Current', 200.00, '2021-05-04 14:05:53', '98765431001'),
('90000000000003', 'Zomato', 'Current', 600.00, '2021-05-04 13:29:30', '98765431002'),
('90000000000004', 'Internshala', 'Current', 100.00, NULL, '98765431003'),
('90000000000005', 'MakeMyTrip', 'Current', 1334.00, '2021-05-10 00:45:42', '98765431004'),
('90000000000006', 'Practo', 'Current', 1334.00, '2021-05-09 16:54:58', '98765431005'),
('90000000000007', 'MKMISHRA', 'Current', 200.01, '2021-05-04 14:01:37', '98765431006'),
('90000000000008', 'OlaCabs', 'Current', 300.00, '2021-05-04 14:31:48', '98765431007'),
('90000000000009', 'UberCabs', 'Current', 2436.50, '2021-05-10 00:38:52', '98765431008'),
('90000000000010', 'IRCTC', 'Current', 1100.25, '2021-05-09 14:37:52', '98765431009'),
('90000000000011', 'IBNET', 'Current', 734.98, '2021-05-10 00:45:43', '98765431010');

-- --------------------------------------------------------

--
-- Table structure for table `cardaccount`
--

CREATE TABLE `cardaccount` (
  `CardNumber` text NOT NULL,
  `AccountNumber` text NOT NULL,
  `CIFNumber` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cardaccount`
--

INSERT INTO `cardaccount` (`CardNumber`, `AccountNumber`, `CIFNumber`) VALUES
('1001 0110 2002 0011', '00000000011', '98765432011'),
('1001 0110 2002 0006', '00000000006', '98765432006'),
('1001 0110 2002 0026', '00000000026', '98765432026');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bank`
--
ALTER TABLE `bank`
  ADD PRIMARY KEY (`AccountNumber`);

--
-- Indexes for table `bank2`
--
ALTER TABLE `bank2`
  ADD PRIMARY KEY (`AccountNumber`);

--
-- Indexes for table `cardaccount`
--
ALTER TABLE `cardaccount`
  ADD UNIQUE KEY `Account Number` (`AccountNumber`) USING HASH;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
