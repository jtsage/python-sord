<?php

function inn_mainmenu() {
	GLOBAL $userid;
	$thismenu  = "\n\n  \033[1;37mSaga of the Red Dragon - \033[0m\033[32mThe Inn\033[0m\n";
	$thismenu .= art_blueline();
	$thismenu .= "\033[32m  You enter the inn and are immediately hailed by several of the patrons.\033[0m\n";
	$thismenu .= "\033[32m  You respond with a wave and scan the room.  The room is filled with\033[0m\n";
	$thismenu .= "\033[32m  smoke from the torches that line the walls.  Oaken tables and chairs\033[0m\n";
	$thismenu .= "\033[32m  are scattered across the room.  You smile as the well-rounded Violet\033[0m\n";
	$thismenu .= "\033[32m  brushes by you....\033[0m\n\n";
	$usersex = user_getsex($userid);
	$flirtwith = ( $usersex == 1 ) ? "Violet" : "Seth Able";
	$thismenu .= menu_2col("(C)onverse with the patrons", "(D)aily News", 5, 5);
	$thismenu .= menu_2col("(F)lirt with {$flirtwith}", "(T)alk to the Bartender", 5, 5);
	$thismenu .= menu_2col("(G)et a Room", "(V)iew Your Stats", 5, 5);
	$thismenu .= menu_2col("(H)ear Seth Able The Bard", "(M)ake Announcment", 5, 5);
	$thismenu .= menu_2col("(R)eturn To Town", "", 5, 5);

	return $thismenu;
}

function inn_prompt() {
        GLOBAL $userid, $logontime;
        $currenttime = time(); $ontime = $currenttime - $logontime;
        $sec = $ontime % 60;
        $min = ( $ontime - $sec ) / 60;
        $psec = ( $sec < 10 ) ? "0{$sec}" : $sec;

	$thismenu  = "\n  \033[1;35mThe Red Dragon Inn\033[0m\033[1;30m (? for menu)\033[0m\n";
	$thismenu .= "  \033[1;30m(C,D,F,T,G,V,H,M,R)\033[0m\n\n";
	$thismenu .= "  \033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[1;37m[\033[22m{$min}:{$psec}\033[1m] \033[0m\033[32m:-: \033[0m";
	return $thismenu;
}

function inn_logic() {
        GLOBAL $userid, $xprt;
        $quitter = 0;
        while (!$quitter) {
                if ( !$xprt ) { slowecho(inn_mainmenu()); }
                slowecho(inn_prompt());
                $choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                switch ($choice) {
			case 'Q':
				$quitter = 1;
				break;
			case 'R':
				$quitter = 1;
				break;
			case '?':
				if ( $xprt ) { slowecho(inn_mainmenu()); }
				break;
			case 'D':
				slowecho(module_dailyhappen(1));
				pauser();
				break;
			case 'V':
				slowecho(module_viewstats($userid));
				pauser();
				break;
			case 'M':
				module_announce();
				break;
			case 'C':
				inn_converse();
				break;
			case 'H':
				inn_bardmenu();
				break;
		}
	}
}


function inn_converse() {
        GLOBAL $db, $MYSQL_PREFIX, $userid;
        $sql = "SELECT data, nombre FROM {$MYSQL_PREFIX}patrons ORDER BY id ASC LIMIT 10";
        $result = mysql_query($sql, $db);
        $output = "\n\n  \033[1;37mConverse with the Patrons\033[22;32m....\033[0m\n";
        $output .= "\033[32m                                      -=-=-=-=-=-\033[0m\n";
        while ( $line = mysql_fetch_array($result) ) {
                $output .= "    \033[32m{$line['nombre']} \033[1;37msays... \033[0m\033[32m" . func_colorcode($line['data']);
                $output .= "\n\033[32m                                      -=-=-=-=-=-\033[0m\n";
        }
	$output .= "\n  \033[32mAdd to the conversation? \033[1m: \033[0m";
	slowecho($output);
	$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
        if ( $yesno == "Y" ) {
		slowecho(func_casebold("\n  What say you? :-: ", 2));
		$ann = preg_replace("/\r\n/", "", chop(fgets(STDIN)));
	        $insann = mysql_real_escape_string($ann);
		$insnme = user_gethandle($userid);
	        $sql = "INSERT INTO {$MYSQL_PREFIX}patrons ( `data`, `nombre` ) VALUES ('{$insann}', '{$insnme}')";
	        $result = mysql_query($sql, $db);
	        slowecho(func_casebold("\n  Wisdom added!\n", 2));
		pauser();
	}
}

function inn_bardmenu() {
	global $userid;
        $thismenu  = "\n\n  \033[1;37mSaga of the Red Dragon - \033[0m\033[32mSeth Able\033[0m\n";
        $thismenu .= art_blueline();
	$thismenu .= "  \033[32mYou stumble over to a dank corner of the Inn.\n  Seth able looks at you expectantly...\n\n";
	$thismenu .= func_normmenu("(A)sk Seth Able to Sing");
	$thismenu .= func_normmenu("(R)eturn to the Inn");
	$thismenu .= "\n  \033[1;35mSeth Able the Bard\033[0m\033[1;30m (A,R,Q) (? for menu)\033[0m\n\n";
	$thismenu .= "  \033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[0m\033[32m:-: \033[0m";
	$miniquit = 0;
	while ( !$miniquit ) {
                slowecho($thismenu);
                $minichoice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                switch ($minichoice) {
			case 'R':
				$miniquit = 1;
				break;
			case 'Q':
				$miniquit = 1;
				break;
			case 'A':
				inn_hearbard();
				break;
		}
	}
}

function inn_hearbard() {
	GLOBAL $db, $MYSQL_PREFIX, $userid, $thebard;
	$sqldidhear = "SELECT sung FROM {$MYSQL_PREFIX}stats WHERE userid = {$userid}";
	$sqlsethear = "UPDATE {$MYSQL_PREFIX}stats SET sung = 1 WHERE userid = {$userid}";
	$result = mysql_query($sqldidhear, $db);
	$line = mysql_fetch_array($result);
	if ( $line['sung'] == 0 ) {
		slowecho("\n  \033[32mSeth thinks for a moment, picks up his lute, and begins...\n\n");
		$songnum = rand(1, 10);
		$pname = user_gethandle($userid);
		foreach( $thebard[$songnum][0] as $lyrics ) {
			sleep(1);
			$lyrics = preg_replace("/\.\.\.\"/", "\033[37m...\"\033[32m", $lyrics);
			$lyrics = preg_replace("/\"\.\.\./", "\033[37m\"...\033[0m", $lyrics);
			$lyrics = preg_replace("/XX/", "\033[1m{$pname}\033[22m", $lyrics);
			slowecho("  {$lyrics}\n");
		}
		slowecho("\n  \033[1;32m{$thebard[$songnum][1][0]}\033[0m\n");
		slowecho("\n  \033[1;34m{$thebard[$songnum][1][1]}\033[0m\n\n");
		$sqlupdate = "UPDATE {$MYSQL_PREFIX}stats SET {$thebard[$songnum][2]} WHERE userid = {$userid}";
		$result = mysql_query($sqlupdate, $db);
		$result = mysql_query($sqlsethear, $db);
		pauser();

	} else { slowecho(func_casebold("\n  Seth says:  I'm a bit tired, maybe tommorow...\n", 2)); }
}

?>
