#!/usr/bin/python
""" Red Dragon Inn
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage """
import random
from functions import *

def rdi_menu_main(art, user):
	""" Main Menu """
	thismenu  = "\r\n\r\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mThe Inn\x1b[0m\r\n"
	thismenu += art.blueline();
	thismenu += "\x1b[32m  You enter the inn and are immediately hailed by several of the patrons.\x1b[0m\r\n"
	thismenu += "\x1b[32m  You respond with a wave and scan the room.  The room is filled with\x1b[0m\r\n"
	thismenu += "\x1b[32m  smoke from the torches that line the walls.  Oaken tables and chairs\x1b[0m\r\n"
	thismenu += "\x1b[32m  are scattered across the room.  You smile as the well-rounded Violet\x1b[0m\r\n"
	thismenu += "\x1b[32m  brushes by you....\x1b[0m\r\n\r\n"
	thismenu += func_menu_2col("(C)onverse with the patrons", "(D)aily News", 5, 5)
	if ( user.getSex() == 1 ):
		flirtwith = "Violet"
	else:
		flirtwith = "Seth Able"
	thismenu += menu_2col("(F)lirt with "+flirtwith, "(T)alk to the Bartender", 5, 5)
	thismenu += menu_2col("(G)et a Room", "(V)iew Your Stats", 5, 5)
	thismenu += menu_2col("(H)ear Seth Able The Bard", "(M)ake Announcment", 5, 5)
	thismenu += menu_2col("(R)eturn To Town", "", 5, 5)
	return thismenu

def rdi_prompt(user):
	""" User Prompt"""
	ptime = func_maketime(user)
	thismenu  = "\r\n  \x1b[1;35mThe Red Dragon Inn\x1b[0m\x1b[1;30m (? for menu)\x1b[0m\r\n"
	thismenu += "  \x1b[1;30m(C,D,F,T,G,V,H,M,R)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

def rdi_logic(connection, art, user):
	""" Red Dragon Inn, main loop """
	thisQuit = False
	while ( not thisQuit ):
		if (  not user.expert ):
			func_slowecho(connection, rdi_menu_main(art, user))
		func_slowecho(connection, rdi_prompt(user))
		data = connection.recv(2)
		if not data: break
		if ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			connection.send('R')
			thisQuit = True
		if ( data[0] == '?' ):
			connection.send('?')
			if ( user.expert):
				func_slowecho(connection, rdi_menu_main(art, user))
		if ( data[0] == 'd' or data[0] == 'D' ):
			connection.send('D')
			func_slowecho(connection, module_dailyhappen(True, user.db, user.thisSord.sqlPrefix()))
			func_pauser(connection)
		if ( data[0] == 't' or data[0] == 'T' ):
			connection.send('T')
			rdi_bartend(connection, art, user)
		if ( data[0] == 'v' or data[0] == 'V' ):
			connection.send('V')
			func_slowecho(connection, module_viewstats(art, user))
			func_pauser(connection)
		if ( data[0] == 'm' or data[0] == 'M' ):
			connection.send('M')
			msg_announce(connection, user)
		if ( data[0] == 'f' or data[0] == 'F' ):
			connection.send('F')
			if ( user.didFlirt() ):
				func_slowecho(connection, func_casebold("\r\n  You have already flirted once today\r\n", 2))
			else:
				rdi_flirt(connection, user)
			func_pauser(connection)
		if ( data[0] == 'c' or data[0] == 'C' ):
			connection.send('C')
			rdi_converse(connection, user)
		if ( data[0] == 'h' or data[0] == 'H' ):
			connection.send('H')
			rdi_menu_bard(connection, art, user)
		if ( data[0] == 'g' or data[0] == 'G' ):
			connection.send('G')
			rdi_getroom(connection, user)

def rdi_getroom(connection, user):
	""" Red Dragon Inn Get a Room """
	price = user.getLevel() * 400
	func_slowecho(connection, "\r\n  \x1b[32mThe bartender approaches you at the mention of a room.\x1b[0m\r\n")
	func_slowecho(connection, "  \x1b[35m\"You want a room, eh?  That'll be "+price+" gold!\"\x1b[0m\r\n")
	func_slowecho(connection, "  \x1b[32mDo you agree? \x1b[1m: \x1b[0m")
	yesno = connection.recv(2)
	if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
		if ( user.getGold() < price ):
			func_slowecho(connection, "\r\n  \x1b[35m\"How bout you find yourself a nice stretch of cardboard box ya bum?\x1b[0m\r\n")
		else:
			user.updateGold(price * -1)
			thisSQL = "UPDATE "+user.thisSord.sqlPrefix()+"stats SET atinn = 1 WHERE userid = "+str(user.thisUserID)
			user.db.execute(thisSQL)
			user.logout()
			connection.close()
			thread.exit()
	else:
		func_slowecho(connection, "\r\n  \x1b[35m\"Suit yourself...\"\x1b[0m\r\n")

def rdi_converse(connection, user):
	""" Converse with patrons """
	thisSQL = "SELECT data, nombre FROM (SELECT * FROM "+user.thisSord.sqlPrefix()+"patrons ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id"
	output  = "\r\n\r\n  \x1b[1;37mConverse with the Patrons\x1b[22;32m....\x1b[0m\r\n"
	output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	user.db.execute(thisSQL)
	for (nombre, data) in user.db.fetchall():
		output += "    \x1b[32m"+nombre+" \x1b[1;37msays... \x1b[0m\x1b[32m" + func_colorcode(data)
		output += "\x1b[0m\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	output += "\r\n  \x1b[32mAdd to the conversation? \x1b[1m: \x1b[0m"
	func_slowecho(connection, output)
	yesno = connection.recv(2)
	if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
		func_slowecho(connection, func_casebold("\r\n  What say you? :-: ", 2))
		ann = func_getLine(connection, True)
		safeann = user.dbc.escape_string(ann)
		thisSQL = "INSERT INTO "+user.thisSord.sqlPrefix()+"patrons ( `data`, `nombre` ) VALUES ('"+safeann+"', '"+user.thisFullname+"')"
		user.db.execute(thisSQL)
		func_slowecho(connection, func_casebold("\r\n  Wisdom added!\r\n", 2))
		func_pauser(connection)

def rdi_menu_bard(connection, art, user):
	""" Talk with the bard """
	ptime = func_maketime(user)
	thismenu  = "\r\n\r\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mSeth Able\x1b[0m\n"
	thismenu += art.blueline()
	thismenu += "  \x1b[32mYou stumble over to a dank corner of the Inn.\n  Seth able looks at you expectantly...\r\n\r\n"
	thismenu += func_normmenu("(A)sk Seth Able to Sing")
	thismenu += func_normmenu("(R)eturn to the Inn")
	thismenu += "\r\n  \x1b[1;35mSeth Able the Bard\x1b[0m\x1b[1;30m (A,R,Q) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	thisQuit = False
	while ( not thisQuit ):
		func_slowecho(connection, thismenu)
		data = connection.recv(2)
		if not data: break
		if ( data[0] == 'r' or data[0] == 'R' or data[0] == 'q' or data[0] == 'Q' ):
			connection.send('R')
			thisQuit = True
		if ( data[0] == 'a' or data[0] == 'A' ):
			rdi_hearbard(connection, user)

def rdi_hearbard(connection, user):
	""" Hear the bard sing"""
	if ( not user.didBard() ):
		func_slowecho(connection, "\r\n  \x1b[32mSeth thinks for a moment, picks up his lute, and begins...\r\n\r\n")
		songnum = random.randint(1, 10)
		for lyrics in thebard[songnum][0]:
			sleep(1);
			re.sub("\{(\d+)\}", "\x1b[" + r"\1" + "m" , text)
			lyrics = re.sub("\.\.\.\"", "\x1b[37m...\"\x1b[32m", lyrics)
			lyrics = re.sub("\"\.\.\.", "\x1b[37m\"...\x1b[0m", lyrics)
			lyrics = re.sub("XX", "\x1b[1m"+user.thisFullname+"\x1b[22m", lyrics)
			func_slowecho(connection, lyrics+"\r\n")
		func_slowecho(connection, "\r\n  \x1b[1;32m"+thebard[songnum][1][0]+"\x1b[0m\r\n")
		func_slowecho(connection, "\r\n  \x1b[1;34m"+thebard[songnum][1][1]+"\x1b[0m\r\n\r\n")
		thisSQL = "UPDATE "+user.thisSord.sqlPrefix()+"stats SET "+thebard[songnum][2]+" WHERE userid = "+str(user.thisUserID)
		user.db.execute(thisSQL)
		func_pauser(connection)
	else:
		func_slowecho(connection, func_casebold("\r\n  Seth says:  I'm a bit tired, maybe tommorow...\r\n", 2))

def rdi_flirt(connection, user):
	""" Flirt initiator.  Locked on viloet for now. """
	$sexo = user_getsex($userid);
	slowecho(inn_flirt_menu($sexo));
	slowecho("\n  \x1b[32mYour Choice? \x1b[1m: \x1b[0m ");
	if ( $sexo == 1 ) { inn_flirt_violet(); } else { inn_flirt_seth(); }
}

/** Red Dragon Inn Violet
 * 
 * Flirt with violet the barmaid
 * 
 * @todo Marriage System
 */
function inn_flirt_violet() {
	GLOBAL $userid, $MYSQL_PREFIX, $db;
	$minichoice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	$usercharm = user_getcharm($userid);
	$userlevel = user_getlevel($userid);
	$gexp = 0; $try = 0; $screw;
	switch ($minichoice) {
		case 'W':
			slowecho("\n  \x1b[32mYou pluck up your courage, catch Violet's eye,\n  and seductivly wink...\x1b[0m\n");
			inn_flirt_and(); $try = 1;
			if ( $usercharm > 0 ) {
				$gexp = 5 * $userlevel;
				slowecho("\n  \x1b[1;34mViolet smiles and blushes deeply.\n  Your relationship is taking off!\x1b[0m\n");
				slowecho("  \x1b[32mYou gain \x1b[1m{$gexp}\x1b[22m experience.\x1b[0m\n");
			} else { slowecho("\n  \x1b[1;31mViolet glares back and returns to her work.\n"); }
			break;
		case 'K':
			slowecho("\n  \x1b[32mAs Violet delivers your beer, you grab her hand,\n  pucker up and kiss it...\x1b[0m\n");
			inn_flirt_and(); $try = 1;
			if ( $usercharm > 1 ) {
				$gexp = 10 * $userlevel;
				slowecho("\n  \x1b[1;34mViolet giggles and blushes deeply.\n  Your relationship is taking off!\x1b[0m\n");
				slowecho("  \x1b[32mYou gain \x1b[1m{$gexp}\x1b[22m experience.\x1b[0m\n");
			} else { slowecho("\n  \x1b[1;31mViolet pulls her hand back and slaps you across the face.\n"); }
			break;
		case 'P':
			slowecho("\n  \x1b[32mYou bolt up as Violet takes your hard earned gold,\n  smile, and plant one on her lips...\x1b[0m\n");
			inn_flirt_and(); $try = 1;
			if ( $usercharm > 3 ) {
				$gexp = 20 * $userlevel;
				slowecho("\n  \x1b[1;34mViolet gasps and hurries away.\n  Your relationship is starting to really move now!\x1b[0m\n");
				slowecho("  \x1b[32mYou gain \x1b[1m{$gexp}\x1b[22m experience.\x1b[0m\n");
			} else { slowecho("\n  \x1b[1;31mViolet knees you right in the family gem stones.\n"); }
			break;
		case 'S':
			slowecho("\n  \x1b[32mYou beckon Violet over, and sit her on your lap...\x1b[0m\n");
			inn_flirt_and(); $try = 1;
			if ( $usercharm > 7 ) {
				$gexp = 30 * $userlevel; 
				slowecho("\n  \x1b[1;34mViolet snuggles down for a moment, then hurries back to work.\n  Very smooth ex-lax.\x1b[0m\n");
				slowecho("  \x1b[32mYou gain \x1b[1m{$gexp}\x1b[22m experience.\x1b[0m\n");
			} else { slowecho("\n  \x1b[1;31mViolet grabs a fork from the table and embeds it in your knee.\n"); }
			break;
		case 'G':
			slowecho("\n  \x1b[32mAs you wander the bar, you spot Violet, and firmly caress\n  her glorious behind...\x1b[0m\n");
			inn_flirt_and(); $try = 1;
			if ( $usercharm > 15 ) {
				$gexp = 40 * $userlevel; 
				slowecho("\n  \x1b[1;34mViolet yalps, spins around and gives you a peck on the cheek.\n  Lovely moves son...\x1b[0m\n");
				slowecho("  \x1b[32mYou gain \x1b[1m{$gexp}\x1b[22m experience.\x1b[0m\n");
			} else { slowecho("\n  \x1b[1;31mViolet twists your arm behind your back, dumps a beer on\n  you, and walks away.  Ouch.\n"); }
			break;
		case 'C':
			slowecho("\n  \x1b[32mYou slam your beer down, exclaim 'the hell with it', grab Violet,\n  and head upstairs to the nearest unused room...\x1b[0m\n");
			inn_flirt_and(); $try = 1; 
			if ( $usercharm > 31 ) {
				$gexp = 40 * $userlevel; $screw = 1;
				slowecho("\n  \x1b[1;34mViolet shifts in your arms, revealing that she\n  'forgot' to wear something this morning.\n  Unfortunatally, women's personal uh...  'hygiene' wasn't\n  what it is now in the dark ages.\x1b[0m\n");
				slowecho("  \x1b[32mYou gain \x1b[1m{$gexp}\x1b[22m experience.\x1b[0m\n");
			} else { slowecho("\n  \x1b[1;31mViolet tears off your pants, grabs a knife, and only your 'small stature'\n  prevents a Bobbit incident.  Bummer.\n"); }
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

/** Red Dragon Inn Flirt Pauser
 * 
 * Pause a few seconds during the flirting
 */
function inn_flirt_and() {
	sleep(1); slowecho("\n  \x1b[1;37m..."); sleep(1); slowecho("\x1b[31mAND\x1b[37m"); sleep(1); slowecho("...\x1b[0m");
}

/** Red Dragon Inn Flirt Menu
 * 
 * Shows the choices of ways to flirt
 * 
 * @param int $sexy Player's sex.  1 = male, 2 = female
 * @return string Fully formatted menu
 */
function inn_flirt_menu($sexy) {
	GLOBAL $flirts;
	foreach ( $flirts[$sexy] as $sayings ) {
		$thismenu .= func_normmenu($sayings[1]);
	}
	return $thismenu;
}

/** Red Dragon Inn Bartender Logic
 * 
 * Controls all bartender functions, excpet for get a room
 * 
 * @todo Bribe system
 */
function inn_bartend() {
	GLOBAL $userid, $xprt, $MYSQL_PREFIX, $db;
	$miniquit = 0;
	if ( user_getlevel($userid) == 1 ) {
		slowecho("\n  \x1b[32mNever heard of ya...  Come back when you've done something.\x1b[0m\n");
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
				slowecho("\n  \x1b[35m\"Ya want to know about \x1b[1mViolet\x1b[22m do ya?  She is every warrior's\x1b[0m");
				slowecho("\n  \x1b[35mwet dream...But forget it, Lad, she only goes for the type\x1b[0m");
				slowecho("\n  \x1b[35mof guy who would help old peple...\"\x1b[0m\n");
				pauser();
				break;
			case 'B':
				control_noimp();
				pauser();
				break;
			case 'C':
				slowecho("\n  \x1b[35m\"Ya wanna change your name, eh?  Yeah..\x1b[0m");
				$curname = user_gethandle($userid);
				$curclass = user_getclass($userid);
				$price = user_getlevel($userid) * 500;
				$lnclass = ( $curclass == 1 ) ? "the Death Knight" : (( $curclass == 2 ) ? "the magician" : "the thief");
				slowecho("\n  \x1b[35m{$curname} {$lnclass} does sound kinda funny..\x1b[0m");
				slowecho("\n  \x1b[35mit would cost ya {$price} gold... Deal?\"\x1b[0m");
				slowecho("\n  \x1b[32mChange your name? [\x1b[1mN\x1b[22m]\x1b[0m ");
				$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
				if ( $yesno == "Y" ) { 
					if ( user_getgold($userid) < $price ) { slowecho("\n  \x1b[35m\"Then I suggest you go find some more gold...\"\x1b[0m\n"); 
					} else {
						$nope = 0;
						slowecho("\n  \x1b[32mWhat'll it be? \x1b[1m: \x1b[0m");
						$ann = preg_replace("/\r\n/", "", chop(fgets(STDIN)));
						$insann = mysql_real_escape_string($ann);
						if ( $insann == "" ) { $nope = 1; }
						elseif ( preg_match("/barak/i", $insann) )       { $nope = 1; slowecho("\n  \x1b[31m** \x1b[35mNaw, the real Barak would decapitate you if he found out. \x1b[31m**\x1b[0m\n"); }
						elseif ( preg_match("/seth able/i", $insann) )   { $nope = 1; slowecho("\n  \x1b[31m** \x1b[35mYou are not God! \x1b[31m**\x1b[0m\n"); }
						elseif ( preg_match("/red dragon/i", $insann) )  { $nope = 1; slowecho("\n  \x1b[31m** \x1b[35mOh go plague some other land! \x1b[31m**\x1b[0m\n"); }
						elseif ( preg_match("/seth/i", $insann) )        { $nope = 1; slowecho("\n  \x1b[31m** \x1b[35mYou are not Seth Able!  Don't take his name in vain! \x1b[31m**\x1b[0m\n"); }
						elseif ( preg_match("/turgon/i", $insann) )      { $nope = 1; slowecho("\n  \x1b[31m** \x1b[35mHaw.  Hardly - Turgon has muscles. \x1b[31m**\x1b[0m\n"); }
						elseif ( preg_match("/violet/i", $insann) )      { $nope = 1; slowecho("\n  \x1b[31m** \x1b[35mHaw.  Hardly - Violet has breasts. \x1b[31m**\x1b[0m\n"); }
						elseif ( preg_match("/dragon/i", $insann) )      { $nope = 1; slowecho("\n  \x1b[31m** \x1b[35mYou ain't Bruce Lee, so get out! \x1b[31m**\x1b[0m\n"); }
						elseif ( preg_match("/bartender/i", $insann) )   { $nope = 1; slowecho("\n  \x1b[31m** \x1b[35mNah, the bartender is smarter than you! \x1b[31m**\x1b[0m\n"); }
						elseif ( preg_match("/chance/i", $insann) )      { $nope = 1; slowecho("\n  \x1b[31m** \x1b[35mWhy not go take a chance with a rattlesnake? \x1b[31m**\x1b[0m\n"); } 
						if ( !$nope ) {
							slowecho("\n  \x1b[32mName Changed.\x1b[0m\n");
							$namesql = "UPDATE {$MYSQL_PREFIX}users SET fullname = '{$insname}' WHERE userid = {$userid}";
							$result = mysql_query($namesql, $db);
							user_takegold($userid, $price);
						}
					}
				} else { slowecho("\n  \x1b[35m\"Fine...Keep your stupid name...See if I care...\"\x1b[0m\n"); }
				pauser();
				break;
			case 'D':
				if ( user_getlevel($userid) == 12 ) {
					slowecho("\n  \x1b[32mA \x1b[1;31mRed Dragon\x1b[0m\x1b[32m eh?  Have you tried to \x1b[1mS\x1b[22mearch?\n"); }
				break;
			case 'G':
				slowecho("\n  \x1b[35m\"You have \x1b[1;37mGems\x1b[0m\x1b[35m, eh?  I'll give ya a pint of magic elixer for two.\"\x1b[0m\n");
				slowecho("  \x1b[32mBuy how many elixers? : ");
				$number = preg_replace("/\r\n/", "", strtoupper(chop(fgets(STDIN))));
				if ( $number > 0 ) {
					$usergems = user_getgems($userid);
					if ( ($number * 2) > $usergems ) { slowecho("\n  \x1b[31mYou don't have that many gems!\x1b[0m\n");
					} else { /*sell and process elixer */
						slowecho("\n  \x1b[32mIncrease which stat?\x1b[0m\n");
						slowecho(func_normmenu("(H)itpoints"));
						slowecho(func_normmenu("(S)trength"));
						slowecho(func_normmenu("(V)itality"));
						slowecho(func_normmenu("(N)evermind"));
						$tinyquit = 0;
						while(!$tinyquit) {
							slowecho("  \x1b[32mChoose : \x1b[0m");
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
									slowecho("\n  \x1b[32mYou feel as if your stamina is greater\n");
									$tinyquit = 1;
									break;
								case 'S':
									user_givestr($userid, $number);
									user_takegems($userid, $gemsused);
									slowecho("\n  \x1b[32mYou feel as if your strength is greater\n");
									$tinyquit = 1;
									break;
								case 'V':
									user_givedef($userid, $number);
									user_takegems($userid, $gemsused);
									slowecho("\n  \x1b[32mYou feel as if your vitality is greater\n");
									$tinyquit = 1;
									break;
							}
						}
						slowecho("\n  \x1b[32mPleasure doing business with you\x1b[0m\n");
					}
				}
				break;  
		}
	}
}

/** Red Dragon Inn Bardtender Menu
 * 
 * Show RDI Bartender menu
 */
function inn_bartendmenu() {
	GLOBAL $userid, $logontime;
	$currenttime = time(); $ontime = $currenttime - $logontime;
	$sec = $ontime % 60;
	$min = ( $ontime - $sec ) / 60;
	$psec = ( $sec < 10 ) ? "0{$sec}" : $sec;
	$thismenu  = "\n\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mBartender\x1b[0m\n";
	$thismenu .= art_blueline();
	$thismenu .= "  \x1b[32mThe bartender escorts you into a back\x1b[0m\n";
	$thismenu .= "  \x1b[32mroom.  \x1b[35m\"I have heard yer name before kid...\x1b[0m\n";
	$thismenu .= "  \x1b[35mwhat do ya want to talk about?\"\x1b[0m\n\n";
	$thismenu .= func_normmenu("(V)iolet");
	$thismenu .= func_normmenu("(G)ems");
	$thismenu .= func_normmenu("(B)ribe");
	$thismenu .= func_normmenu("(C)hange your name");
	$thismenu .= func_normmenu("(R)eturn to Bar");
	$thismenu .= "\n  \x1b[35m\"Well?\" \x1b[32mThe bartender inquires. \x1b[1;30m(V,G,B,C,R) (? for menu)\x1b[0m\n";
	$thismenu .= "\n  \x1b[32mYour command, \x1b[1m" . user_gethandle($userid) . "\x1b[22m? \x1b[1;37m[\x1b[22m{$min}:{$psec}\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m";
	return $thismenu;
}

?>"""
