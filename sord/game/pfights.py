#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains player fighting code.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "19 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

import random, re
from ..base import func
from ..base import user
from . import menu
from . import data
from . import util

class killer():
	""" S.O.R.D. Killing Fields """
	def __init__(self, user):
		""" Initialize Killing Fields Instance """
		self.user = user
		
	def run(self):
		""" Slaughter Run Logic """
		user = self.user
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if ( not user.expert ):
					user.write(user.art.killer())
				user.write(menu.slaughter(user))
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 'q' or key[0] == 'Q' or key[0] == 'r' or key[0] == 'R' ):
				user.write('R')
				thisQuit = True
			elif ( key[0] == 'e' or key[0] == 'E' ):
				user.write('E')
				util.dirt(user)
			elif ( key[0] == 'w' or key[0] == 'W' ):
				user.write('W')
				if ( user.pkill > 0 ):
					user.write(func.casebold("\r\n  Carve what in the soft dirt? :-: ", 2))
					ann = func.getLine(user.ntcon, True)
					user.dbcon.execute("INSERT INTO dirt ( `data`, `nombre` ) VALUES ( ?, ? )", (ann, user.thisFullname))
					user.dbcon.commit()
					user.write(func.casebold("\r\n  Carving Added!\r\n", 2))
					user.pause()
				else:
					user.write("\r\n  \x1b[32mYou have to accomplish something here before you can trash talk!\x1b[0m\r\n")
			elif ( key[0] == 'l' or key[0] == 'L' ):
				user.write('L')
				user.write(self.list())
				user.pause()
			elif ( key[0] == 's' or key[0] == 'S' ):
				user.write("S\r\n")
				tokillID = util.finduser(user, "\r\n  \x1b[32mKill Who ?")
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
						fight(user, usertoKill)
				else:
					user.write("\r\n  \x1b[32mNo user by that name found.\x1b[0m\r\n")
			else:
				skipDisp = True

	def list(self):
		""" Player List """
		user = self.user
		db = user.dbcon.cursor()
		db.execute("SELECT userid, fullname, exp, level, cls, sex, alive FROM users WHERE atinn = 0 AND userid <> ? AND userid NOT IN ( SELECT userid FROM online ) ORDER BY exp DESC", (user.thisUserID,))
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
	
			output += lineSex + lineClass + "\x1b[32m" + line[1] + func.padnumcol(str(line[1]), 23) + func.padright(str(line[2]), 11)
			output += func.padright(str(line[3]), 6) + "        " + lineStatus + "\r\n"
		db.close()
		return output + "\r\n"
		
	def menu(self, user, ehp, ename) : 
		""" Forest Fight Menu """
		thismenu  = "\r\n  \x1b[32mYour Hitpoints : \x1b[1m"+str(user.hp)+"\x1b[0m\r\n"
		thismenu += "  \x1b[32m"+ename+"'s Hitpoints : \x1b[1m"+str(ehp)+"\x1b[0m\r\n\r\n"
		thismenu += func.normmenu("(A)ttack")
		thismenu += func.normmenu("(S)tats")
		thismenu += func.normmenu("(R)un")
		thismenu += "\r\n  \x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? [\x1b[1;35mA\x1b[0m\x1b[32m] : \x1b[0m"
		return thismenu

	def fight(self, user, usertokill):
		""" Master Fight System """
		user.pfight -= 1
		thisUserDefense = user.defence
		thisUserHit     = user.str / 2
		ctrlDead = False
		ctrlRan  = False
		ctrlWin  = False
		thisEnemyHit     = usertokill.str / 2
		thisEnemyDefense = usertokill.defence
		thisEnemyWeapon  = data.weapon[usertokill.weapon]
		
		user.write("\r\n\r\n  \x1b[32m**\x1b[1;37mFIGHT\x1b[0m\x1b[32m**\r\n")
		user.write("\r\n  \x1b[32mYou have encountered "+usertokill.thisFullname+"!!\x1b[0m\r\n")
	
		skipDisp = False
		while ( user.hp > 0 and usertokill.hp > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
			if ( not skipDisp ):
				user.write(self.menu(user, usertokill.hp, usertokill.thisFullname))
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 's' or key[0] == 'S' ):
				user.write('S')
				user.write(util.viewstats(user))
			elif ( key[0] == 'a' or key[0] == 'A' ): # Attack!
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
						user.write("\r\n  \x1b[31m"+usertokill.thisFullname+" lies dead at your feet!\x1b[0m\r\n")
			elif ( key[0] == 'r' or key[0] == 'R' ): # Run Away
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
			elif ( key[0] == 'q' or key[0] == 'Q' ):
				user.write("Q\r\n  \x1b[31mYou are in Combat!  Try Running!\x1b[0m\r\n")
			elif ( key[0] == 'h' or key[0] == 'H' ):
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
			lamentTop = len(data.killerwin) - 1
			lamentThis = data.killerwin[random.randint(0, lamentTop)]
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
			lamentTop = len(data.killerlose) - 1
			lamentThis = data.killerlose[random.randint(0, lamentTop)]
			lamentThis = re.sub("`n", "\r\n", lamentThis)
			lamentThis = re.sub("`g", user.thisFullname, lamentThis)
			lamentThis = re.sub("`e", usertokill.thisFullname, lamentThis)
			user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (lamentThis,))
			user.dbcon.commit()
			user.write(func.casebold("  Tragically, you died.  Returning to the mundane world for the day...\n", 1))
			raise Exception('normal', "User is DOA.  Bummer.")


