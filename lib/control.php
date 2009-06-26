<?php

function control_getlogin() {
	$gotname = 0; $ittr = 0;
	while ( !$gotname ) {
		$ittr++; if ( $ittr > 3 ) { die(func_casebold("Disconnecting - Too Many Login Attempts\n", 1)); }
		slowecho(func_casebold("Welcome Warrior!  Enter Your Login Name (OR '\033[1m\033[31mnew\033[32m') :-: ", 2));
		$uname = substr(fgets(STDIN), 0, 12);
		$uname = preg_replace("/\r\n/", "", $uname); 
		if ( user_exist($uname) ) { 
	                slowecho(func_casebold("Password :-: ",2));  
        	        $userid = user_getid($uname);
                	$password = preg_replace("/\r\n/", "", substr(fgets(STDIN), 0, 12));
	                if ( user_chkpass($userid, $password) ) { return $userid; }
			else { slowecho(func_casebold("Incorrect Password Dumbass!\n", 1)); }
	 	} else {
			if ( $uname == "new" ) { 
				return control_newuser();
				$gotname = 1;
				$newuser = 1;
			} 
			else { slowecho(func_casebold("User Name Not Found!\n", 2)); }
		}
	}
	return false;
}

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
		if ( $newfname == "" ) { slowecho(func_casebold("HEY! No Anonymous Players!\n", 1)); }
                else { $goodname = 1; }
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
		if ( $newsex != "M" && $newsex != "F" ) { slowecho(func_casebold("Not an Option Homeslice\n", 1)); }
		else $goodother = 1;
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
                if ( $newclass != "K" && $newclass != "D" && $newclass != "L" ) { slowecho(func_casebold("Not an Option Homeslice\n", 1)); }
                else $goodother = 1;
        } $goodother = 0;
	if ( $newclass == "K" ) { $newclassnum = 1; slowecho(func_casebold("Welcome warrior to the ranks of the Death Knights!\n", 2)); }
	if ( $newclass == "D" ) { $newclassnum = 2; slowecho(func_casebold("Feel the force young jedi.!\n", 2)); }
	if ( $newclass == "L" ) { $newclassnum = 3; slowecho(func_casebold("You're a real shitheel, you know that?\n", 2)); }
	$sql = "INSERT INTO {$MYSQL_PREFIX}users (`username`, `password`, `fullname`) VALUES ('{$newname}', '{$newpass}', '{$newfname}')";
	$result = mysql_query($sql, $db);
	$userid = mysql_insert_id();
	$sql2 = "INSERT INTO {$MYSQL_PREFIX}stats (`userid`, `sex`, `class`) VALUES ({$userid}, {$newsexnum}, {$newclassnum})";
	$result = mysql_query($sql2, $db);
	return $userid;
}

function control_noimp() {
	slowecho(func_casebold("Function not yet implemented, Sorry\n", 1));
}
?>
