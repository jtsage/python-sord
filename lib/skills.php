<?php

function skill_getuse_d ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT used FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['used'];
}

function skill_getuse_m ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT uset FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['uset'];
}

function skill_getuse_t ( $userid ) {
        global $db, $MYSQL_PREFIX;
        $sql = "SELECT uset FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line['uset'];
}

function skill_getuse ( $userid, $skill, $ins ) {
        global $db, $MYSQL_PREFIX;
        if ( $skill == 1 ) { $sname = 'used'; }
        if ( $skill == 2 ) { $sname = 'usem'; }
        if ( $skill == 3 ) { $sname = 'uset'; }
        $sql = "SELECT {$sname} FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line[$sname];
}

function skill_getskill ( $userid, $skill, $ins ) {
        global $db, $MYSQL_PREFIX;
        if ( $skill == 1 ) { $sname = 'spcld'; }
        if ( $skill == 2 ) { $sname = 'spclm'; }
        if ( $skill == 3 ) { $sname = 'spclt'; }
        $sql = "SELECT {$sname} FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
        $line = mysql_fetch_array($result);
        return $line[$sname];
}

function skill_giveuse ( $userid, $skill, $ins ) {
        global $db, $MYSQL_PREFIX;
	if ( $skill == 1 ) { $sname = 'used'; }
	if ( $skill == 2 ) { $sname = 'usem'; }
	if ( $skill == 3 ) { $sname = 'uset'; }
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET {$sname} = ( {$sname} + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function skill_takeuse ( $userid, $skill, $ins ) {
        global $db, $MYSQL_PREFIX;
        if ( $skill == 1 ) { $sname = 'used'; }
        if ( $skill == 2 ) { $sname = 'usem'; }
        if ( $skill == 3 ) { $sname = 'uset'; }
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET {$sname} = ( {$sname} - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function skill_giveskill ( $userid, $skill, $ins ) {
        global $db, $MYSQL_PREFIX;
        if ( $skill == 1 ) { $sname = 'spcld'; }
        if ( $skill == 2 ) { $sname = 'spclm'; }
        if ( $skill == 3 ) { $sname = 'spclt'; }
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET {$sname} = ( {$sname} + {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}

function skill_takeskill ( $userid, $skill, $ins ) {
        global $db, $MYSQL_PREFIX;
        if ( $skill == 1 ) { $sname = 'spcld'; }
        if ( $skill == 2 ) { $sname = 'spclm'; }
        if ( $skill == 3 ) { $sname = 'spclt'; } 
        $sql = "UPDATE {$MYSQL_PREFIX}stats SET {$sname} = ( {$sname} - {$ins} ) WHERE userid = {$userid}";
        $result = mysql_query($sql, $db);
}





?>
