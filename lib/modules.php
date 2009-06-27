<?php
function module_viewstats($userid) {
	GLOBAL $db, $MYSQL_PREFIX, $weapon, $armor, $classes;
	$sql = "SELECT s.*, fullname FROM {$MYSQL_PREFIX}users u, {$MYSQL_PREFIX}stats s WHERE u.userid = {$userid} AND u.userid = s.userid";
	$result = mysql_query($sql, $db);
	$line = mysql_fetch_array($result);
	$output  = "\n\n\033[1m\033[37m{$line['fullname']}\033[0m\033[32m's Stats...\n";
	$output .= art_line();
	$output .= "\033[32m Experience    : \033[1m{$line['exp']}\033[0m\n";
	$output .= "\033[32m Level         : \033[1m{$line['level']}\033[0m"  . padnumcol($line['level'], 20)  . "\033[32mHitPoints          : \033[1m{$line['hp']} \033[22mof\033[1m {$line['hpmax']}\033[0m\n";
	$output .= "\033[32m Forest Fights : \033[1m{$line['ffight']}\033[0m" . padnumcol($line['ffight'], 20) . "\033[32mPlayer Fights Left : \033[1m{$line['pfight']}\033[0m\n";
	$output .= "\033[32m Gold In Hand  : \033[1m{$line['gold']}\033[0m"   . padnumcol($line['gold'], 20)   . "\033[32mGold In Bank       : \033[1m{$line['bank']}\033[0m\n";
	$output .= "\033[32m Weapon        : \033[1m{$weapon[$line['weapon']]}\033[0m"   . padnumcol($weapon[$line['weapon']], 20)   . "\033[32mAttack Strength    : \033[1m{$line['str']}\033[0m\n";
	$output .= "\033[32m Armor         : \033[1m{$armor[$line['armor']]}\033[0m"   . padnumcol($armor[$line['armor']], 20)   . "\033[32mDefensive Strength : \033[1m{$line['def']}\033[0m\n";
	$output .= "\033[32m Charm         : \033[1m{$line['charm']}\033[0m"   . padnumcol($line['charm'], 20)   . "\033[32mGems               : \033[1m{$line['gems']}\033[0m\n\n";
	if ( $line['class'] == 1 || $line['spcld'] > 0 ) {
		$output .= "\033[32m The {$classes[1]} Skills: \033[1m" . ( $line['spcld'] > 0 ? $line['spcld'] : "NONE" ) . padnumcol(($line['spcld'] > 0 ? $line['spcld'] : "NONE"), 11) . "\033[0m\033[32mUses Today: (\033[1m{$line['skilluse']}\033[22m)\033[0m\n"; }
	if ( $line['class'] == 2 || $line['spclm'] > 0 ) {
		$output .= "\033[32m The {$classes[2]} Skills: \033[1m" . ( $line['spclm'] > 0 ? $line['spclm'] : "NONE" ) . padnumcol(($line['spclm'] > 0 ? $line['spclm'] : "NONE"), 15) . "\033[0m\033[32mUses Today: (\033[1m{$line['skilluse']}\033[22m)\033[0m\n"; }
	if ( $line['class'] == 3 || $line['spclt'] > 0 ) {
		$output .= "\033[32m The {$classes[3]} Skills: \033[1m" . ( $line['spclt'] > 0 ? $line['spclt'] : "NONE" ) . padnumcol(($line['spclt'] > 0 ? $line['spclt'] : "NONE"), 18) . "\033[0m\033[32mUses Today: (\033[1m{$line['skilluse']}\033[22m)\033[0m\n"; }
	$output .= "\n \033[1;32mYou are currently interested in \033[37mThe {$classes[$line['class']]} \033[32mskills.\n\n";
	return $output;
}

function module_dailyhappen($noprmpt) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT data FROM {$MYSQL_PREFIX}daily ORDER BY id DESC";
	$result = mysql_query($sql, $db);
	$output = "\n\n\033[1;37mRecent Happenings\033[22;32m....\033[0m\n";
	$output .= "\033[32m                                      -=-=-=-=-=-\033[0m\n";
	while ( $line = mysql_fetch_array($result) ) {
		$output .= "    " . func_colorcode($line['data']);
		$output .= "\n\033[32m                                      -=-=-=-=-=-\033[0m\n";
	}
	$output .= ( $noprmpt ) ? "" : "\n\033[32m(\033[1;35mC\033[22;32m)ontinue  \033[32m(\033[1;35mT\033[22;32m)odays happenings again  \033[1;32m[\033[35mC\033[32m] \033[22m:-: ";
	return $output;
}

function module_who() {
	GLOBAL $db, $MYSQL_PREFIX, $classes;
	$sql = "SELECT o.userid, fullname, exp, level, class FROM {$MYSQL_PREFIX}users u, {$MYSQL_PREFIX}online o, {$MYSQL_PREFIX}stats s WHERE o.userid = u.userid AND o.userid = s.userid ORDER BY exp";
        $result = mysql_query($sql, $db);
        $output = "\n\n\033[1;37mPeople Online Now\033[22;32m....\033[0m\n";
        $output .= art_line();
        $output .= "\033[1;32mName" . padnumcol("Name", 20) . "Class" . padnumcol("class", 20);
        $output .= "Experience" . padnumcol("experience", 20) . "Level\033[0m\n";
        while ( $line = mysql_fetch_array($result) ) {
	        $output .= "\033[32m" . $line['fullname'] . padnumcol($line['fullname'], 20) . $classes[$line['class']] . padnumcol($classes[$line['class']], 20);
                $output .= $line['exp'] . padnumcol($line['exp'], 20) . $line['level'] . "\033[0m\n";
	}
	return $output . "\n";
}


function module_list() {
	GLOBAL $db, $MYSQL_PREFIX, $classes;
	$sql = "SELECT u.userid, fullname, exp, level, class FROM {$MYSQL_PREFIX}users u, {$MYSQL_PREFIX}stats s WHERE u.userid = s.userid ORDER BY exp";
        $result = mysql_query($sql, $db);
        $output = "\n\n\033[1;37mWarrior List\033[22;32m....\033[0m\n";
        $output .= art_line();
        $output .= "\033[1;32mName" . padnumcol("Name", 20) . "Class" . padnumcol("class", 20);
        $output .= "Experience" . padnumcol("experience", 20) . "Level\033[0m\n";
        while ( $line = mysql_fetch_array($result) ) {
	        $output .= "\033[32m" . $line['fullname'] . padnumcol($line['fullname'], 20) . $classes[$line['class']] . padnumcol($classes[$line['class']], 20);
                $output .= $line['exp'] . padnumcol($line['exp'], 20) . $line['level'] . "\033[0m\n";
	}
	return $output . "\n";
}

function module_abduls() {
	GLOBAL $db, $MYSQL_PREFIX, $armor, $xprt, $userid, $armorprice, $armorndef, $armordef;
        $quitter = 0;
        while ( !$quitter ) {
 		if ( !$xprt ) { slowecho(art_abdul()); }
		slowecho(menu_abdul());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'B':
				slowecho(art_armbuy());
				slowecho("\n\n\033[32mYour choice? \033[1m:\033[22m-\033[1m:\033[0m ");
				$number = preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN))));
				if ( $number > 0 && $number < 16 ) {
					if ( user_getarmor($userid) > 0 ) { slowecho(func_casebold("\nYou cannot hold 2 sets of Armor!\n", 1)); pauser(); }
					else {
						if ( user_getgold($userid) < $armorprice[$number] ) { slowecho(func_casebold("\nYou do NOT have enough Gold!\n", 1)); pauser(); }
						else {
							if ( user_getdef($userid) < $armorndef[$number] ) { slowecho(func_casebold("\nYou are NOT strong enough for that!\n", 1)); pauser(); }
							else {
								slowecho(func_casebold("\nI'll sell you my Best {$armor[$number]} for {$armorprice[$number]} gold.  OK? ", 2)); 
								$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
								if ( $yesno == "Y" ) {
									user_setarmor($userid, $number);
									user_takegold($userid, $armorprice[$number]);
									user_givedef($userid, $armordef[$number]);
									slowecho(func_casebold("\nPleasure doing business with you!\n", 2));
									pauser();
								} else { slowecho(func_casebold("\nFine then...\n", 2)); pauser(); }
							}
						}
					}
				}
				break;
			case 'S':
				$sellpercent = 50 + rand(1, 10);
				$sellarmor = user_getarmor($userid);
				if ( $sellarmor > 0 ) {
  					$sellprice = ( $sellpercent / 100 ) * $armorprice[$sellarmor];
					slowecho(func_casebold("\nHmm...  I'll buy that {$armor[$sellarmor]} for {$sellprice} gold.  OK? ", 2));
					$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	                	        if ( $yesno == "Y" ) {
						user_setarmor($userid, 0);
						user_givegold($userid, $sellprice);
						user_takedef($userid, $armordef[$sellarmor]);
						slowecho(func_casebold("\nPleasure doing business with you!\n", 2));
						pauser();
	                                } else { slowecho(func_casebold("\nFine then...\n", 2)); }
				} else { slowecho(func_casebold("\nYou have nothing I want!\n", 1)); pauser(); }
				break;
			case '?':
				if ( !$xprt ) { slowecho(art_abdul()); }
				break;
			case 'Y':
				slowecho(module_viewstats($userid));
				pauser();
				break;
			case 'Q':
				$quitter = 1;
				break;
			case 'R':
				$quitter = 1;
				break;
		}
	}
}


	
function module_arthurs() {
	GLOBAL $db, $MYSQL_PREFIX, $weapon, $xprt, $userid, $weaponprice, $weaponnstr, $weaponstr;
        $quitter = 0;
        while ( !$quitter ) {
 		if ( !$xprt ) { slowecho(art_arthur()); }
		slowecho(menu_arthur());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'B':
				slowecho(art_wepbuy());
				slowecho("\n\n\033[32mYour choice? \033[1m:\033[22m-\033[1m:\033[0m ");
				$number = preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN))));
				if ( $number > 0 && $number < 16 ) {
					if ( user_getweapon($userid) > 0 ) { slowecho(func_casebold("\nYou cannot hold 2 weapons!\n", 1)); pauser(); }
					else {
						if ( user_getgold($userid) < $weaponprice[$number] ) { slowecho(func_casebold("\nYou do NOT have enough Gold!\n", 1)); pauser(); }
						else {
							if ( user_getstr($userid) < $weaponnstr[$number] ) { slowecho(func_casebold("\nYou are NOT strong enough for that!\n", 1)); pauser(); }
							else {
								slowecho(func_casebold("\nI'll sell you my Favorite {$weapon[$number]} for {$weaponprice[$number]} gold.  OK? ", 2)); 
								$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
								if ( $yesno == "Y" ) {
									user_setweapon($userid, $number);
									user_takegold($userid, $weaponprice[$number]);
									user_givestr($userid, $weaponstr[$number]);
									slowecho(func_casebold("\nPleasure doing business with you!\n", 2));
									pauser();
								} else { slowecho(func_casebold("\nFine then...\n", 2)); pauser(); }
							}
						}
					}
				}
				break;
			case 'S':
				$sellpercent = 50 + rand(1, 10);
				$sellweapon = user_getweapon($userid);
				if ( $sellweapon > 0 ) {
  					$sellprice = ( $sellpercent / 100 ) * $weaponprice[$sellweapon];
					slowecho(func_casebold("\nHmm...  I'll buy that {$armor[$sellweapon]} for {$sellprice} gold.  OK? ", 2));
					$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	                	        if ( $yesno == "Y" ) {
						user_setweapon($userid, 0);
						user_givegold($userid, $sellprice);
						user_takestr($userid, $weaponstr[$sellweapon]);
						slowecho(func_casebold("\nPleasure doing business with you!\n", 2));
						pauser();
	                                } else { slowecho(func_casebold("\nFine then...\n", 2)); }
				} else { slowecho(func_casebold("\nYou have nothing I want!\n", 1)); pauser(); }
				break;
			case '?':
				if ( !$xprt ) { slowecho(art_weapon()); }
				break;
			case 'Y':
				slowecho(module_viewstats($userid));
				pauser();
				break;
			case 'Q':
				$quitter = 1;
				break;
			case 'R':
				$quitter = 1;
				break;
		}
	}
}

?>
