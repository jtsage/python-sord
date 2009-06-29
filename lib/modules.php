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
		$output .= "\033[32m The {$classes[1]} Skills: \033[1m" . ( $line['spcld'] > 0 ? $line['spcld'] : "NONE" ) . padnumcol(($line['spcld'] > 0 ? $line['spcld'] : "NONE"), 11) . "\033[0m\033[32mUses Today: (\033[1m{$line['used']}\033[22m)\033[0m\n"; }
	if ( $line['class'] == 2 || $line['spclm'] > 0 ) {
		$output .= "\033[32m The {$classes[2]} Skills: \033[1m" . ( $line['spclm'] > 0 ? $line['spclm'] : "NONE" ) . padnumcol(($line['spclm'] > 0 ? $line['spclm'] : "NONE"), 15) . "\033[0m\033[32mUses Today: (\033[1m{$line['usem']}\033[22m)\033[0m\n"; }
	if ( $line['class'] == 3 || $line['spclt'] > 0 ) {
		$output .= "\033[32m The {$classes[3]} Skills: \033[1m" . ( $line['spclt'] > 0 ? $line['spclt'] : "NONE" ) . padnumcol(($line['spclt'] > 0 ? $line['spclt'] : "NONE"), 18) . "\033[0m\033[32mUses Today: (\033[1m{$line['uset']}\033[22m)\033[0m\n"; }
	$output .= "\n \033[1;32mYou are currently interested in \033[37mThe {$classes[$line['class']]} \033[32mskills.\n\n";
	return $output;
}

function module_dailyhappen($noprmpt) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT data FROM {$MYSQL_PREFIX}daily ORDER BY id ASC LIMIT 10";
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
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT o.userid, fullname, DATE_FORMAT(whence, '%H:%i') as whence FROM {$MYSQL_PREFIX}users u, {$MYSQL_PREFIX}online o WHERE o.userid = u.userid ORDER BY whence ASC";
        $result = mysql_query($sql, $db);
        $output = "\n\n\033[1;37m                     Warriors In The Realm Now\033[22;32m\033[0m\n";
        $output .= art_line();
        while ( $line = mysql_fetch_array($result) ) {
	        $output .= "  \033[1;32m" . $line['fullname'] . padnumcol($line['fullname'], 28);
		$output .= "\033[0m\033[32mArrived At                    \033[1;37m" . $line['whence'] . "\033[0m\n";
	}
	return $output . "\n";
}


function module_list() {
	GLOBAL $db, $MYSQL_PREFIX, $classes;
	$sql = "SELECT u.userid, fullname, exp, level, class, spclm, spcld, spclt, sex, alive FROM {$MYSQL_PREFIX}users u, {$MYSQL_PREFIX}stats s WHERE u.userid = s.userid ORDER BY exp DESC";
        $result = mysql_query($sql, $db);
	$output .= "\n\n\033[32m    Name                    Experience    Level    Mastered    Status\033[0m\n";
        $output .= art_line();
        while ( $line = mysql_fetch_array($result) ) {
		$sex = ( $line['sex'] == 2 ) ? "\033[1;35mF\033[0m " : "  ";
		$class = ( $line['class'] == 1 ) ? "\033[1;31mD\033[0m " : (( $line['class'] == 2 ) ? "\033[1;34mM\033[0m " : "\033[1;33mT\033[0m " );
		$master .= ( $line['spcld'] > 39 ) ? "\033[37mD \033[0m" : (( $line['spcld'] > 19 ) ? "\033[1;37mD \033[0m" : "");
		$master .= ( $line['spclm'] > 39 ) ? "\033[37mM \033[0m" : (( $line['spclm'] > 19 ) ? "\033[1;37mM \033[0m" : "");
		$master .= ( $line['spclt'] > 39 ) ? "\033[37mT \033[0m" : (( $line['spclt'] > 19 ) ? "\033[1;37mT \033[0m" : "");
		$masterpad .= ( $line['spcld'] > 19 ) ? "  " : "";
		$masterpad .= ( $line['spclm'] > 19 ) ? "  " : "";
		$masterpad .= ( $line['spclt'] > 19 ) ? "  " : "";
		$exp = number_format($line['exp'], 0);
		$status = ( $line['alive'] == 1 ) ? "\033[1;32mAlive\033[0m" : "\033[31mDead\033[0m";

		$output .= $sex . $class . "\033[32m{$line['fullname']}" . padnumcol($line['fullname'], 23) . padright($exp, 11);
		$output .= padright($line['level'], 6) . "        {$master}" . padnumcol($masterpad, 12) . $status . "\n";
	}
	return $output . "\n";
}

function module_announce() {
	GLOBAL $db, $MYSQL_PREFIX;
	slowecho(func_casebold("\n  Your announcment? :-: ", 2));
	$ann = preg_replace("/\r\n/", "", chop(fgets(STDIN)));
	$insann = mysql_real_escape_string($ann);
	$sql = "INSERT INTO {$MYSQL_PREFIX}daily ( `data` ) VALUES ('{$ann}')";
	$result = mysql_query($sql, $db);
	slowecho(func_casebold("\n  Announcment Made!\n", 2));
	pauser();
}

function module_heal() {
	GLOBAL $userid;
        $quitter = 0;
        while (!$quitter) {
                slowecho(menu_heal());
                $choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                switch ($choice) {
                        case 'Q':
                                $quitter = 1;
                                break;
                        case 'R':
                                $quitter = 1;
                                break;
                        case '?':
                                break;
			case 'H':
				$hptoheal = user_gethpmax($userid) - user_gethp($userid);
				if ( $hptoheal < 1 ) { slowecho(func_casebold("\n  You do not need healing!\n", 2)); 
				} else {
 					$usergold = user_getgold($userid);
					$userlvl = user_getlevel($userid);
					$perhpgold = $userlvl * 5;
					if ( $usergold < ($userlvl * $perhpgold) ) { slowecho(func_casebold("\nYou're poor!\n", 2)); 
					} else {
						$costtoheal = $hptoheal * $perhpgold;
						$userafford = ( $usergold - ( $usergold % $perhpgold ) ) / $perhpgold;
						if ( $userafford > $hptoheal ) { $userafford = $hptoheal; }
						$usercost = $userafford * $perhpgold;
						user_takegold($userid, $usercost);
						user_givehp($userid, $userafford);
						slowecho("\n  \033[32m\033[1m{$userafford} \033[22mHitPoints are healed and you feel much better!\033[0m\n");
						pauser(); $quitter = 1;
					}
				}
				break;
			case 'C':
                                $hptoheal = user_gethpmax($userid) - user_gethp($userid);
                                if ( $hptoheal < 1 ) { slowecho(func_casebold("\n  You do not need healing!\n", 2)); 
				} else {
					slowecho("\n  \033[32mHow much to heal warrior? \033[1m: \033[0m");
					$number = preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN))));
					if ( !is_numeric($number) ) { break; }
					if ( $number > $hptoheal ) { $number = $hptoheal; }
					if ( $number > 0 ) {
						$usergold = user_getgold($userid);
						$userlvl = user_getlevel($userid);
						$perhpgold = $userlvl * 5;
						$costforaction = $perhpgold * $number;
						if ( $costforaction > $usergold ) { slowecho(func_casebold("\n  You do not have enough gold for that!\n", 1));
						} else {
							user_takegold($userid, $costforaction);
							user_givehp($userid, $number);
							slowecho("\n  \033[32m\033[1m{$number} \033[22mHitPoints are healed and you feel much better!\033[0m\n");
							pauser();
						}
					}
				}
				break;

					
		}
	}
}

function module_forest() {
	GLOBAL $userid, $xprt;
        $quitter = 0;
        while (!$quitter) {
                if ( !$xprt ) { slowecho(art_forest()); }
		slowecho(menu_forest());
                $choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                switch ($choice) {
			case 'Q':
				$quitter = 1;
				break;
			case 'R':
				$quitter = 1;
				break;
			case '?':
				if ( $xprt ) { slowecho(art_forest()); }
				break;
			case 'H':
				module_heal();
				break;
			case 'Y':
				module_viewstats($userid);
				break;
			case 'V':
				module_viewstats($userid);
				break;
			case 'L':
				$ffights = user_getffight($userid);
				if ( $ffights > 0 ) {
					$happening = rand(1, 8);
					if ( $happening == 3 ) { forest_special(); }
					else { forest_fight(); }
				} else { slowecho(func_casebold("  You are mighty tired.  Try again tommorow\n", 2)); }
				break;
			case 'A':
				slowecho(func_casebold("  You brandish your weapon dramatically.\n", 2));
				break;
			case 'D':
				slowecho(func_casebold("  Your Death Knight skills cannot help your here.\n", 2));
				break;
                        case 'M':
                                slowecho(func_casebold("  Your Mystical skills cannot help your here.\n", 2));
                                break;
                        case 'T':
                                slowecho(func_casebold("  Your Thieving skills cannot help your here.\n", 2));
                                break;
		}
	}
}


function module_bank() {
	GLOBAL $userid;
        $quitter = 0;
	while (!$quitter) {
		slowecho(menu_bank());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                switch ($choice) {
			case 'Q':
				$quitter = 1;
				break;
			case 'R':
				$quitter = 1;
				break;
			case '?':
				break;
			case 'D':
				slowecho("\n  \033[32mDeposit how much? \033[1;30m(1 for all) \033[1;32m:\033[0m ");
				$number = preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN))));
  				if ( $number > user_getgold($userid) ) { slowecho(func_casebold("\n  You don't have that much gold!\n", 1)); pauser();
				} else {
					if ( $number == 1 ) { $number = user_getgold($userid); }
					user_givebank($userid, $number);
					user_takegold($userid, $number);
					slowecho(func_casebold("\n  Gold deposited\n", 2));
					pauser();
				}
				break;
			case 'W':
                                slowecho("\n  \033[32mWithdraw how much? \033[1;30m(1 for all) \033[1;32m:\033[0m ");
                                $number = preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN))));
                                if ( $number > user_getbank($userid) ) { slowecho(func_casebold("\n  You don't have that much gold!\n", 1)); pauser();
                                } else {
                                        if ( $number == 1 ) { $number = user_getbank($userid); }
                                        user_givegold($userid, $number);
                                        user_takebank($userid, $number);
                                        slowecho(func_casebold("\n  Gold widthdrawn\n", 2));
                                        pauser();
                                }
				break;
			case 'T':
				slowecho("\n  \033[32mTransfer to which player? \033[1;32m:\033[0m ");
				$name = mysql_real_escape_string(preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN)))));
				if ( user_fexist($name) ) {
					$sendto = user_fgetid($name); $sendtofn = user_gethandle($sendto); 
					if ( $sendto == $userid ) { slowecho(func_casebold("\n  You cannot transfer to yourself!\n", 1)); pauser(); 
					} else {
						slowecho("\n  \033[32mDid you mean \033[1m{$sendtofn}\033[0m \033[1;30m(Y/N)\033[0m\033[32m ?\033[0m ");
						$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	        	                        if ( $yesno == "Y" ) {
							slowecho("\n  \033[32mTransfer how much? \033[1;30m(1 for all) \033[1;32m:\033[0m ");
	                		                $number = preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN))));
							if ( $number > user_getgold($userid) ) { slowecho(func_casebold("\n  You don't have that much gold!\n", 1)); pauser();
                                			} else {
		                                        	if ( $number == 1 ) { $number = user_getgold($userid); }
		        	                                user_givegold($sendto, $number);
			                                        user_takegold($userid, $number);
        			                                slowecho(func_casebold("\n  Gold transfered\n", 2));
                			                        pauser();
                        			        }
						}
					}
				} else { slowecho(func_casebold("\n  No User by that name found!\n", 1)); pauser(); }
				break;
		}

	}
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

function module_turgon() {
        GLOBAL $db, $MYSQL_PREFIX, $masters, $userid;
        $quitter = 0;
        while ( !$quitter ) {
                slowecho(menu_turgon());
                $choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                switch ($choice) {
			case 'R':
				$quitter = 1;
				break;
			case '?':
				break;
			case 'Q':
				$ulvl = user_getlevel($userid);
				$uexp = user_getexp($userid);
				$nexp = $masters[$ulvl][2] - $uexp;
				if ( $nexp < 0 ) { $nexp = 0; }
				foreach ( $masters[$ulvl][3] as $wisdom ) {
					slowecho("\n  \033[32m{$wisdom}\033[0m");
				}
				slowecho("\n\n  \033[1;37m{$masters[$ulvl][0]}\033[0m\033[32m looks at you closely and says...\n");
				if ( $nexp == 0 ) { slowecho("  \033[32m{$masters[$ulvl][4]}\033[0m\n"); }
				else { slowecho("  \033[32mYou need about \033[1;37m{$nexp}\033[0m\033[32m experience before you'll be as good as me.\033[0m\n"); }
				pauser();
				break;
			case 'V':
				control_noimp();
				break;
			case 'Y':
				slowecho(module_viewstats($userid));
				break;
			case 'A':
				master_fight();
				break;

		}
	}
}
?>
