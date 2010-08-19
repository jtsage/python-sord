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

def module_turgon(user):
	""" Visit the master """
	thisQuit = False
	skipDisp = False
	while ( not thisQuit ):
		if ( not skipDisp ):
			if ( not user.expert ):
				user.write(user.art.turgon())
			user.write(menu_turgon(user))
		skipDisp = False
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 'r' or data[0] == 'R' ):
			user.write('R')
			thisQuit = True
		elif ( data[0] == '?' ):
			user.write("?\r\n")
		elif ( data[0] == 'q' or data[0] == 'Q' ):
			user.write("Q\r\n")
			if ( user.level < 12 ):
				thisUserLevel = user.level
				thisUserExp   = user.exp
				thisNeedExp   = masters[thisUserLevel][2] - thisUserExp
				for thisWisdom in masters[thisUserLevel][3]:
					user.write("\r\n  \x1b[32m"+thisWisdom+"\x1b[0m")
				user.write("\r\n\r\n  \x1b[1;37m"+masters[thisUserLevel][0]+"\x1b[0;32m looks at you closely and says...\r\n")
				if ( thisNeedExp < 1 ):
					user.write("\r\n  \x1b[32m"+masters[thisUserLevel][4]+"\x1b[0m\r\n")
				else:
					user.write("\r\n  \x1b[32mYou need about \x1b[1;37m"+str(thisNeedExp)+"\x1b[0;32m experience before you'll be as good as me.\x1b[0m\r\n")
			else:
				user.write("\r\n  \x1b[32mYou have learned all that you can.  This place holds nothing more for you!\x1b[0m\r\n")
			user.pause()
		elif ( data[0] == 'v' or data[0] == 'V' ):
			user.write('V')
			db = user.dbcon.cursor()
			db.execute("SELECT fullname, dkill FROM users u, stats s WHERE s.userid = u.userid AND s.dkill > 0 ORDER by s.dkill DESC")
			user.write("\r\n\r\n  \x1b[32mUsers who have slain the dragon:\x1b[0m\r\n")
			for row in db.fetchall():
				if not row:
					user.write("\r\n\r\n  \x1b[32mWhat a sad thing - there are no heroes in this realm.\x1b[0m\r\n")
					break
				else:
					for (nombre, data) in row:
						user.write("  \x1b[32m"+nombre+padnumcol(nombre, 25)+"\x1b[1m"+str(data)+"\x1b[0m\r\n")
			user.write("\r\n")
			db.close()
			user.pause()
		elif ( data[0] == 'y' or data[0] == 'Y' ):
			user.write('Y')
			user.write(module_viewstats(user))
			user.pause()
		elif ( data[0] == 'a' or data[0] == 'A' ):
			user.write('A')
			if ( user.level > 11 ):
				user.write("\r\n\r\n  \x1b[32mThere is no master for you to attack stoopid!\x1b[0m\r\n")
			elif ( user.master ):
				user.write("\r\n\r\n  \x1b[32mI'm sorry my son, you may only fight me once per game-day\x1b[0m\r\n")
			else:
				master_fight(user)
		else:
			skipDisp = True



def master_fight(user):
	""" Master Fight System """
	thisUserLevel = user.level
	thisTopEnemy  = len(enemies[thisUserLevel]) - 1
	thisUserDefense = user.defence
	thisUserHit     = user.str / 2
	ctrlDead = False
	ctrlRan  = False
	ctrlWin  = False
	thisEnemyHit     = masters[thisUserLevel][7] / 2
	thisEnemyDefense = masters[thisUserLevel][8]
	thisEnemyHP      = masters[thisUserLevel][6]
	thisEnemyName    = masters[thisUserLevel][0]
	thisEnemyWeapon  = masters[thisUserLevel][1]
	
	user.write("\r\n\r\n  \x1b[32m**\x1b[1;37mFIGHT\x1b[0m\x1b[32m**\r\n")
	user.write("\r\n  \x1b[32mYou have encountered "+thisEnemyName+"!!\x1b[0m\r\n")

	skipDisp = False
	while ( user.hp > 0 and thisEnemyHP > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
		if ( not skipDisp ):
			user.write(forest_menu(user, thisEnemyHP, thisEnemyName))
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
			if ( False ): # We Hit First (always)
				if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
					hisAttack = 0
			if ( hisAttack >= user.hp ): # We are dead.  Bummer.
				ctrlDead = True
				hisAttack = user.hp # No insult to injury
			if ( hisAttack > 0 ): # He hit us
				user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
				user.hp -= hisAttack
			else: 
				user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely\x1b[0m\r\n")
			if ( myAttack > 0 and not ctrlDead ): # We hit him!
				user.write("\r\n  \x1b[32mYou hit "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
				thisEnemyHP = thisEnemyHP - myAttack
				if ( thisEnemyHP < 1 ): # We Win!
					ctrlWin = True
					user.write("\r\n  \x1b[31m"+masters[thisUserLevel][5]+"\x1b[0m\r\n")
		elif ( data[0] == 'r' or data[0] == 'R' ): # Run Away
			user.write("\r\n  \x1b[32mYou retire from the field before getting yourself killed.\x1b[0m\r\n")
			user.hp = user.hpmax
			user.master = 1
			ctrlRan = True
		elif ( data[0] == 'q' or data[0] == 'Q' ):
			user.write("\r\n  \x1b[31mYou are in Combat!  Try Running!\x1b[0m\r\n")
		elif ( data[0] == 'h' or data[0] == 'H' ):
			user.write("\r\n  \x1b[32mYou are in combat, and they don't make house calls!\x1b[0m\r\n")
		else:
			skipDisp = True

	if ( ctrlWin ) :
		addExp = masters[thisUserLevel][2] / 10
		user.exp += addExp
		user.level += 1
		user.defence += masterwin[thisUserLevel][2]
		user.str += masterwin[thisUserLevel][1]
		user.hpmax += masterwin[thisUserLevel][0]
		user.updateSkillPoint(user.cls, 1)
		user.updateSkillUse(user.cls, 1)
		user.hp = user.hpmax
		user.write("\r\n  \x1b[32mYou have receieved \x1b[1m+"+str(masterwin[thisUserLevel][2])+"\x1b[22m vitality, \x1b[1m+"+str(masterwin[thisUserLevel][1])+"\x1b[22m strength, and \x1b[1m+"+str(masterwin[thisUserLevel][0])+"\x1b[22m hitpoints.\x1b[0m\r\n")
		user.write("  \x1b[32mYou have gained \x1b[1m"+str(addExp)+"\x1b[22m experience, and are now level \x1b[1m"+str(user.level)+"\x1b[22m.\x1b[0m\r\n")
		user.pause()
	if ( ctrlDead ) :
		user.master = 1
		user.hp = user.hpmax
		user.write("\r\n  \x1b[31mTragically, you are horribly disfigured....  oh wait...\x1b[0m\r\n")
		user.write("  \x1b[31mYou always looked like that you say?...  That's unfortunate...\x1b[0m\r\n")
		user.write("  \x1b[32mAnyway, you lost.  Being the gracious master "+thisEnemyName+" is, he heals\r\n  you and sends you away for the day.\x1b[0m\r\n")
		user.pause()
		
