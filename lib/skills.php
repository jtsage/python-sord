<?php
/**
 * User Special Skill Control Functions.
 * 
 * Controls user special skills
 * 
 * @package phpsord
 * @subpackage phpsord-general
 * @author J.T.Sage
 */

/** Get Death Knight use points
 * 
 * @param int $userid User ID
 * @return int Usage points
 */
function skill_getuse_d ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT used FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['used'];
}

/** Get Magician use points
 * 
 * @param int $userid User ID
 * @return int Usage points
 */
function skill_getuse_m ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT usem FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['uset'];
}

/** Get Thief use points
 * 
 * @param int $userid User ID
 * @return int Usage points
 */
function skill_getuse_t ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT uset FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['uset'];
}

/** Get Skill use points
 * 
 * @param int $userid User ID
 * @param int $skill User Class (1 = Death Night, 2 = Magic, 3 = Thief)
 * @param mixed $ins Unused variable apparently.
 * @return int Usage points
 */
function skill_getuse ( $userid, $skill, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	if ( $skill == 1 ) { $sname = 'used'; }
	if ( $skill == 2 ) { $sname = 'usem'; }
	if ( $skill == 3 ) { $sname = 'uset'; }
	$sql = "SELECT {$sname} FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line[$sname];
}

/** Get Skill points (expertise)
 * 
 * @param int $userid User ID
 * @param int $skill User Class (1 = Death Night, 2 = Magic, 3 = Thief)
 * @param mixed $ins Unused variable apparently.
 * @return int Skill points
 */
function skill_getskill ( $userid, $skill, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	if ( $skill == 1 ) { $sname = 'spcld'; }
	if ( $skill == 2 ) { $sname = 'spclm'; }
	if ( $skill == 3 ) { $sname = 'spclt'; }
	$sql = "SELECT {$sname} FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line[$sname];
}

/** Give Skill use points
 * 
 * @param int $userid User ID
 * @param int $skill User Class (1 = Death Night, 2 = Magic, 3 = Thief)
 * @param mixed $ins Skill use points to add
 */
function skill_giveuse ( $userid, $skill, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	if ( $skill == 1 ) { $sname = 'used'; }
	if ( $skill == 2 ) { $sname = 'usem'; }
	if ( $skill == 3 ) { $sname = 'uset'; }
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET {$sname} = ( {$sname} + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take Skill use points
 * 
 * @param int $userid User ID
 * @param int $skill User Class (1 = Death Night, 2 = Magic, 3 = Thief)
 * @param mixed $ins Skill use points to remove
 */
function skill_takeuse ( $userid, $skill, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	if ( $skill == 1 ) { $sname = 'used'; }
	if ( $skill == 2 ) { $sname = 'usem'; }
	if ( $skill == 3 ) { $sname = 'uset'; }
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET {$sname} = ( {$sname} - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give Skill points (expertise)
 * 
 * @param int $userid User ID
 * @param int $skill User Class (1 = Death Night, 2 = Magic, 3 = Thief)
 * @param mixed $ins Skill points to add
 */
function skill_giveskill ( $userid, $skill, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	if ( $skill == 1 ) { $sname = 'spcld'; }
	if ( $skill == 2 ) { $sname = 'spclm'; }
	if ( $skill == 3 ) { $sname = 'spclt'; }
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET {$sname} = ( {$sname} + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take Skill points (expertise)
 * 
 * @param int $userid User ID
 * @param int $skill User Class (1 = Death Night, 2 = Magic, 3 = Thief)
 * @param mixed $ins Skill points to remove
 */
function skill_takeskill ( $userid, $skill, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	if ( $skill == 1 ) { $sname = 'spcld'; }
	if ( $skill == 2 ) { $sname = 'spclm'; }
	if ( $skill == 3 ) { $sname = 'spclt'; } 
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET {$sname} = ( {$sname} - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

?>
