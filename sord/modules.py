#!/usr/bin/python
import random
from functions import *
from data import *
from menus import *
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
 * @param int $userid User ID
 * @return string Formatted output for display"""
def module_viewstats(art, user):
	output  = "\r\n\r\n\x1b[1m\x1b[37m"+user.thisFullname+"\x1b[0m\x1b[32m's Stats...\r\n"
	output += art.line()
	output += "\x1b[32m Experience    : \x1b[1m"+str(user.getExperience())+"\x1b[0m\r\n"
	output += "\x1b[32m Level         : \x1b[1m"+str(user.getLevel())+"\x1b[0m" + padnumcol(str(user.getLevel()), 20) + "\x1b[32mHitPoints          : \x1b[1m"+str(user.getHP())+" \x1b[22mof\x1b[1m "+str(user.getHPMax())+"\x1b[0m\r\n"
	output += "\x1b[32m Forest Fights : \x1b[1m"+str(user.getForestFight())+"\x1b[0m" + padnumcol(str(user.getForestFight()), 20) + "\x1b[32mPlayer Fights Left : \x1b[1m"+str(user.getPlayerFight())+"\x1b[0m\r\n"
	output += "\x1b[32m Gold In Hand  : \x1b[1m"+str(user.getGold())+"\x1b[0m" + padnumcol(str(user.getGold()), 20) + "\x1b[32mGold In Bank       : \x1b[1m"+str(user.getBank())+"\x1b[0m\r\n"
	output += "\x1b[32m Weapon        : \x1b[1m"+weapon[user.getWeapon()]+"\x1b[0m" + padnumcol(weapon[user.getWeapon()], 20) + "\x1b[32mAttack Strength    : \x1b[1m"+str(user.getStrength())+"\x1b[0m\r\n"
	output += "\x1b[32m Armor         : \x1b[1m"+armor[user.getArmor()]+"\x1b[0m" + padnumcol(armor[user.getArmor()], 20) + "\x1b[32mDefensive Strength : \x1b[1m"+str(user.getDefense())+"\x1b[0m\r\n"
	output += "\x1b[32m Charm         : \x1b[1m"+str(user.getCharm())+"\x1b[0m" + padnumcol(str(user.getCharm()), 20) + "\x1b[32mGems               : \x1b[1m"+str(user.getGems())+"\x1b[0m\r\n\r\n"
	for skillnum in [1,2,3]:
		if ( user.getClass() == skillnum or user.getSkillPoint(skillnum) > 0 ):
			output += "\x1b[32m The "+classes[skillnum]+" Skills: \x1b[1m"
			if ( user.getSkillUse(skillnum) > 0 ):
				output +=  str(user.getSkillPoint(skillnum)) + padnumcol(str(user.getSkillPoint(skillnum)), 11)
			else:
				output += "NONE     "
			output += padnumcol(classes[skillnum], 12)
			output += "\x1b[0m\x1b[32mUses Today: (\x1b[1m"+str(user.getSkillUse(skillnum))+"\x1b[22m)\x1b[0m\r\n"
	output += "\r\n \x1b[1;32mYou are currently interested in \x1b[37mThe "+classes[user.getClass()]+" \x1b[32mskills.\r\n\r\n";
	return output

""" View Daily Happenings
 * @param bool $noprmpt Do not prompt for additions.
 * @return string Formatted output for display """
def module_dailyhappen(noprmpt, db, prefix):
	thisSQL = "SELECT data FROM (SELECT * FROM "+prefix+"daily ORDER BY id DESC LIMIT 10) AS tbl ORDER BY tbl.id"
	db.execute(thisSQL)
	output  = "\r\n\r\n\x1b[1;37mRecent Happenings\033[22;32m....\x1b[0m\r\n"
	output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	for line in db.fetchall():
		output += "    " + func_colorcode(line[0])
		output += "\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	if ( not noprmpt ) :
		output +=  "\n\x1b[32m(\x1b[1;35mC\x1b[22;32m)ontinue  \x1b[32m(\x1b[1;35mT\x1b[22;32m)odays happenings again  \x1b[1;32m[\x1b[35mC\x1b[32m] \x1b[22m:-: "
	return output


""" Who's Online
 * @return string Formatted output for display"""
def module_who(art, db, prefix):
	thisSQL = "SELECT o.userid, fullname, DATE_FORMAT(whence, '%H:%i') as whence FROM "+prefix+"users u, "+prefix+"online o WHERE o.userid = u.userid ORDER BY whence ASC"
	db.execute(thisSQL)
	output  = "\r\n\r\n\x1b[1;37m                     Warriors In The Realm Now\x1b[22;32m\x1b[0m\r\n"
	output += art.line()
	for line in db.fetchall():
		output += "  \x1b[1;32m" + line[1] + padnumcol(line[1], 28)
		output += "\x1b[0m\x1b[32mArrived At                    \x1b[1;37m" + line[2] + "\x1b[0m\r\n"
	return output + "\r\n"


""" Player List
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

"""
""" Ye Olde Bank """
def module_bank(connection, art, user):
	thisQuit = False
	while ( not thisQuit ):
		func_slowecho(connection, menu_bank(user, art))
		data = connection.recv(2)
		if not data: break
		if ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			connection.send('Q')
			thisQuit = True
		if ( data[0] == 'd' or data[0] == 'D' ):
			connection.send('D')
			func_slowecho(connection, "\r\n  \x1b[32mDeposit how much? \x1b[1;30m(1 for all) \x1b[1;32m:\x1b[0m ")
			number = int(func_getLine(connection, True))
			if ( number > user.getGold() ):
				func_slowecho(func_casebold(connection, "\r\n  You don't have that much gold!\r\n", 1))
				func_pauser(connection)
			else:
				if ( number == 1 ):
					number = user.getGold()
				user.updateBank(number)
				user.updateGold(number * -1)
				func_slowecho(connection, func_casebold("\r\n  Gold deposited\r\n", 2))
				func_pauser(connection)
		if ( data[0] == 'w' or data[0] == 'W' ):
			connection.send('W')
			func_slowecho(connection, "\r\n  \x1b[32mWithdraw how much? \x1b[1;30m(1 for all) \x1b[1;32m:\x1b[0m ")
			number = int(func_getLine(connection, True))
			if ( number > user.getBank() ):
				func_slowecho(connection, func_casebold("\r\n  You don't have that much gold in the bank!\r\n", 1))
				func_pauser(connection)
			else:
				if ( number == 1 ):
					number = user.getBank()
				user.updateGold(number)
				user.updateBank(number * -1)
				func_slowecho(connection, func_casebold("\r\n  Gold widthdrawn\r\n", 2))
				func_pauser(connection)
		if ( data[0] == 't' or data[0] == 'T' ):
			connection.send('T')
			func_slowecho(connection, "\r\n  \x1b[32mSorry, transfers are currently offline.\x1b[0m")
			"""slowecho("\n  \033[32mTransfer to which player? \033[1;32m:\033[0m ");
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
								pauser();	}	}	}
				} else { slowecho(func_casebold("\n  No User by that name found!\n", 1)); pauser(); } """

""" Abdul's Armor"""
def module_abduls(connection, art, user):
	thisQuit = False
	while ( not thisQuit ):
 		if ( not user.expert ):
			func_slowecho(connection, art.abdul())
		func_slowecho(connection, menu_abdul(user))
		data = connection.recv(2)
		if not data: break
		if ( data[0] == 'b' or data[0] == 'B' ):
			connection.send('B')
			func_slowecho(connection, art.armbuy())
			func_slowecho(connection, "\r\n\r\n\x1b[32mYour choice? \x1b[1m:\x1b[22m-\x1b[1m:\x1b[0m ")
			number = int(func_getLine(connection, True))
			if ( number > 0 and number < 16 ):
				if ( user.getArmor() > 0 ):
					func_slowecho(connection, func_casebold("\r\nYou cannot hold 2 sets of Armor!\r\n", 1))
					func_pauser(connection)
				else:
					if ( user.getGold() < armorprice[number] ):
						func_slowecho(connection, func_casebold("\r\nYou do NOT have enough Gold!\n", 1))
						func_pauser(connection)
					else:
						if ( user.getDefense() < armorndef[number] ):
							func_slowecho(connection, func_casebold("\r\nYou are NOT strong enough for that!\r\n", 1))
							func_pauser(connection)
						else:
							func_slowecho(connection, func_casebold("\r\nI'll sell you my Best "+armor[number]+" for "+str(armorprice[number])+" gold.  OK? ", 2)) 
							yesno = connection.recv(2)
							if not yesno: break
							if ( yesno[0] == "Y" or yesno[0] == "y" ):
								connection.send('Y')
								user.setArmor(number)
								user.updateGold(armorprice[number] * -1)
								user.updateDefense(armordef[number])
								func_slowecho(connection, func_casebold("\r\nPleasure doing business with you!\r\n", 2))
								func_pauser(connection)
							else:
								func_slowecho(connection, func_casebold("\r\nFine then...\r\n", 2))
								func_pauser(connection)
		if ( data[0] == 's' or data[0] == 'S' ):
			connection.send('S')
			sellpercent = 50 + random.randint(1, 10)
			sellarmor = user.getArmor()
			if ( sellarmor > 0 ):
				sellprice = ((sellpercent * armorprice[sellarmor]) // 100 )
				func_slowecho(connection, func_casebold("\r\nHmm...  I'll buy that "+armor[sellarmor]+" for "+str(sellprice)+" gold.  OK? ", 2))
				yesno = connection.recv(2)
				if not yesno: break
				if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
					connection.send('Y')
					user.setArmour(0)
					user.updateGold(sellprice)
					unstrength = (60 * armordef[sellweapon]) // 100
					user.updateDefense(unstrength * -1)
					func_slowecho(connection, func_casebold("\r\nPleasure doing business with you!\r\n", 2))
					func_pauser(connection)
				else:
					func_slowecho(connection, func_casebold("\r\nFine then...\r\n", 2))
					func_pauser(connection)
			else:
				func_slowecho(connection, func_casebold("\r\nYou have nothing I want!\r\n", 1))
				func_pauser(connection)
		if ( data[0] == "?" ):
			connection.send('?')
			if ( user.expert ):
				func_slowecho(connection, art.abdul())
		if ( data[0] == 'Y' or data[0] == 'y' ):
			connection.send('Y')
			func_slowecho(connection, module_viewstats(art, user))
			func_pauser(connection)
		if ( data[0] == 'Q' or data[0] == 'q' or data[0] == 'R' or data[0] == 'r' ):
			connection.send('Q')
			thisQuit = True;

"""King Arthur's Weapons"""
def module_arthurs(connection, art, user):
	thisQuit = False
	while ( not thisQuit ):
 		if ( not user.expert ):
			func_slowecho(connection, art.arthur())
		func_slowecho(connection, menu_arthur(user))
		data = connection.recv(2)
		if not data: break
		if ( data[0] == 'b' or data[0] == 'B' ):
			connection.send('B')
			func_slowecho(connection, art.wepbuy())
			func_slowecho(connection, "\r\n\r\n\x1b[32mYour choice? \x1b[1m:\x1b[22m-\x1b[1m:\x1b[0m ")
			number = int(func_getLine(connection, True))
			if ( number > 0 and number < 16 ):
				if ( user.getWeapon() > 0 ):
					func_slowecho(connection, func_casebold("\r\nYou cannot hold 2 Weapons!\r\n", 1))
					func_pauser(connection)
				else:
					if ( user.getGold() < weaponprice[number] ):
						func_slowecho(connection, func_casebold("\r\nYou do NOT have enough Gold!\n", 1))
						func_pauser(connection)
					else:
						if ( user.getStrength() < weaponnstr[number] ):
							func_slowecho(connection, func_casebold("\r\nYou are NOT strong enough for that!\r\n", 1))
							func_pauser(connection)
						else:
							func_slowecho(connection, func_casebold("\r\nI'll sell you my Favorite "+weapon[number]+" for "+str(weaponprice[number])+" gold.  OK? ", 2)) 
							yesno = connection.recv(2)
							if not yesno: break
							if ( yesno[0] == "Y" or yesno[0] == "y" ):
								connection.send('Y')
								user.setWeapon(number)
								user.updateGold(weaponprice[number] * -1)
								user.updateStrength(weaponstr[number])
								func_slowecho(connection, func_casebold("\r\nPleasure doing business with you!\r\n", 2))
								func_pauser(connection)
							else:
								func_slowecho(connection, func_casebold("\r\nFine then...\r\n", 2))
								func_pauser(connection)
		if ( data[0] == 's' or data[0] == 'S' ):
			connection.send('S')
			sellpercent = 50 + random.randint(1, 10)
			sellweapon = user.getWeapon()
			if ( sellweapon > 0 ):
				sellprice = ((sellpercent * weaponprice[sellweapon]) // 100 )
				func_slowecho(connection, func_casebold("\r\nHmm...  I'll buy that "+weapon[sellweapon]+" for "+str(sellprice)+" gold.  OK? ", 2))
				yesno = connection.recv(2)
				if not yesno: break
				if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
					connection.send('Y')
					user.setWeapon(0)
					user.updateGold(sellprice)
					unstrength = (60 * weaponstr[sellweapon]) // 100
					user.updateStrength(unstrength * -1)
					func_slowecho(connection, func_casebold("\r\nPleasure doing business with you!\r\n", 2))
					func_pauser(connection)
				else:
					func_slowecho(connection, func_casebold("\r\nFine then...\r\n", 2))
					func_pauser(connection)
			else:
				func_slowecho(connection, func_casebold("\r\nYou have nothing I want!\r\n", 1))
				func_pauser(connection)
		if ( data[0] == "?" ):
			connection.send('?')
			if ( user.expert ):
				func_slowecho(connection, art.abdul())
		if ( data[0] == 'Y' or data[0] == 'y' ):
			connection.send('Y')
			func_slowecho(connection, module_viewstats(art, user))
			func_pauser(connection)
		if ( data[0] == 'Q' or data[0] == 'q' or data[0] == 'R' or data[0] == 'r' ):
			connection.send('Q')
			thisQuit = True;
				

"""

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

