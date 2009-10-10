<?php
/**
 * User Control Functions.
 * 
 * Controls user statistics and calls
 * 
 * @package phpsord
 * @subpackage phpsord-general
 * @author J.T.Sage
 */

/** Check if a user exists by username
 * 
 * @param string $username Username
 * @return bool true if found
 */
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

/** Check if a user exists by fullname
 * 
 * @param string $fullname fullname
 * @return bool true if found
 */
function user_fexist ($fullname) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT * FROM {$MYSQL_PREFIX}users WHERE fullname = '{$fullname}'";
	$result = mysql_query($sql, $db);
	if ( mysql_num_rows($result) == 0 ) {
		return false;
	} else {
		return true;
	}
}

/** Log a user out
 * 
 * @param int $userid User ID
 */
function user_logout ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$logoutsql = "DELETE FROM {$MYSQL_PREFIX}online WHERE userid = {$userid}";
	$results = mysql_query($logoutsql, $db);
}

/** Kill a user
 * 
 * @param int $userid User ID
 */
function user_setdead ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}users SET alive = 0 WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Check if a user is dead
 * 
 * @param int $userid User ID
 * @return bool true if dead
 */
function user_isdead ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT alive FROM {$MYSQL_PREFIX}users WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	if ( $line['alive'] ) { return false; } else { return true; }
}

/** Update last login time for a user
 * 
 * @param int $userid User ID
 */
function user_logintime ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}users SET last = CURRENT_TIMESTAMP WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Get a user ID from a username
 * 
 * This function is not search-safe, fails silently
 * 
 * @param string $username Username
 * @return int User ID
 */
function user_getid ($username) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT userid FROM {$MYSQL_PREFIX}users WHERE username = '{$username}'";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['userid'];
}

/** Get a user ID from a full name
 * 
 * This function is not search-safe, fails silently
 * 
 * @param string $fullname Fullname of user
 * @return int User ID
 */
function user_fgetid ($fullname) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT userid FROM {$MYSQL_PREFIX}users WHERE fullname = '{$fullname}'";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['userid']; 
}

/** Get a user fullname from ID
 * 
 * @param int $userid User ID
 * @return string Full User Name
 */
function user_gethandle ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT fullname FROM {$MYSQL_PREFIX}users WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['fullname'];
}

/** Get user level
 * 
 * @param int $userid User ID
 * @return int User Level
 */
function user_getlevel ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT level FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['level'];
}

/** Get player class
 * 
 * @param int $userid User ID
 * @return int Player Class
 */
function user_getclass ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT class FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['class'];
}

/** Get player sex
 * 
 * @param int $userid User ID
 * @return int Player sex (1=male. 2=female)
 */
function user_getsex ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT sex FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['sex'];
}

/** Get player's flirt status for the game day
 * 
 * @param int $userid User ID
 * @return int Player Flirt Status ( 1 = flirted already )
 */
function user_didflirt ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT flirt FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['flirt'];
}

/** Check if player is staying at the inn
 * 
 * @param int $userid User ID
 * @return int Player Inn Status (1=at the inn)
 */
function user_atinn ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT atinn FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['atinn'];
}

/** Set player has left the Inn
 * 
 * @param int $userid User ID
 */
function user_leaveinn ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET atinn = 0 WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Get player's armour type
 * 
 * @param int $userid User ID
 * @return int Player Armour type
 */
function user_getarmor ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT armor FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['armor'];
}

/** Get player's weapon type
 * 
 * @param int $userid User ID
 * @return int Player Weapon type
 */
function user_getweapon ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT weapon FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['weapon'];
}

/** Get player's gold on hand
 * 
 * @param int $userid User ID
 * @return int Player's gold on hand
 */
function user_getgold ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT gold FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['gold'];
}

/** Get player's gold in bank
 * 
 * @param int $userid User ID
 * @return int Player's gold in bank
 */
function user_getbank ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT bank FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['bank'];
}

/** Get player's defence
 * 
 * @param int $userid User ID
 * @return int Player's defense
 */
function user_getdef ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT def FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['def'];
}

/** Get player's strength
 * 
 * @param int $userid User ID
 * @return int Player's strength
 */
function user_getstr ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT str FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['str'];
}

/** Get player's current hitpoints
 * 
 * @param int $userid User ID
 * @return int Player's current hitpoints
 */
function user_gethp ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT hp FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['hp'];
}

/** Get player's total hitpoints
 * 
 * @param int $userid User ID
 * @return int Player's total hitpoints
 */
function user_gethpmax ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT hpmax FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['hpmax'];
}

/** Get player's experience
 * 
 * @param int $userid User ID
 * @return int Player's expierience
 */
function user_getexp ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT exp FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['exp'];
}

/** Get player's gems
 * 
 * @param int $userid User ID
 * @return int Player's gems
 */
function user_getgems ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT gems FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['gems'];
}

/** Get player's charm
 * 
 * @param int $userid User ID
 * @return int Player's charm
 */
function user_getcharm ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT charm FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['charm'];
}

/** Get player's remaining forest fights
 * 
 * @param int $userid User ID
 * @return int Player's remaining forest fights
 */
function user_getffight ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT ffight FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['ffight'];
}

/** Get player's remaining player fights
 * 
 * @param int $userid User ID
 * @return int Player's remaining player fights
 */
function user_getpfight ( $userid ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT pfight FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['pfight'];
}

/** Set player's armor
 * 
 * @param int $userid User ID
 * @param int $ins Armor type
 */
function user_setarmor ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET armor = {$ins} WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Set player's weapon
 * 
 * @param int $userid User ID
 * @param int $ins Weapon type
 */
function user_setweapon ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX; 
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET weapon = {$ins} WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Set player's level
 * 
 * @param int $userid User ID
 * @param int $ins New Level
 */
function user_setlevel ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET level = {$ins} WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player gold
 * 
 * @param int $userid User ID
 * @param int $ins Gold to add
 */
function user_givegold ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET gold = ( gold + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player gold
 * 
 * @param int $userid User ID
 * @param int $ins Gold to take
 */
function user_takegold ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET gold = ( gold - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player gold in bank
 * 
 * @param int $userid User ID
 * @param int $ins Gold to add to bank
 */
function user_givebank ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET bank = ( bank + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player gold from bank
 * 
 * @param int $userid User ID
 * @param int $ins Gold to remove from bank
 */
function user_takebank ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET bank = ( bank - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player defence points
 * 
 * @param int $userid User ID
 * @param int $ins Defence to add
 */
function user_givedef ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET def = ( def + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player defence points
 * 
 * @param int $userid User ID
 * @param int $ins Defence to remove
 */
function user_takedef ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET def = ( def - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player strength points
 * 
 * @param int $userid User ID
 * @param int $ins Strength to add
 */
function user_givestr ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET str = ( str + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player strength points
 * 
 * @param int $userid User ID
 * @param int $ins Strength to remove
 */
function user_takestr ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET str = ( str - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player experince
 * 
 * @param int $userid User ID
 * @param int $ins Experience to add
 */
function user_giveexp ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET exp = ( exp + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player experience
 * 
 * @param int $userid User ID
 * @param int $ins Experience to remove
 */
function user_takeexp ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET exp = ( exp - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player hitpoints
 * 
 * @param int $userid User ID
 * @param int $ins Hitpoints to add
 */
function user_givehp ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET hp = ( hp + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player hitpoints
 * 
 * @param int $userid User ID
 * @param int $ins Hitpoints to remove
 */
function user_takehp ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET hp = ( hp - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player max hitpoints
 * 
 * @param int $userid User ID
 * @param int $ins Max Hitpoints to add
 */
function user_givehpmax ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET hpmax = ( hpmax + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player max hitpoints
 * 
 * @param int $userid User ID
 * @param int $ins Max Hitpoints to remove
 */
function user_takehpmax ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET hpmax = ( hpmax - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player gems
 * 
 * @param int $userid User ID
 * @param int $ins Gems to add
 */
function user_givegems ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET gems = ( gems + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player gems
 * 
 * @param int $userid User ID
 * @param int $ins Gems to remove
 */
function user_takegems ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET gems = ( gems - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player charm
 * 
 * @param int $userid User ID
 * @param int $ins Charm to add
 */
function user_givecharm ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET charm = ( charm + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player charm
 * 
 * @param int $userid User ID
 * @param int $ins Charm to remove
 */
function user_takecharm ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET charm = ( charm - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player forest fights
 * 
 * @param int $userid User ID
 * @param int $ins Forest fights to add
 */
function user_giveffight ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET ffight = ( ffight + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player forest fights
 * 
 * @param int $userid User ID
 * @param int $ins Forest fights to remove
 */
function user_takeffight ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET ffight = ( ffight - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Give player vs player fights
 * 
 * @param int $userid User ID
 * @param int $ins Player fights to add
 */
function user_givepfight ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET pfight = ( pfight + {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Take player vs player fights
 * 
 * @param int $userid User ID
 * @param int $ins Player fights to remove
 */
function user_takepfight ( $userid, $ins ) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "UPDATE {$MYSQL_PREFIX}stats SET pfight = ( pfight - {$ins} ) WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
}

/** Check a user password
 * 
 * @param int $userid User ID
 * @param string $pass Password to check
 */
function user_chkpass ($userid, $pass) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT password FROM {$MYSQL_PREFIX}users WHERE userid = {$userid}";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	if ( $line['password'] == $pass ) { return true; }
	else { return false; }
}

?>
