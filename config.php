<?php
/**
 * Configuration file.
 * 
 * Contains all configuration data for the game
 * 
 * @package phpsord
 * @subpackage phpsord-system
 * @author J.T.Sage
 * @staticvar string $MYSQL_SERVER Hostname of mysql server.
 * @staticvar string $MYSQL_USER User for mysql server.
 * @staticvar string $MYSQL_PASS Password for mysql server.
 * @staticvar string $MYSQL_DATABASE Database to use on mysql server.
 * @staticvar string $MYSQL_PREFIX Prefix for all mysql table names.
 * @staticvar string $SORD_HOST Name of the game host.  FQDN.
 * @staticvar string $SORD_ADMIN Name of the game admin.
 * @staticvar int $SORD_DELINACT Number of game days to delete inactive users after.
 * @staticvar int $SORD_DAYLENGTH Length of the game days, in hours.
 * @staticvar int $SORD_BANKINT Interest to be paid on bank acounts per game day.
 * @staticvar int $SORD_FFIGHT Number of forest fights to start each game day, per player.
 * @staticvar int $SORD_PFIGHT Number of player fights to start each game day, per player.
 */

$MYSQL_SERVER = "localhost";
$MYSQL_USER = "sord";
$MYSQL_PASS = "dr0s";
$MYSQL_DATABASE = "sord";
$MYSQL_PREFIX = "gameone_";
$SORD_HOST = "bbs.jtsage.com";
$SORD_ADMIN = "JTSage";

$SORD_DELINACT = 256;
$SORD_DAYLENGTH = 8;
$SORD_BANKINT = 10;
$SORD_FFIGHT = 30;
$SORD_PFIGHT = 5;

?>
