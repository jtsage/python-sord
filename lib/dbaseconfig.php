<?php

GLOBAL $MYSQL_SERVER, $MYSQL_USER, $MYSQL_PASS, $MYSQL_DATABASE;

  $db = mysql_connect($MYSQL_SERVER, $MYSQL_USER, $MYSQL_PASS);
  if (!$db) {
    die('Could not connect: ' . mysql_error());
  }  

  $dbr = mysql_select_db($MYSQL_DATABASE, $db);
  if (!$dbr) {
    die ('Can\'t use database : ' . mysql_error());
  }

?>
