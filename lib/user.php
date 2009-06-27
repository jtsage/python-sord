<?php

/* User Subroutines */

function user_exist ($username) {
	global $db, $MYSQL_PREFIX;
	$sql = "SELECT * FROM {$MYSQL_PREFIX}users WHERE username = '{$username}'";
 	$result = mysql_query($sql, $db);
	if ( mysql_num_rows($result) == 0 ) { 
		return false;
	} else { 
		return true;
	}
}

function user_getid ($username) {
	global $db, $MYSQL_PREFIX;
	$sql = "SELECT userid FROM {$MYSQL_PREFIX}users WHERE username = '{$username}'";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['userid'];
}

function user_gethandle ( $userid ) {
	global $db, $MYSQL_PREFIX;
	$sql = "SELECT fullname FROM {$MYSQL_PREFIX}users WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['fullname'];
}

function user_getarmor ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT armor FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['armor'];
}


function user_chkpass ($userid, $pass) {
	global $db, $MYSQL_PREFIX;
	$sql = "SELECT password FROM {$MYSQL_PREFIX}users WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	if ( $line['password'] == $pass ) { return true; }
	else { return false; }
}

