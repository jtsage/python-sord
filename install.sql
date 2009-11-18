-- phpMyAdmin SQL Dump
-- version 3.2.2.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 17, 2009 at 08:13 PM
-- Server version: 5.1.37
-- PHP Version: 5.2.10-2ubuntu6.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `sord`
--

-- --------------------------------------------------------

--
-- Table structure for table `gameone_daily`
--

CREATE TABLE IF NOT EXISTS `gameone_daily` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data` varchar(80) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `gameone_daily`
--

INSERT INTO `gameone_daily` (`id`, `data`) VALUES
(1, '{31}Welcome to {1}{37}S{0}{32}.O.R.D');

-- --------------------------------------------------------

--
-- Table structure for table `gameone_dhtpatrons`
--

CREATE TABLE IF NOT EXISTS `gameone_dhtpatrons` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data` varchar(80) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `gameone_dhtpatrons`
--

INSERT INTO `gameone_dhtpatrons` (`id`, `data`, `nombre`) VALUES
(1, '{34}Welcome to the {31}Dark Horse Tavern', 'Chance');


-- --------------------------------------------------------

--
-- Table structure for table `gameone_dirt`
--

CREATE TABLE IF NOT EXISTS `gameone_dirt` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data` varchar(80) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `gameone_dirt`
--

INSERT INTO `gameone_dirt` (`id`, `data`, `nombre`) VALUES
(1, '{32}Mighty quiet around here...', 'Jack the Ripper');

-- --------------------------------------------------------

--
-- Table structure for table `gameone_flowers`
--

CREATE TABLE IF NOT EXISTS `gameone_flowers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data` varchar(80) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `gameone_flowers`
--

INSERT INTO `gameone_flowers` (`id`, `data`, `nombre`) VALUES
(1, '{34}Does this toga make me look {31}Fat?', 'Fairy #1'),
(2, '{36}No, just {1}ugly', 'Fairy #2');


-- --------------------------------------------------------

--
-- Table structure for table `gameone_mail`
--

CREATE TABLE IF NOT EXISTS `gameone_mail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from` int(10) unsigned NOT NULL,
  `to` int(10) unsigned NOT NULL,
  `message` varchar(300) NOT NULL,
  `sent` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `gameone_mail`
--

-- --------------------------------------------------------

--
-- Table structure for table `gameone_online`
--

CREATE TABLE IF NOT EXISTS `gameone_online` (
  `userid` int(10) unsigned DEFAULT NULL,
  `whence` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `userid` (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gameone_online`
--


-- --------------------------------------------------------

--
-- Table structure for table `gameone_patrons`
--

CREATE TABLE IF NOT EXISTS `gameone_patrons` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data` varchar(80) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `gameone_patrons`
--

INSERT INTO `gameone_patrons` (`id`, `data`, `nombre`) VALUES
(1, '{34}Welcome to the {31}Red Dragon {34}Inn', 'The Bartender');

-- --------------------------------------------------------

--
-- Table structure for table `gameone_setup`
--

CREATE TABLE IF NOT EXISTS `gameone_setup` (
  `name` varchar(10) NOT NULL,
  `valueint` int(11) DEFAULT NULL,
  `valuetext` varchar(40) DEFAULT NULL,
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gameone_setup`
--

INSERT INTO `gameone_setup` (`name`, `valueint`, `valuetext`) VALUES
('gdays', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `gameone_stats`
--

CREATE TABLE IF NOT EXISTS `gameone_stats` (
  `userid` int(10) unsigned NOT NULL,
  `class` int(4) unsigned NOT NULL DEFAULT '1',
  `sex` int(4) unsigned NOT NULL DEFAULT '1',
  `flirt` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `sung` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `master` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `atinn` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `horse` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `fairy` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `ffight` int(10) unsigned NOT NULL DEFAULT '20',
  `pfight` int(10) unsigned NOT NULL DEFAULT '3',
  `gems` int(10) unsigned NOT NULL DEFAULT '0',
  `gold` int(10) unsigned NOT NULL DEFAULT '500',
  `bank` int(10) unsigned NOT NULL DEFAULT '0',
  `level` int(4) unsigned NOT NULL DEFAULT '1',
  `charm` int(10) unsigned NOT NULL DEFAULT '0',
  `spclm` int(4) unsigned NOT NULL DEFAULT '0',
  `spclt` int(4) unsigned NOT NULL DEFAULT '0',
  `spcld` int(4) unsigned NOT NULL DEFAULT '0',
  `used` int(4) unsigned NOT NULL DEFAULT '0',
  `usem` int(4) unsigned NOT NULL DEFAULT '0',
  `uset` int(4) unsigned NOT NULL DEFAULT '0',
  `str` int(10) unsigned NOT NULL DEFAULT '10',
  `def` int(10) unsigned NOT NULL DEFAULT '1',
  `exp` int(10) unsigned NOT NULL DEFAULT '1',
  `hp` int(10) unsigned NOT NULL DEFAULT '20',
  `hpmax` int(10) unsigned NOT NULL DEFAULT '20',
  `weapon` int(10) unsigned NOT NULL DEFAULT '1',
  `armor` int(10) unsigned NOT NULL DEFAULT '1',
  `pkill` int(10) unsigned NOT NULL DEFAULT '0',
  `dkill` int(10) unsigned NOT NULL DEFAULT '0',
  `fuck` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`userid`),
  KEY `class` (`class`),
  KEY `level` (`level`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gameone_stats`
--

-- --------------------------------------------------------

--
-- Table structure for table `gameone_users`
--

CREATE TABLE IF NOT EXISTS `gameone_users` (
  `userid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(12) NOT NULL,
  `password` varchar(12) NOT NULL,
  `fullname` varchar(40) NOT NULL,
  `last` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `alive` int(10) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`userid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `gameone_users`
--

