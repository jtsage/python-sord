#!/usr/bin/python
"""
 * Fighting Subsystem.
 * Contains forest fights, events, player fights, leveling up
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage """
 from functions import *
from data import *
from modules import *
from user2 import sorduser

def killer_fight(user, usertokill):
	""" Master Fight System """
	user.pfight -= 1
	thisUserDefense = user.defence
	thisUserHit     = user.str / 2
	ctrlDead = False
	ctrlRan  = False
	ctrlWin  = False
	thisEnemyHit     = usertokill.str / 2
	thisEnemyDefense = usertokill.defence
	thisEnemyWeapon  = weapon[usertokill.weapon]
	
	user.write("\r\n\r\n  \x1b[32m**\x1b[1;37mFIGHT\x1b[0m\x1b[32m**\r\n")
	user.write("\r\n  \x1b[32mYou have encountered "+usertokill.thisFullname+"!!\x1b[0m\r\n")

	skipDisp = False
	while ( user.hp > 0 and usertokill.hp > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
		if ( not skipDisp ):
			user.write(forest_menu(user, usertokill.hp, usertokill.thisFullname))
		skipDisp = False
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 's' or data[0] == 'S' ):
			user.write('S')
			user.write(module_viewstats(user))
		elif ( data[0] == 'a' or data[0] == 'A' ): # Attack!
			user.write("A\r\n")
			hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
			myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) - thisEnemyDefense
			if ( True ): # We Hit First (always)
				if ( myAttack >= usertokill.hp ): # If he's dead, he didn't hit us at all - also, set our attack to zero him
					myAttack = usertokill.hp
					hisAttack = 0
			if ( hisAttack >= user.hp ): # We are dead.  Bummer.
				ctrlDead = True
				hisAttack = user.hp # No insult to injury
			if ( hisAttack > 0 ): # He hit us
				user.write("\r\n  \x1b[32m"+usertokill.thisFullname+" hits you with "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
				user.hp -= hisAttack
			else: 
				user.write("\r\n  \x1b[32m"+usertokill.thisFullname+" misses you completely\x1b[0m\r\n")
			if ( myAttack > 0 and not ctrlDead ): # We hit him!
				user.write("\r\n  \x1b[32mYou hit "+usertokill.thisFullname+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
				usertokill.hp -= myAttack
				if ( usertokill.hp < 1 ): # We Win!
					ctrlWin = True
					user.write("\r\n  \x1b[31m"+usertokill.thisFullname+" lies diead at your feet!\x1b[0m\r\n")
		elif ( data[0] == 'r' or data[0] == 'R' ): # Run Away
			user.write('R')
			if ( random.randint(1, 10) == 4 ): # Hit in the back.
				hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
				if ( hisAttack >= user.hp ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.hp # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  \x1b[32m"+usertokill.thisFullname+" hits you in the back with it's "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\r\n")
					user.hp -= hisAttack
			else:
				user.write("\r\n  \x1b[32mYou narrowly escape harm.\x1b[0m\r\n")
				ctrlRan = True
		elif ( data[0] == 'q' or data[0] == 'Q' ):
			user.write("Q\r\n  \x1b[31mYou are in Combat!  Try Running!\x1b[0m\r\n")
		elif ( data[0] == 'h' or data[0] == 'H' ):
			user.write("H\r\n  \x1b[32mYou are in combat, and they don't make house calls!\x1b[0m\r\n")
		else:
			skipDisp = True

	if ( ctrlWin ) :
		user.pkill += 1
		addExp = usertokill.exp / 2
		delExp = usertokill.exp / 10
		addGems = usertokill.gems / 2
		if ( addGems < 1 ):
			addGems = 0
		else:
			user.gems += addGems
			usertokill.gems -= addGems
		addGold = usertokill.gold
		if ( addGold > 0 ):
			user.gold += addGold
			usertokill.gold -= addGold
		user.exp += addExp
		usertokill.exp -= delExp
		usertokill.alive = 0
		user.write("\r\n  \x1b[32mYou have gained \x1b[1m"+str(addExp)+"\x1b[0;32m experience, \x1b[1m"+str(addGems)+"\x1b[0;32m gems, and \x1b[1m"+str(addGold)+"\x1b[0;32m gold.\x1b[0m\r\n")
		lamentTop = len(killerwin) - 1
		lamentThis = killerwin[random.randint(0, lamentTop)]
		lamentThis = re.sub("`n", "\r\n", lamentThis)
		lamentThis = re.sub("`g", user.thisFullname, lamentThis)
		lamentThis = re.sub("`e", usertokill.thisFullname, lamentThis)
		user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (lamentThis,))
		user.dbcon.commit()
		user.pause()
	if ( ctrlDead ) :
		usertokill.pkill += 1
		usertokill.hp = usertokill.hpmax #Heal the undead other player (he won)
		addExp = user.exp / 2
		delExp = user.exp / 10
		addGems = user.gems / 2
		if ( addGems < 1 ):
			addGems = 0
		else:
			user.gems -= addGems
			usertokill.gems += addGems
		addGold = user.gold
		if ( addGold > 0 ):
			user.gold -= addGold
			usertokill.gold += addGold
		user.exp -= delExp
		usertokill.exp += addExp
		user.alive = 0
		#exception handles, do it later. user.logout()
		lamentTop = len(killerlose) - 1
		lamentThis = killerlose[random.randint(0, lamentTop)]
		lamentThis = re.sub("`n", "\r\n", lamentThis)
		lamentThis = re.sub("`g", user.thisFullname, lamentThis)
		lamentThis = re.sub("`e", usertokill.thisFullname, lamentThis)
		user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (lamentThis,))
		user.dbcon.commit()
		user.write(func_casebold("  Tragically, you died.  Returning to the mundane world for the day...\n", 1))
		raise Exception('normal', "User is DOA.  Bummer.")


def module_killer(user):
	""" Forest Fight - Non-Combat """
	thisQuit = False
	skipDisp = False
	while ( not thisQuit ):
		if ( not skipDisp ):
			if ( not user.expert ):
				user.write(user.art.killer())
			user.write(menu_slaughter(user))
		skipDisp = False
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			user.write('R')
			thisQuit = True
		elif ( data[0] == 'e' or data[0] == 'E' ):
			user.write('E')
			module_dirt(user)
		elif ( data[0] == 'w' or data[0] == 'W' ):
			user.write('W')
			if ( user.pkill > 0 ):
				user.write(func_casebold("\r\n  Carve what in the soft dirt? :-: ", 2))
				ann = func_getLine(user.ntcon, True)
				user.dbcon.execute("INSERT INTO dirt ( `data`, `nombre` ) VALUES ( ?, ? )", (ann, user.thisFullname))
				user.dbcon.commit()
				user.write(func_casebold("\r\n  Carving Added!\r\n", 2))
				user.pause()
			else:
				user.write("\r\n  \x1b[32mYou have to accomplish something here before you can trash talk!\x1b[0m\r\n")
		elif ( data[0] == 'l' or data[0] == 'L' ):
			user.write('L')
			user.write(killer_list(user))
			user.pause()
		elif ( data[0] == 's' or data[0] == 'S' ):
			user.write("S\r\n")
			tokillID = module_finduser(user, "\r\n  \x1b[32mKill Who ?")
			if ( tokillID > 0 ):
				tokillName = user.userGetLogin(tokillID)
				usertoKill = sorduser(tokillName, user.dbcon, user.ntcon, user.art)
				if ( not usertoKill.alive ):
					user.write("\r\n  \x1b[31mAlready dead your holiness...\x1b[0m\r\n")
					user.pause()
				elif ( usertoKill.isOnline() ):
					user.write("\r\n  \x1b[32mThey are online right now!  (and real time player fights are not yet supported.  sorry)\x1b[0m\r\n")
					user.pause()
				else:
					killer_fight(user, usertoKill)
			else:
				user.write("\r\n  \x1b[32mNo user by that name found.\x1b[0m\r\n")
		else:
			skipDisp = True

def killer_list(user):
	""" Player List
	* @return string Formatted output for display """
	db = user.dbcon.cursor()
	db.execute("SELECT u.userid, fullname, exp, level, cls, sex, alive FROM users u, stats s WHERE u.userid = s.userid AND s.atinn = 0 AND u.userid <> ? AND u.userid NOT IN ( SELECT userid FROM online ) ORDER BY exp DESC", (user.thisUserID,))
	output = "\r\n\r\n\x1b[32m    Name                    Experience    Level     Status\x1b[0m\r\n";
	output += user.art.line()
	for line in db.fetchall():
		if ( line[5] == 2 ):
			lineSex = "\x1b[1;35mF\x1b[0m "
		else:
			lineSex = "  "
			
		if ( line[4] == 1 ):
			lineClass = "\x1b[1;31mD \x1b[0m"
		elif ( line[4] == 2 ):
			lineClass = "\x1b[1;31mM \x1b[0m"
		else:
			lineClass = "\x1b[1;31mT \x1b[0m"

		if ( line[6] == 1 ):
			lineStatus = "\x1b[1;32mAlive\x1b[0m"
		else:
			lineStatus = "\x1b[31mDead\x1b[0m"

		output += lineSex + lineClass + "\x1b[32m" + line[1] + padnumcol(str(line[1]), 23) + padright(str(line[2]), 11)
		output += padright(str(line[3]), 6) + "        " + lineStatus + "\r\n"
	db.close()
	return output + "\r\n"
