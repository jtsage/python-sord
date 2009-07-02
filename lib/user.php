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

function user_fexist ($fullname) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT * FROM {$MYSQL_PREFIX}users WHERE fullname = '{$fullname}'";
        $result = mysql_query($sql, $db);
        if ( mysql_num_rows($result) == 0 ) {
                return false;
        } else {
                return true;
        }
}

function user_logout ( $userid ) {
	global $db, $MYSQL_PREFIX;
	$logoutsql = "DELETE FROM {$MYSQL_PREFIX}online WHERE userid = {$userid}";
	$results = mysql_query($logoutsql, $db);
}

function user_setdead ( $userid ) {
	global $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}users SET alive = 0 WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

function user_isdead ( $userid ) {
	global $db, $MYSQL_PREFIX;
	$sql = "SELECT alive FROM {$MYSQL_PREFIX}users WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	if ( $line['alive'] ) { return false; } else { return true; }
}

function user_logintime ( $userid ) {
	global $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}users SET last = CURRENT_TIMESTAMP WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

function user_getid ($username) {
	global $db, $MYSQL_PREFIX;
	$sql = "SELECT userid FROM {$MYSQL_PREFIX}users WHERE username = '{$username}'";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['userid'];
}


function user_fgetid ($fullname) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT userid FROM {$MYSQL_PREFIX}users WHERE fullname = '{$fullname}'";
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

function user_getlevel ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT level FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['level'];
}

function user_getclass ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT class FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['class'];
}

function user_getsex ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT sex FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['sex'];
}

function user_didflirt ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT flirt FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['flirt'];
}

function user_atinn ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT atinn FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['atinn'];
}

function user_leaveinn ( $userid ) {
	global $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET atinn = 0 WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

function user_getarmor ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT armor FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['armor'];
}

function user_getweapon ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT weapon FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['weapon'];
}

function user_getgold ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT gold FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['gold'];
}

function user_getbank ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT bank FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['bank'];
}

function user_getdef ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT def FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['def'];
}

function user_getstr ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT str FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['str'];
}

function user_gethp ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT hp FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['hp'];
}

function user_gethpmax ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT hpmax FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['hpmax'];
}

function user_getexp ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT exp FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['exp'];
}

function user_getgems ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT gems FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['gems'];
}

function user_getcharm ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT charm FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['charm'];
}

function user_getffight ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT ffight FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['ffight'];
}

function user_getpfight ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT pfight FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['pfight'];
}

function user_setarmor ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET armor = {$ins} WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_setweapon ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX; 
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET weapon = {$ins} WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_setlevel ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET level = {$ins} WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_givegold ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET gold = ( gold + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takegold ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET gold = ( gold - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_givebank ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET bank = ( bank + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takebank ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET bank = ( bank - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}


function user_givedef ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET def = ( def + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takedef ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET def = ( def - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_givestr ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET str = ( str + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takestr ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET str = ( str - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_giveexp ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET exp = ( exp + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takeexp ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET exp = ( exp - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_givehp ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET hp = ( hp + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takehp ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET hp = ( hp - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_givehpmax ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET hpmax = ( hpmax + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takehpmax ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET hpmax = ( hpmax - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_givegems ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET gems = ( gems + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takegems ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET gems = ( gems - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_givecharm ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET charm = ( charm + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takecharm ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET charm = ( charm - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_giveffight ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET ffight = ( ffight + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takeffight ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET ffight = ( ffight - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_givepfight ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET pfight = ( pfight + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_takepfight ( $userid, $ins ) {
        global $db, $MYSQL_PREFIX;
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET pfight = ( pfight - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function user_chkpass ($userid, $pass) {
	global $db, $MYSQL_PREFIX;
	$sql = "SELECT password FROM {$MYSQL_PREFIX}users WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	if ( $line['password'] == $pass ) { return true; }
	else { return false; }
}

