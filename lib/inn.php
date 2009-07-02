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
			case 'T':
				inn_bartend();
				break;
			case 'V':
				slowecho(module_viewstats($userid));
				pauser();
				break;
			case 'M':
				module_announce();
				break;
			case 'F':
				if ( ! (user_didflirt($userid)) ) {
					inn_flirt();
				} else { slowecho("\n  \033[32mYou have already flirted once today...\033[0m\n"); }
				pauser();
				break;
			case 'C':
				inn_converse();
				break;
			case 'H':
				inn_bardmenu();
				break;
			case 'G':
				inn_getroom();
				break;
		}
	}
}

function inn_getroom() {
	GLOBAL $db, $MYSQL_PREFIX, $userid;
	$price = user_getlevel($userid) * 400;
	slowecho("\n  \033[32mThe bartender approaches you at the mention of a room.\033[0m\n");
	slowecho("  \033[35m\"You want a room, eh?  That'll be {$price} gold!\"\033[0m\n");
	slowecho("  \033[32mDo you agree? \033[1m: \033[0m");
        $yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
        if ( $yesno == "Y" ) {
		if ( user_getgold($userid) < $price ) { slowecho("\n  \033[35m\"How bout you find yourself a nice stretch of cardboard box ya bum?\033[0m\n"); 
		} else {
			user_takegold($userid, $price);
			$sql = "UPDATE {$MYSQL_PREFIX}stats SET atinn = 1 WHERE userid = {$userid}";
			$result = mysql_query($sql, $db);
			user_logout($userid);
			die(func_casebold("Quitting to a nice, warm bed...\n", 1));
		}
	} else { slowecho("\n  \033[35m\"Suit yourself...\"\033[0m\n"); }
}

function inn_converse() {
        GLOBAL $db, $MYSQL_PREFIX, $userid;
        $sql = "SELECT data, nombre FROM (SELECT * FROM {$MYSQL_PREFIX}patrons ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id";
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


function inn_flirt() {
	GLOBAL $userid, $flirts;
	$sexo = user_getsex($userid);
	slowecho(inn_flirt_menu($sexo));
	slowecho("\n  \033[32mYour Choice? \033[1m: \033[0m ");
	if ( $sexo == 1 ) { inn_flirt_violet(); } else { inn_flirt_seth(); }
}

function inn_flirt_violet() {
	GLOBAL $userid, $MYSQL_PREFIX, $db;
	$minichoice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	$usercharm = user_getcharm($userid);
	$userlevel = user_getlevel($userid);
	$gexp = 0; $try = 0; $screw;
        switch ($minichoice) {
		case 'W':
			slowecho("\n  \033[32mYou pluck up your courage, catch Violet's eye,\n  and seductivly wink...\033[0m\n");
			inn_flirt_and(); $try = 1;
			if ( $usercharm > 0 ) {
				$gexp = 5 * $userlevel;
				slowecho("\n  \033[1;34mViolet smiles and blushes deeply.\n  Your relationship is taking off!\033[0m\n");
				slowecho("  \033[32mYou gain \033[1m{$gexp}\033[22m experience.\033[0m\n");
			} else { slowecho("\n  \033[1;31mViolet glares back and returns to her work.\n"); }
			break;
                case 'K':
                        slowecho("\n  \033[32mAs Violet delivers your beer, you grab her hand,\n  pucker up and kiss it...\033[0m\n");
                        inn_flirt_and(); $try = 1;
                        if ( $usercharm > 1 ) {
                                $gexp = 10 * $userlevel;
                                slowecho("\n  \033[1;34mViolet giggles and blushes deeply.\n  Your relationship is taking off!\033[0m\n");
                                slowecho("  \033[32mYou gain \033[1m{$gexp}\033[22m experience.\033[0m\n");
                        } else { slowecho("\n  \033[1;31mViolet pulls her hand back and slaps you across the face.\n"); }
                        break;
                case 'P':
                        slowecho("\n  \033[32mYou bolt up as Violet takes your hard earned gold,\n  smile, and plant one on her lips...\033[0m\n");
                        inn_flirt_and(); $try = 1;
                        if ( $usercharm > 3 ) {
                                $gexp = 20 * $userlevel;
                                slowecho("\n  \033[1;34mViolet gasps and hurries away.\n  Your relationship is starting to really move now!\033[0m\n");
                                slowecho("  \033[32mYou gain \033[1m{$gexp}\033[22m experience.\033[0m\n");
                        } else { slowecho("\n  \033[1;31mViolet knees you right in the family gem stones.\n"); }
                        break;
                case 'S':
                        slowecho("\n  \033[32mYou beckon Violet over, and sit her on your lap...\033[0m\n");
                        inn_flirt_and(); $try = 1;
                        if ( $usercharm > 7 ) {
                                $gexp = 30 * $userlevel; 
                                slowecho("\n  \033[1;34mViolet snuggles down for a moment, then hurries back to work.\n  Very smooth ex-lax.\033[0m\n");
                                slowecho("  \033[32mYou gain \033[1m{$gexp}\033[22m experience.\033[0m\n");
                        } else { slowecho("\n  \033[1;31mViolet grabs a fork from the table and embeds it in your knee.\n"); }
                        break;
                case 'G':
                        slowecho("\n  \033[32mAs you wander the bar, you spot Violet, and firmly caress\n  her glorious behind...\033[0m\n");
                        inn_flirt_and(); $try = 1;
                        if ( $usercharm > 15 ) {
                                $gexp = 40 * $userlevel; 
                                slowecho("\n  \033[1;34mViolet yalps, spins around and gives you a peck on the cheek.\n  Lovely moves son...\033[0m\n");
                                slowecho("  \033[32mYou gain \033[1m{$gexp}\033[22m experience.\033[0m\n");
                        } else { slowecho("\n  \033[1;31mViolet twists your arm behind your back, dumps a beer on\n  you, and walks away.  Ouch.\n"); }
                        break;
                case 'C':
                        slowecho("\n  \033[32mYou slam your beer down, exclaim 'the hell with it', grab Violet,\n  and head upstairs to the nearest unused room...\033[0m\n");
                        inn_flirt_and(); $try = 1; 
                        if ( $usercharm > 31 ) {
                                $gexp = 40 * $userlevel; $screw = 1;
                                slowecho("\n  \033[1;34mViolet shifts in your arms, revealing that she\n  'forgot' to wear something this morning.\n  Unfortunatally, women's personal uh...  'hygiene' wasn't\n  what it is now in the dark ages.\033[0m\n");
                                slowecho("  \033[32mYou gain \033[1m{$gexp}\033[22m experience.\033[0m\n");
                        } else { slowecho("\n  \033[1;31mViolet tears off your pants, grabs a knife, and only your 'small stature'\n  prevents a Bobbit incident.  Bummer.\n"); }
                        break;
	}
	if ( $try ) {
		$sql = "UPDATE {$MYSQL_PREFIX}stats SET flirt = 1 WHERE userid = {$userid}";
		$result = mysql_query($sql, $db);
	}
	if ( $gexp > 0 ) {
		user_giveexp($userid, $gexp);
	}
	if ( $screw ) {
		$vd = array('herpes', 'crabs', 'ghonnereah');
		$vdc = rand(0, 2);
		$namey = user_gethandle($userid);

		$sql = "INSERT INTO {$MYSQL_PREFIX}daily ( `data` ) VALUES ( '{32}{1}{$namey}{0}{32} got a little somethin somethin today.  {34}And {$vd[$vdc]}.')";
		$result = mysql_query($sql, $db);
	}
}

function inn_flirt_and() {
	sleep(1); slowecho("\n  \033[1;37m..."); sleep(1); slowecho("\033[31mAND\033[37m"); sleep(1); slowecho("...\033[0m");
}

function inn_flirt_menu($sexy) {
	GLOBAL $flirts;
	foreach ( $flirts[$sexy] as $sayings ) {
		$thismenu .= func_normmenu($sayings[1]);
	}
	return $thismenu;
}

function inn_bartend() {
        GLOBAL $userid, $xprt, $MYSQL_PREFIX, $db;
	$miniquit = 0;
	if ( user_getlevel($userid) == 1 ) {
		slowecho("\n  \033[32mNever heard of ya...  Come back when you've done something.\033[0m\n");
		$miniquit = 1;
	}
        while (!$miniquit) {
                slowecho(inn_bartendmenu());
                $choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                switch ($choice) {
			case '?':
				break;
			case 'R':
				$miniquit = 1;
				break;
			case 'Q':
				$miniquit = 1;
				break;
			case 'V':
				slowecho("\n  \033[35m\"Ya want to know about \033[1mViolet\033[22m do ya?  She is every warrior's\033[0m");
				slowecho("\n  \033[35mwet dream...But forget it, Lad, she only goes for the type\033[0m");
				slowecho("\n  \033[35mof guy who would help old peple...\"\033[0m\n");
				pauser();
				break;
			case 'B':
				control_noimp();
				pauser();
				break;
			case 'C':
				slowecho("\n  \033[35m\"Ya wanna change your name, eh?  Yeah..\033[0m");
				$curname = user_gethandle($userid);
				$curclass = user_getclass($userid);
				$price = user_getlevel($userid) * 500;
				$lnclass = ( $curclass == 1 ) ? "the Death Knight" : (( $curclass == 2 ) ? "the magician" : "the thief");
				slowecho("\n  \033[35m{$curname} {$lnclass} does sound kinda funny..\033[0m");
				slowecho("\n  \033[35mit would cost ya {$price} gold... Deal?\"\033[0m");
				slowecho("\n  \033[32mChange your name? [\033[1mN\033[22m]\033[0m ");
				$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                                if ( $yesno == "Y" ) { 
					if ( user_getgold($userid) < $price ) { slowecho("\n  \033[35m\"Then I suggest you go find some more gold...\"\033[0m\n"); 
					} else {
						$nope = 0;
						slowecho("\n  \033[32mWhat'll it be? \033[1m: \033[0m");
						$ann = preg_replace("/\r\n/", "", chop(fgets(STDIN)));
					        $insann = mysql_real_escape_string($ann);
						if ( $insann == "" ) { $nope = 1; }
						elseif ( preg_match("/barak/i", $insann) )       { $nope = 1; slowecho("\n  \033[31m** \033[35mNaw, the real Barak would decapitate you if he found out. \033[31m**\033[0m\n"); }
						elseif ( preg_match("/seth able/i", $insann) )   { $nope = 1; slowecho("\n  \033[31m** \033[35mYou are not God! \033[31m**\033[0m\n"); }
						elseif ( preg_match("/red dragon/i", $insann) )  { $nope = 1; slowecho("\n  \033[31m** \033[35mOh go plague some other land! \033[31m**\033[0m\n"); }
						elseif ( preg_match("/seth/i", $insann) )        { $nope = 1; slowecho("\n  \033[31m** \033[35mYou are not Seth Able!  Don't take his name in vain! \033[31m**\033[0m\n"); }
						elseif ( preg_match("/turgon/i", $insann) )      { $nope = 1; slowecho("\n  \033[31m** \033[35mHaw.  Hardly - Turgon has muscles. \033[31m**\033[0m\n"); }
						elseif ( preg_match("/violet/i", $insann) )      { $nope = 1; slowecho("\n  \033[31m** \033[35mHaw.  Hardly - Violet has breasts. \033[31m**\033[0m\n"); }
						elseif ( preg_match("/dragon/i", $insann) )      { $nope = 1; slowecho("\n  \033[31m** \033[35mYou ain't Bruce Lee, so get out! \033[31m**\033[0m\n"); }
						elseif ( preg_match("/bartender/i", $insann) )   { $nope = 1; slowecho("\n  \033[31m** \033[35mNah, the bartender is smarter than you! \033[31m**\033[0m\n"); }
						elseif ( preg_match("/chance/i", $insann) )      { $nope = 1; slowecho("\n  \033[31m** \033[35mWhy not go take a chance with a rattlesnake? \033[31m**\033[0m\n"); } 

						if ( !$nope ) {
							slowecho("\n  \033[32mName Changed.\033[0m\n");
							$namesql = "UPDATE {$MYSQL_PREFIX}users SET fullname = '{$insname}' WHERE userid = {$userid}";
							$result = mysql_query($namesql, $db);
							user_takegold($userid, $price);
						}
					}
				} else { slowecho("\n  \033[35m\"Fine...Keep your stupid name...See if I care...\"\033[0m\n"); }
				pauser();
				break;
			case 'D':
				if ( user_getlevel($userid) == 12 ) {
					slowecho("\n  \033[32mA \033[1;31mRed Dragon\033[0m\033[32m eh?  Have you tried to \033[1mS\033[22mearch?\n"); }
				break;
			case 'G':
				slowecho("\n  \033[35m\"You have \033[1;37mGems\033[0m\033[35m, eh?  I'll give ya a pint of magic elixer for two.\"\033[0m\n");
				slowecho("  \033[32mBuy how many elixers? : ");
				$number = preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN))));
				if ( $number > 0 ) {
					$usergems = user_getgems($userid);
					if ( ($number * 2) > $usergems ) { slowecho("\n  \033[31mYou don't have that many gems!\033[0m\n");
					} else { /*sell and process elixer */
						slowecho("\n  \033[32mIncrease which stat?\033[0m\n");
						slowecho(func_normmenu("(H)itpoints"));
						slowecho(func_normmenu("(S)trength"));
						slowecho(func_normmenu("(V)itality"));
						slowecho(func_normmenu("(N)evermind"));
						$tinyquit = 0;
						while(!$tinyquit) {
							slowecho("  \033[32mChoose : \033[0m");
							$gemsused = $number * 2;
							$bart = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
							switch ($bart) {
								case 'N':
									$tinyquit = 1;
									break;
								case 'H':
									user_givehpmax($userid, $number);
									user_givehp($userid, $number);
									user_takegems($userid, $gemsused);
									break;
								case 'S':
									user_givestr($userid, $number);
									user_takegems($userid, $gemsused);
									break;
								case 'V':
									user_givedef($userid, $number);
									user_takegems($userid, $gemsused);
									break;
							}
						}
						slowecho("\n  \033[32mPleasure doing business with you\033[0m\n");
					}
				}
				break;  
		}
	}
}

function inn_bartendmenu() {
        GLOBAL $userid, $logontime;
        $currenttime = time(); $ontime = $currenttime - $logontime;
        $sec = $ontime % 60;
        $min = ( $ontime - $sec ) / 60;
        $psec = ( $sec < 10 ) ? "0{$sec}" : $sec;

        $thismenu  = "\n\n  \033[1;37mSaga of the Red Dragon - \033[0m\033[32mBartender\033[0m\n";
        $thismenu .= art_blueline();
        $thismenu .= "  \033[32mThe bartender escorts you into a back\033[0m\n";
	$thismenu .= "  \033[32mroom.  \033[35m\"I have heard yer name before kid...\033[0m\n";
	$thismenu .= "  \033[35mwhat do ya want to talk about?\"\033[0m\n\n";
	$thismenu .= func_normmenu("(V)iolet");
	$thismenu .= func_normmenu("(G)ems");
	$thismenu .= func_normmenu("(B)ribe");
	$thismenu .= func_normmenu("(C)hange your name");
	$thismenu .= func_normmenu("(R)eturn to Bar");
	$thismenu .= "\n  \033[35m\"Well?\" \033[32mThe bartender inquires. \033[1;30m(V,G,B,C,R) (? for menu)\033[0m\n";
        $thismenu .= "\n  \033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[1;37m[\033[22m{$min}:{$psec}\033[1m] \033[0m\033[32m:-: \033[0m";
	return $thismenu;
}

?>
