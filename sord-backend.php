#!/usr/bin/php
<?php

require_once("config.php");
require_once("lib/dbaseconfig.php");

$dailysayings = array (
	0 => 'More children are missing today.',
	1 => 'A small girl was missing today.',
	2 => 'The town is in grief.  Several children didnt come home today.',
	3 => 'Dragon sighting reported today by a drunken old man.',
	4 => 'Despair covers the land - more bloody remains have been found today.',
	5 => 'A group of children did not return from a nature walk today.',
	6 => 'The land is in chaos today.  Will the abductions ever stop?',
	7 => 'Dragon scales have been found in the forest today..Old or new?',
	8 => 'Several farmers report missing cattle today.',
	9 => 'A Child was found today!  But scared deaf and dumb.');
$randsaying = rand(0, 9);
$interest = ($SORD_BANKINT / 100) + 1;

$sql1 = "UPDATE {$MYSQL_PREFIX}stats SET ffight = {$SORD_FFIGHT} WHERE ffight < {$SORD_FFIGHT}20";
$sql2 = "UPDATE {$MYSQL_PREFIX}stats SET pfight = {$SORD_PFIGHT} WHERE pfight < {$SORD_PFIGHT}";
$sql3 = "UPDATE {$MYSQL_PREFIX}stats SET usem = spclm";
$sql4 = "UPDATE {$MYSQL_PREFIX}stats SET used = (spcld DIV 5) + 1 WHERE spcld > 0";
$sql5 = "UPDATE {$MYSQL_PREFIX}stats SET uset = (spclt DIV 5) + 1 WHERE spclt > 0";
$sql6 = "INSERT INTO {$MYSQL_PREFIX}daily ( `data` ) VALUES ( '{31}{$dailysayings[$randsaying]}' )";
$sql7 = "UPDATE {$MYSQL_PREFIX}users SET alive = 1 WHERE alive = 0";
$sql8 = "UPDATE {$MYSQL_PREFIX}stats SET bank = ( bank * {$interest} ) WHERE bank > 0";
$sql9 = "DELETE FROM {$MYSQL_PREFIX}users WHERE last < ( CURRENT_TIMESTAMP - INTERVAL {$SORD_DELINACT} DAY )";
$sql0 = "UPDATE {$MYSQL_PREFIX}setup SET valueint = ( valueint + 1 ) WHERE `name` = 'gdays'";

$sqla = "UPDATE {$MYSQL_PREFIX}stats SET flirt = 0 WHERE 1";
$sqlb = "UPDATE {$MYSQL_PREFIX}stats SET sung = 0 WHERE 1";
$sqlc = "UPDATE {$MYSQL_PREFIX}stats SET master = 0 WHERE 1";


$result = mysql_query($sql1, $db);
$result = mysql_query($sql2, $db);
$result = mysql_query($sql3, $db);
$result = mysql_query($sql4, $db);
$result = mysql_query($sql5, $db);
$result = mysql_query($sql6, $db);
$result = mysql_query($sql7, $db);
$result = mysql_query($sql8, $db);
$result = mysql_query($sql9, $db);
$result = mysql_query($sql0, $db);
$result = mysql_query($sqla, $db);
$result = mysql_query($sqlb, $db);





?>
