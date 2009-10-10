<?php
/**
 * User and Game Control Functions.
 * 
 * Controls user creation, login, and base game functions.
 * 
 * @package phpsord
 * @subpackage phpsord-general
 * @author J.T.Sage
 */

/**
 * Log in a user.  Calls to create a new user if needed.
 * 
 * @return mixed UserID on successful login, false on failed login.
 */
function control_getlogin() {
	$gotname = 0; $ittr = 0;
	while ( !$gotname ) {
		$ittr++; if ( $ittr > 3 ) { die(func_casebold("Disconnecting - Too Many Login Attempts\n", 1)); }
		slowecho(func_casebold("\nWelcome Warrior!  Enter Your Login Name (OR '\033[1m\033[31mnew\033[32m') :-: ", 2));
		$uname = substr(fgets(STDIN), 0, 12);
		$uname = preg_replace("/\r\n/", "", $uname); 
		if ( user_exist($uname) ) { 
			slowecho(func_casebold("\nPassword :-: ",2));  
			$userid = user_getid($uname);
			$password = preg_replace("/\r\n/", "", substr(fgets(STDIN), 0, 12));
			if ( user_chkpass($userid, $password) ) { return $userid;
			} else { slowecho(func_casebold("Incorrect Password Dumbass!\n", 1)); }
	 	} else {
			if ( $uname == "new" ) { 
				return control_newuser();
				$gotname = 1;
				$newuser = 1;
			} else { slowecho(func_casebold("User Name Not Found!\n", 2)); }
		}
	}
	return false;
}

/**
 * Create a new user
 * 
 * @return int UserID to control_getlogin for return to main program.
 */
function control_newuser() {
	GLOBAL $db, $MYSQL_PREFIX;
	slowecho(func_casebold("\nCreating a New Character...\n", 2));
	$goodname = 0; $goodpasswd = 0; $goodother = 0;
	while ( !$goodname ) {
		slowecho(func_casebold("\nPlease Choose a Username (12 characters MAX) :-: ", 2));
		$newname = preg_replace("/\r\n/", "", substr(fgets(STDIN), 0, 12));
		if ( user_exist($newname) ) { slowecho(func_casebold("Name In Use!\n", 1)); }
		else { $goodname = 1; }
	} $goodname = 0;
	while ( !$goodname ) {
		slowecho(func_casebold("\nAnd, how will you be addressed? (a Handle) (40 characters MAX) :-: ", 2));
		$newfname = preg_replace("/\r\n/", "", substr(fgets(STDIN), 0, 40));
		if ( $newfname == "" ) { slowecho(func_casebold("HEY! No Anonymous Players!\n", 1)); 
		} else { $goodname = 1; }
	}
	while ( !$goodpasswd ) {
		slowecho(func_casebold("\nPick a Password (12 characters MAX) :-: ", 2));
		$newpass = preg_replace("/\r\n/", "", substr(fgets(STDIN), 0, 12));
		if ( $newpass == "" ) { slowecho(func_casebold("Password MUST Not Be Empty\n", 1)); }
		else $goodpasswd = 1;
	}
	while ( !$goodother ) { 
		slowecho(func_casebold("\nYour Sex (M/F) :-: ", 2));
		$newsex = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		if ( $newsex != "M" && $newsex != "F" ) { slowecho(func_casebold("Not an Option Homeslice\n", 1));
		} else $goodother = 1;
	} $goodother = 0;
	if ( $newsex == "M" ) { $newsexnum = 1; slowecho(func_casebold("My, what a girly man you are...\n", 2)); }
	if ( $newsex == "F" ) { $newsexnum = 2; slowecho(func_casebold("Gee sweetheart, hope you don't break a nail...\n", 2)); }

	slowecho(func_casebold("\nPick that which best describes your childhood.\nFrom an early age, you remember:\n\n", 2));
	slowecho(func_normmenu("(D)abbling in the mystical forces"));
	slowecho(func_normmenu("(K)illing a lot of woodland creatures"));
	slowecho(func_normmenu("(L)ying, cheating, and stealing from the blind"));
	while ( !$goodother ) {
		slowecho(func_casebold("\nYour Choice (D/K/L) :-: ", 2));
		$newclass = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		if ( $newclass != "K" && $newclass != "D" && $newclass != "L" ) { slowecho(func_casebold("Not an Option Homeslice\n", 1)); 
		} else $goodother = 1;
	} $goodother = 0;
	if ( $newclass == "K" ) { $newclassnum = 1; slowecho(func_casebold("Welcome warrior to the ranks of the Death Knights!\n", 2)); }
	if ( $newclass == "D" ) { $newclassnum = 2; slowecho(func_casebold("Feel the force young jedi.!\n", 2)); }
	if ( $newclass == "L" ) { $newclassnum = 3; slowecho(func_casebold("You're a real shitheel, you know that?\n", 2)); }
	$sql = "INSERT INTO {$MYSQL_PREFIX}users (`username`, `password`, `fullname`) VALUES ('{$newname}', '{$newpass}', '{$newfname}')";
	$result = mysql_query($sql, $db);
	$userid = mysql_insert_id();
	$sql2 = "INSERT INTO {$MYSQL_PREFIX}stats (`userid`, `sex`, `class`) VALUES ({$userid}, {$newsexnum}, {$newclassnum})";
	$result = mysql_query($sql2, $db);
	skill_giveuse($userid, $newclassnum, 1);
	skill_giveskill($userid, $newclassnum, 1);
	return $userid;
}

/**
 * Function not implemented stub.
 */
function control_noimp() {
	slowecho(func_casebold("Function not yet implemented, Sorry\n", 1));
}

/** 
 * Interactivly find a user by name.
 * 
 * @param string $prompt Prompt for user input of username to search for.
 * @return mixed User id of found user, false if none found.
 */
function control_finduser($prompt) {
	global $userid;
	$prompt = $prompt . " \033[1;32m:\033[22m-\033[1;32m:\033[0m ";
	slowecho($prompt);
	$name = mysql_real_escape_string(preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN)))));
	if ( user_fexist($name) ) {
		$sendto = user_fgetid($name); $sendtofn = user_gethandle($sendto);
		if ( $sendto == $userid ) { return false; 
		} else {
			slowecho("\n  \033[32mDid you mean \033[1m{$sendtofn}\033[0m \033[1;30m(Y/N)\033[0m\033[32m ?\033[0m ");
			$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
			if ( $yesno == "Y" ) {
				return $sendto;
			} else { return false; }
		}
	} else { return false; }
}

/**
 * Read waiting in-game e-mail. Very simple.
 * 
 * @todo Add option to keep messages as read
 * @param int $userid User ID to pull in game mail for.
 * @return mixed False if no mail, no value if mail.
 */
function control_readmail($userid) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT `id`, `from`, `message`, DATE_FORMAT(sent, '%W %M %Y, %H:%i') as sent FROM {$MYSQL_PREFIX}mail WHERE `to` = {$userid}";
	$result = mysql_query($sql, $db);
	if ( mysql_num_rows($result) > 0 ) {
		while ( $line = mysql_fetch_array($result) ) {
			$thismail .= "\n  \033[1;37mNew Mail...\033[0m\n";
			$thismail .= art_line();
			$thismail .= "\033[32m  From: \033[1m" . user_gethandle($line['from']) . "\033[0m\n";
			$thismail .= "\033[32m  Date: \033[1m" . $line['sent'] . "\033[0m\n";
			$thismail .= "\033[32m  Message: " . func_colorcode($line['message']) . "\033[0m\n\n";
			slowecho($thismail);
			control_nukemail($line['id']);
			pauser();
		}
	} else { return false; }
}

/** 
 * Delete a mail message
 * 
 * @param int $msgid Message ID # to remove.
 */
function control_nukemail($msgid) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql .= "DELETE FROM {$MYSQL_PREFIX}mail WHERE `id` = {$msgid}";
	$result = mysql_query($sql, $db);
}

/** 
 * Get number of days game has been running.
 * 
 * @return int Number of days game has been running.
 */
function control_getruntime() {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql .= "SELECT valueint FROM {$MYSQL_PREFIX}setup WHERE `name` = 'gdays'";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	return $line['valueint'];
}

/**
 * Send in game mail to a user
 * 
 * @param int $userid User ID of the sender
 */
function control_sendmail($userid) {
	GLOBAL $db, $MYSQL_PREFIX;
	$fromid = $userid;
	$toid = control_finduser("\n  \033[32mSend mail to which user?");
	if ( $toid == 0 ) { return false; 
	} else {
		slowecho("\n  \033[32mYour message \033[1m:\033[0m ");
		$msg = mysql_real_escape_string(preg_replace("/\r\n/", "", chop(fgets(STDIN))));
		$sql = "INSERT INTO {$MYSQL_PREFIX}mail (`to`, `from`, `message`) VALUES ('{$toid}', '{$fromid}', '{$msg}')";
		$result = mysql_query($sql, $db);
		slowecho(func_casebold("\n  Message Sent\n"), 2);
		pauser();
	}
}

?>
