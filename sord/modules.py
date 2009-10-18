#!/usr/bin/python
"""
 * Module System
 * 
 * Contains modules for everything except the Inn and the Fighting system.
 * 
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage
"""

""" View Player Stats
 * 
 * View current player's stats.
 * 
 * @param int $userid User ID
 * @return string Formatted output for display
 */
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

/** View Daily Happenings
 * 
 * View the daily happenings
 * 
 * @param bool $noprmpt Do not prompt for additions.
 * @return string Formatted output for display
 */
function module_dailyhappen($noprmpt) {
	GLOBAL $db, $MYSQL_PREFIX;
	$sql = "SELECT data FROM (SELECT * FROM {$MYSQL_PREFIX}daily ORDER BY id DESC LIMIT 10) AS tbl ORDER BY tbl.id";
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

/** Who's Online
 * 
 * Show current users online
 * 
 * @return string Formatted output for display
 */
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
}"""
from functions import *
""" Player List
 * List all players
 * 
 * @return string Formatted output for display """
def module_list(art, db, prefix):
	thisSQL = "SELECT u.userid, fullname, exp, level, class, spclm, spcld, spclt, sex, alive FROM "+prefix+"users u, "+prefix+"stats s WHERE u.userid = s.userid ORDER BY exp DESC"
	db.execute(thisSQL)
	output = "\r\n\r\n\x1b[32m    Name                    Experience    Level    Mastered    Status\x1b[0m\r\n";
	output += art.line()
	for line in db.fetchall():
		if ( line[8] == 2 ):
			lineSex = "\x1b[1;35mF\x1b[0m "
		else:
			lineSex = "  "
			
		if ( line[4] == 1 ):
			lineClass = "\x1b[1;31mD \x1b[0m"
		elif ( line[4] == 2 ):
			lineClass = "\x1b[1;31mM \x1b[0m"
		else:
			lineClass = "\x1b[1;31mT \x1b[0m"
		
		lineMaster = ""
		if ( line[6] > 19 ):
			if ( line[6] > 39 ):
				lineMaster += "\x1b[1;37mD \x1b[0m"
			else:
				lineMaster += "\x1b[37mD \x1b[0m"
		else:
			lineMaster += "  "
			
		if ( line[5] > 19 ):
			if ( line[5] > 39 ):
				lineMaster += "\x1b[1;37mM \x1b[0m"
			else:
				lineMaster += "\x1b[37mM \x1b[0m"
		else:
			lineMaster += "  "
						
		if ( line[7] > 19 ):
			if ( line[7] > 39 ):
				lineMaster += "\x1b[1;37mT \x1b[0m"
			else:
				lineMaster += "\x1b[37mT \x1b[0m"
		else:
			lineMaster += "  "
									
		
		if ( line[9] == 1 ):
			lineStatus = "\x1b[1;32mAlive\x1b[0m"
		else:
			lineStatus = "\x1b[31mDead\x1b[0m"
			
		output += lineSex + lineClass + "\x1b[32m" + line[1] + padnumcol(str(line[1]), 23) + padright(str(line[2]), 11)
		output += padright(str(line[3]), 6) + "        " + lineMaster + padnumcol(lineMaster, 12) + lineStatus + "\r\n"
	return output + "\r\n"

"""
/** Make announcment
 * 
 * Make an announcment in the daily happenings.
 */
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

/** Healers Hut Logic
 * 
 * Visit and use the healers hut
 */
function module_heal() {
	GLOBAL $userid;
	$quitter = 0;
	while (!$quitter) {
		slowecho(menu_heal());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'Q': // QUIT
				$quitter = 1; break;
			case 'R': // QUIT
				$quitter = 1; break;
			case '?': // SHOW MENU
				break;
			case 'H': // HEAL ALL POSSIBLE
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
			case 'C': // HEAL CERTAIN AMOUNT
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

/** Forest Fight Menu (non-combat)
 * 
 * Visit the forest
 */
function module_forest() {
	GLOBAL $userid, $xprt;
	$quitter = 0;
	while (!$quitter) {
		if ( !$xprt ) { slowecho(art_forest()); }
		slowecho(menu_forest());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'Q': // QUIT
				$quitter = 1; break;
			case 'R': // QUIT
				$quitter = 1; break;
			case '?': // SHOW MENU
				if ( $xprt ) { slowecho(art_forest()); } break;
			case 'H': // HEALERS HUT
				module_heal(); break;
			case 'Y': // VIEW STATS
				module_viewstats($userid); break;
			case 'V': // VIEW STATS
				module_viewstats($userid); break;
			case 'L': // LOOK FOR SOMETHING TO KILL
				$ffights = user_getffight($userid);
				if ( $ffights > 0 ) {
					$happening = rand(1, 8);
					if ( $happening == 3 ) { forest_special(); }
					else { forest_fight(); }
				} else { slowecho(func_casebold("  You are mighty tired.  Try again tommorow\n", 2)); }
				break;
			case 'A': // ATTACK NOTHING
				slowecho(func_casebold("  You brandish your weapon dramatically.\n", 2)); break;
			case 'D': // SPECIAL ATTACK NOTHING
				slowecho(func_casebold("  Your Death Knight skills cannot help your here.\n", 2)); break;
			case 'M': // SPECIAL ATTACK NOTHING
				slowecho(func_casebold("  Your Mystical skills cannot help your here.\n", 2)); break;
			case 'T': // SPECIAL ATTACK NOTHING
				slowecho(func_casebold("  Your Thieving skills cannot help your here.\n", 2)); break;
		}
	}
}

/** Ye Olde Bank
 * 
 * Visit the bank
 */
function module_bank() {
	GLOBAL $userid;
	$quitter = 0;
	while (!$quitter) {
		slowecho(menu_bank());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'Q': // QUIT
				$quitter = 1; break;
			case 'R': // QUIT
				$quitter = 1; break;
			case '?': // SHOW MENU
				break;
			case 'D': // DEPOSIT
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
			case 'W': // WITHDRAWL
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
			case 'T': // TRANSFER
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

/** Abdul's Armor
 * 
 * Visit the armory
 */
function module_abduls() {
	GLOBAL $db, $MYSQL_PREFIX, $armor, $xprt, $userid, $armorprice, $armorndef, $armordef;
	$quitter = 0;
	while ( !$quitter ) {
 		if ( !$xprt ) { slowecho(art_abdul()); }
		slowecho(menu_abdul());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'B': // BUY ARMOR
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
			case 'S': // SELL ARMOR
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
			case '?': // SHOW MENU
				if ( !$xprt ) { slowecho(art_abdul()); } break;
			case 'Y': // VIEW STATS
				slowecho(module_viewstats($userid)); pauser(); break;
			case 'Q': // QUIT
				$quitter = 1; break;
			case 'R': // QUIT
				$quitter = 1; break;
		}
	}
}

/** King Arthur's Weapons
 * 
 * Visit the weaponry
 */
function module_arthurs() {
	GLOBAL $db, $MYSQL_PREFIX, $weapon, $xprt, $userid, $weaponprice, $weaponnstr, $weaponstr;
	$quitter = 0;
	while ( !$quitter ) {
 		if ( !$xprt ) { slowecho(art_arthur()); }
		slowecho(menu_arthur());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'B': // BUY WEAPON
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
			case 'S': // SELL WEAPON
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
			case '?': // SHOW MENU
				if ( !$xprt ) { slowecho(art_weapon()); } break;
			case 'Y': // VIEW STATS
				slowecho(module_viewstats($userid)); pauser(); break;
			case 'Q': // QUIT
				$quitter = 1; break;
			case 'R': // QUIT
				$quitter = 1; break;
		}
	}
}

/** Turgon's Warrior Training (pre-combat)
 * 
 * Visit the master
 * 
 * @todo Implement the hall of honor (V)
 */
function module_turgon() {
	GLOBAL $db, $MYSQL_PREFIX, $masters, $userid;
	$quitter = 0;
	while ( !$quitter ) {
		slowecho(menu_turgon());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'R': // QUIT
				$quitter = 1; break;
			case '?': // SHOW MENU
				break;
			case 'Q': // QUESTION MASTER
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
			case 'V': // VIEW HALL OF HONOR
				control_noimp(); break;
			case 'Y': // VIEW STATS
				slowecho(module_viewstats($userid)); break;
			case 'A': // FIGHT MASTER
				if ( user_seenmaster($userid) ) { slowecho("\n\n  \033[32mI'm sorry my son, you may only fight me once per game-day\033[0m\n"); }
				else { master_fight(); }
				break;
		}
	}
}

/** Look at the forest flowers
 * 
 * Yet another in-game message board.
 *
 * @todo random sayings generator for this section
 */
function module_flowers() {
	GLOBAL $db, $MYSQL_PREFIX, $userid;
	$sql = "SELECT data, nombre FROM (SELECT * FROM {$MYSQL_PREFIX}flowers ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id";
	$result = mysql_query($sql, $db);
	$output = "\n\n  \033[1;37mStudy the forest flowers\033[22;32m....\033[0m\n";
	$output .= "\033[32m                                      -=-=-=-=-=-\033[0m\n";
	while ( $line = mysql_fetch_array($result) ) {
		$output .= "    \033[32m{$line['nombre']} \033[1;37msays... \033[0m\033[32m" . func_colorcode($line['data']);
		$output .= "\033[0m\n\033[32m                                      -=-=-=-=-=-\033[0m\n";
	}
	$output .= "\n  \033[32mAdd to the conversation? \033[1m: \033[0m";
	slowecho($output);
	$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	if ( $yesno == "Y" ) {
		slowecho(func_casebold("\n  What!?  What do you want? :-: ", 2));
		$ann = preg_replace("/\r\n/", "", chop(fgets(STDIN)));
		$insann = mysql_real_escape_string($ann);
		$insnme = user_gethandle($userid);
		$sql = "INSERT INTO {$MYSQL_PREFIX}flowers ( `data`, `nombre` ) VALUES ('{$insann}', '{$insnme}')";
		$result = mysql_query($sql, $db);
		slowecho(func_casebold("\n  Idiocy added!\n", 2));
		pauser();
	}
}
"""

