#!/usr/bin/python
"""
 * Fighting Subsystem.
 * Contains forest fights, events, player fights, leveling up
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage """
import random, re, time
from functions import *
from data import *
from modules import *
from user2 import sorduser

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

def module_forest(user):
	""" Forest Fight - Non-Combat """
	thisQuit = False
	skipDisp = False
	while ( not thisQuit ):
		if ( not skipDisp ):
			if ( not user.expert ):
				user.write(user.art.forest())
				if ( user.horse == True ): 
					user.write(func_normmenu("(T)ake Horse to Dark Horse Tavern"))
			user.write(menu_forest(user))
		skipDisp = False
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			user.write('Q')
			thisQuit = True
		elif ( data[0] == '?' ):
			user.write('?')
			if ( user.expert ):
				user.write(user.art.forest())
		elif ( data[0] == 'x' or data[0] == 'X' ):
			user.write('X')
			user.toggleXprt()
		elif ( data[0] == 's' or data[0] == 'S' ):
			if ( user.level == 12 ):
				user.write('S')
				dragon_fight(user)
		elif ( data[0] == 'h' or data[0] == 'H' ):
			user.write('H')
			module_heal(user)
		elif ( data[0] == 'v' or data[0] == 'V' or data[0] == 'y' or data[0] == 'Y' ):
			module_viewstats(user)
		elif ( data[0] == 'l' or data[0] == 'l' ):
			user.write("L\r\n")
			if ( user.ffight > 0 ):
				if ( random.randint(1, 8) == 3 ):
					forest_special(user)
				else:
					forest_fight(user)
			else:
				user.write(func_casebold("\r\n  You are mighty tired.  Try again tommorow\r\n", 2))
		elif ( data[0] == 'a' or data[0] == 'A' ):
			user.write('A')
			user.write(func_casebold("\r\n  You brandish your weapon dramatically.\r\n", 2))
		elif ( data[0] == 'd' or data[0] == 'D' ):
			user.write('D')
			user.write(func_casebold("\r\n  Your Death Knight skills cannot help your here.\r\n", 2))
		elif ( data[0] == 'm' or data[0] == 'M' ):
			user.write('M')
			user.write(func_casebold("\r\n  Your Mystical skills cannot help your here.\r\n", 2))
		elif ( data[0] == 't' or data[0] == 'T' ):
			user.write('T')
			if ( user.horse == True ):
				dht_logic(user)
			else:
				user.write(func_casebold("\r\n  Your Thieving skills cannot help your here.\r\n", 2))
		elif ( data[0] == 'b' or data[0] == 'B' ):
			user.write('B')
			user.write(func_casebold("\r\n  A buzzard swoops down and grabs all your gold on hand.\r\n", 2))
			if ( user.gold > 0 ):
				user.bank += user.gold
				user.gold = 0
		else:
			skipDisp = True

def forest_special(user):
	""" Forest Special Events """
	if ( user.horse == True ):
		happening = random.randint(1, 11)
	else:
		happening = random.randint(1, 12)
	if ( happening == 1 ):   # Find Gems GOOD!
		thisfind = random.randint(1, 4)
		user.write(user.art.line())
		user.write("  \x1b[32mFortune Smiles Upon You.  You find \x1b[1;37m"+str(thisfind)+"\x1b[0m\x1b[32m gems!\x1b[0m\r\n")
		user.write(user.art.line())
		user.pause()
		user.gems += thisfind
	elif ( happening == 2 ): # Find Gold  GOOD!
		thisfind = random.randint(1, 4) * 200 * user.level
		user.write(user.art.line())
		user.write("  \x1b[32mFortune Smiles Upon You.  You find a sack full of \x1b[1;37m"+str(thisfind)+"\x1b[0m\x1b[32m gold!\x1b[0m\r\n")
		user.write(user.art.line())
		user.pause()
		user.gold += thisfind
	elif ( happening == 3 ): # Hammerstone (attack str++)  GOOD!
		user.write(user.art.line())
		user.write("  \x1b[32mYou find a hammer stone.  You quickly hit it as hard as possible.\r\n\r\n  \x1b[1mYour attack strength is raised by 1!\x1b[0m\r\n")
		user.write(user.art.line())
		user.pause()
		user.str += 1
	elif ( happening == 4 ): # Merry Men (hp = hpmax)
		user.write(user.art.line())
		user.write("  \x1b[32mYou stumble across a group of merry men.\r\n  They offer you ale you can't resist.\r\n  \x1b[1mYou feel refreshed!\x1b[0m\r\n")
		user.write(user.art.line())
		user.pause()
		user.hp = user.hpmax
	elif ( happening == 5 ): # Old Man (gold + (lvl * 500) && charm +1 on help) (costs 1 fight) GOOD!
		user.write(user.art.line())
		user.write("  \x1b[32mYou come upon an old man wandering around.\r\n  He asks you for help back to town.\x1b[0m\r\n\r\n")
		user.write(func_normmenu("(H)elp the old man"))
		user.write(func_normmenu("(I)gnore him"))
		user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
		miniQuit = False
		while ( not miniQuit ):
			data = user.ntcon.recv(2)
			if ( data[0] == 'h' or data[0] == 'H' ):
				user.write('H')
				goldtoadd = user.level * 500
				user.write("\r\n\r\n  \x1b[32mYou help the old gentleman home.\r\n  \x1b[1mHe gives you "+str(goldtoadd)+" gold and 1 charm!.\x1b[0m\r\n")
				user.gold += goldtoadd
				user.charm += 1
				user.ffight -= 1
				miniQuit = True
			elif ( data[0] == 'i' or data[0] == 'I' ):
				user.write('I')
				user.write("\r\n  \x1b[31mYou just really \x1b[1mSUCK\x1b[0;31m, don't you?\x1b[0m\r\n")
				miniQuit = True
			else:
				pass
		user.pause()
	elif ( happening == 6 ): # Ugly (33%) and Pretty (66%) stick GOOD!
		user.write(user.art.line())
		user.write("  \x1b[32mA demented penguin jumps from the bushes and whacks you with a")
		sticktype = random.randint(1, 3)
		if ( sticktype == 2 ):
			user.write("\x1b[1;31m ugly \x1b[0;32m")
		else:
			user.write("\x1b[1m pretty \x1b[0;32m")
		user.write("stick!\r\n  Your charm is ")
		if ( sticktype == 2 ):
			user.write("lowered")
			if ( user.charm > 0 ):
				user.charm -= 1
		else:
			user.write("raised")
			user.charm += 1
		user.write(" by 1!!\x1b[0m\r\n")
		user.pause()
	elif ( happening == 7 ): # Old Hag GOOD!
		user.write(user.art.line())
		user.write("  \x1b[32mYou come across an old hag.\r\n\r\n  \x1b[1m\"Give me a gem my pretty, and I will completely heal you!\"\x1b[0;32m\r\n  She screeches!\x1b[0m\r\n\r\n")
		user.write(func_normmenu("(G)ive her a gem"))
		user.write(func_normmenu("(K)ick her and run"))
		user.write(func_normmenu("(L)eave polietly"))
		miniQuit = False
		while ( not miniQuit ):
			user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
			data = user.ntcon.recv(2)
			if ( data[0] == 'l' or data[0] == 'L' ):
				user.write("L\r\n\r\n  \x1b[32mThe old hag begins following you like a lost puppy.\x1b[0m\r\n")
			elif ( data[0] == 'k' or data[0] == 'K' ):
				user.write("K\r\n\r\n  \x1b[32mYou hate to be rude to your elders, but sometimes deperate times call for\r\n  deperate measures.  You which the old hag in the shin and run for it.\x1b[0m\r\n")
				miniQuit = True
			elif ( data[0] == 'g' or data[0] == 'G' ):
				user.write('G')
				if ( user.gems > 0 ):
					user.write("\r\n\r\n  \x1b[1;32m\"Thank you\"\x1b[0;32m she cackles.\r\n  \x1b[1mYou feel refreshed and renewed\x1b[0m\r\n")
					user.hpmax += 1
					user.hp = user.hpmax
					user.gems -= 1
					miniQuit = True
				else:
					user.write("\r\n\r\n  \x1b[1;32m\"You don't have any gems you stinky cow-pox pustule!\"\[33[0;32m she yells.\r\n  \x1b[1mCome to think of it, you feel rather like a cow-pie.\x1b[0m\r\n")
					user.hp = 1
					miniQuit = True
			else: 
				pass
		user.pause()
	elif ( happening == 8 ): # Flowers in the forest. GOOD!
		user.write(user.art.line())
		user.write("  \x1b[32mYou come across a grove of flowers, and decide to inspect them closer...\r\n  \x1b[1mThere is something written here!\x1b[0m\r\n")
		user.pause()
		module_flowers(user)
	elif ( happening == 9 ): # rescue man/maiden GOOD!
		user.write(user.art.line())
		user.write("  \x1b[32mYou come upon a dead bird.  While gross, you begin to put it out of your\r\n  mind when you notice a scroll attached to it's leg\r\n\r\n")
		user.write("  \x1b[1mTo Whome It May Concern:\r\n    I have been locked in this terrible tower for many cycles.\r\n    Please save me soon!\n        ~ Elora\r\n\r\n")
		user.write(func_normmenu("(S)eek the maiden"))
		user.write(func_normmenu("(I)gnore her plight"))
		user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
		miniQuit = False
		while ( not miniQuit ):
			data = user.ntcon.recv(2)
			if ( data[0] == 'i' or data[0] == 'I' ):
				user.write('I')
				miniQuit = True
			elif ( data[0] == 's' or data[0] == 'S' ):
				user.write('S')
				user.ffight -= 1
				thisMiniQuit = False
				thisTower = 0
				user.write("\r\n\r\n  \x1b[32mWhere do you wish to seek the maiden?\x1b[0m\r\n")
				user.write(func_normmenu("(K)eep of Hielwain"))
				user.write(func_normmenu("(S)tarbucks Seattle Spaceneedle"))
				user.write(func_normmenu("(C)astle Morbidia"))
				user.write(func_normmenu("(S)ty of Pigashia"))
				user.write(func_normmenu("(B)logshares Brutal Belfry"))
				user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
				while ( not thisMiniQuit ):
					miniData = user.ntcon.recv(2)
					if ( miniData[0] == 'k' or miniData[0] == 'K' ):
						user.write('K')
						thisTower = 1
						thisMiniQuit = True
					elif ( miniData[0] == 's' or miniData[0] == 'S' ):
						user.write('S')
						thisTower = 2
						thisMiniQuit = True
					elif ( miniData[0] == 'c' or miniData[0] == 'C' ):
						user.write('C')
						thisTower = 3
						thisMiniQuit = True
					elif ( miniData[0] == 's' or miniData[0] == 'S' ):
						user.write('S')
						thisTower = 4
						thisMiniQuit = True
					elif ( miniData[0] == 'b' or miniData[0] == 'B' ):
						user.write('B')
						thisTower = 5
						thisMiniQuit = True
					else:
						pass
				user.write(user.art.tower())
				user.pause()
				if ( thisTower == random.randint(1, 5) ): # Correct Choice
					user.write("\r\n  \x1b[32mYou have choosen \x1b[1mwisely.\x1b[0m\r\n")
					user.write("  \x1b[32mElora gasps in suprise, saunters over, and thanks you 'properly'\r\n  \x1b[1mYou feel smarter, more gem laden, and -erm- 'satisfied'\x1b[0m\r\n")
					user.gems += 5
					user.gold += (user.level * 500)
				else: # WRONG
					if ( random.randint(1, 2) == 1 ): # REALLY, REALLY WRONG
						user.write("\r\n  \x1b[32mYou have choosen \x1b[1mpoorly.  really poorly.\x1b[0m\r\n\r\n")
						user.write("  \x1b[32mYou hear a strange groan and out pops Ken the Magnificent,\r\n  the disfigured midget (er, 'little person').\r\n  Sadly, 'little person' doesn't refer to all of him.\r\n\r\n  \x1b[1mYou feel terrible, both physically and mentally\x1b[0m\r\n")
						user.hp = 1
					else: # NOT SO BAD
						user.write("\r\n  \x1b[32mYou have choosen \x1b[1mpoorly.\x1b[0m\r\n")
						user.write("  \x1b[32mYou run like hell before anything bad happens.\x1b[0m\r\n")
				miniQuit = True
		user.pause()
	elif ( happening == 10 ): # lessons DKNIGHT GOOD, 
		if ( user.cls == 1 ):
			forest_lesson_d(user)
		elif ( user.cls == 2 ):
			forest_lesson_m(user)
		else:
			forest_lesson_t(user)
	elif ( happening == 11 ): # fairies
		forest_fairies(user)
		user.pause()
	elif ( happening == 12 ): # darkhorse
		dht_logic(user)
		user.pause()
	else:
		pass
		

def forest_fairies(user):
	user.write(user.art.fairies())
	user.pause()
	user.write("  \x1b[32mYou glance at the fairies, trying to decide what to do.\r\n\r\n")
	user.write(func_normmenu("(A)sk for a Blessing"))
	user.write(func_normmenu("(T)ry and catch one"))
	miniQuit = False
	while ( not miniQuit ):
		user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
		miniData = user.ntcon.recv(2)
		if ( miniData[0] == 'a' or miniData[0] == 'A' ):
			user.write('A')
			miniQuit = True
			blessingIs = random.randint(1, 4)
			if ( blessingIs == 4 and user.horse == True ):
				# Trap for already has a horse!
				blessingIs = 2
			if ( blessingIs == 1 ): # A Kiss
				user.write("\r\n\r\n  \x1b[32mYou recieve a kiss from Teesha and feel better!\x1b[0m\r\n\r\n")
				user.hp = user.hpmax
			elif ( blessingIs == 2 ): # Sad Stories
				user.write("\r\n\r\n  \x1b[32mThe fairies tell you sad stories.\r\n  \x1b[1mYou're tears turn into gems!\x1b[0m\r\n\r\b")
				user.gems += 2
			elif ( blessingIs == 3 ): # Fairy lore.
				user.write("\r\n\r\n  \x1b[32mThe fairies tell you secret fairly lore.\r\n  \x1b[1mYou feel smarter\x1b[0m\r\n\r\b")
				user.exp += ( user.level * 20 )
			elif ( blessingIs == 4 ): # The Horse
				user.write("\r\n\r\n  \x1b[32mThe fairys bless you with a new companion!\r\n  Please remember, horses are for riding, not, er... \x1b[1m*riding*\x1b[0m\r\n\r\n")
				user.horse = 1
			else:
				user.write("\r\n\r\n  \x1b[1;37mWTF?\x1b[0m\r\n\r\n")
		if ( miniData[0] == 't' or miniData[0] == 'T' ):
			user.write('T')
			miniQuit = True
			caughtIt = random.randint(1, 3)
			if ( caughtIt == 3 ):  # Grabbed One!
				user.write("\r\n\r\n  \x1b[32mYou managed to grab one!\r\n  You place it in your pocket for later.\x1b[0m\r\n")
				user.fairy = 1
			else:
				user.write("\r\n\r\n  \x1b[32mYou MISS!  And grab a thornberry bush instead!\x1b[0m\r\n")
				user.hp = 1

def forest_fight(user):
	""" Forest Fight System """
	user.ffight -= 1
	thisUserLevel = user.level
	thisTopEnemy  = len(enemies[thisUserLevel]) - 1
	thisEnemy     = random.randint(0, thisTopEnemy)
	if ( random.randint(1, 10) == 8 ):
		thisUnderdog = True
	else:
		thisUnderdog = False
	thisUserDefense = user.defence
	thisUserHit     = user.str / 2
	ctrlDead = False
	ctrlRan  = False
	ctrlWin  = False
	thisEnemyHit    = enemies[thisUserLevel][thisEnemy][2] / 2
	thisEnemyHP     = enemies[thisUserLevel][thisEnemy][3]
	thisEnemyName   = enemies[thisUserLevel][thisEnemy][0]
	thisEnemyWeapon = enemies[thisUserLevel][thisEnemy][1]
	
	user.write("\r\n\r\n  \x1b[32m**\x1b[1;37mFIGHT\x1b[0m\x1b[32m**\r\n")
	user.write("\r\n  \x1b[32mYou have encountered "+thisEnemyName+"!!\x1b[0m\r\n")

	if ( thisUnderdog ):
		if ( user.horse == True and random.randint(1, 3) == 2 ):
			user.write("\r\n  \x1b[32m\"Prepare to die, fool!\" "+thisEnemyName+" screams.\r\n")
			user.write("  He takes a Death Crystal from his cloak and throws it at you.\r\n")
			user.write("  Your horse moves its huge body to intercept the crystal.\r\n")
			user.write("\r\n  \x1b[1mYOUR HORSE IS VAPORIZED!\x1b[0;32m\r\n\r\n")
			user.write("  Tears of anger flow down your cheeks.  Your valiant steed must be\r\n")
			user.write("  avenged.\r\n")
			user.write("\r\n  \x1b[1mYOU PUMMEL "+thisEnemyName+" WITH BLOWS!\x1b[0;32m\r\n\r\n")
			user.write("  A few seconds later, your adversary is dead.\r\n")
			user.write("  You bury your horse in a small clearing.  The best friend you ever\r\n")
			user.write("  had.\r\n")
			thisEnemyHP = 0
			ctrlWin = True
			user.horse = 0
		else:
			hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
			if ( hisAttack > 0 ):
				if ( hisAttack > user.hp ):
					ctrlDead = True
					hisAttack = user.hp
				user.write("\r\n  \x1b[32m"+thisEnemyName+" executes a sneak attach for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage!\x1b[0m\r\n")
				user.hp -= hisAttack
			else:
				user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely!\x1b[0m\r\n")
	else:
		user.write("\r\n  \x1b[32mYour skill allows you to get the first strike.\x1b[0m\r\n")

	skipDisp = False
	while ( user.hp > 0 and thisEnemyHP > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
		if ( not skipDisp ):
			user.write(forest_menu(user, thisEnemyHP, thisEnemyName, True))
		skipDisp = False
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 's' or data[0] == 'S' ):
			user.write('S')
			user.write(module_viewstats(user))
		elif ( data[0] == 'a' or data[0] == 'A' ): # Attack!
			user.write("A\r\n")
			hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
			myAttack  = ( thisUserHit + random.randint(0, thisUserHit))
			if ( not thisUnderdog ): # We Hit First
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
					user.write("\r\n  \x1b[31m"+enemies[thisUserLevel][thisEnemy][6]+"\x1b[0m\r\n")
		elif ( data[0] == 'd' or data[0] == 'D' ): # Attack!
			user.write("D\r\n")
			if ( user.getSkillUse(1) > 0 ):
				user.updateSkillUse(1, -1)
				hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
				myAttack  = ( thisUserHit + (random.randint(2,5) * random.randint((thisUserHit / 2), thisUserHit))) + thisUserHit
				if ( not thisUnderdog ): # We Hit First
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
					user.write("\r\n  \x1b[1;32mUltra Powerful Move!\x1b[0m\r\n  \x1b[32mYou hit "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
					thisEnemyHP = thisEnemyHP - myAttack
					if ( thisEnemyHP < 1 ): # We Win!
						ctrlWin = True
						user.write("\r\n  \x1b[31m"+enemies[thisUserLevel][thisEnemy][6]+"\x1b[0m\r\n")
			else:
				user.write("\r\n  \x1b[32mYou have no Death Knight Skill Use Points!\x1b[0m\r\n\r\n")
		elif ( data[0] == 't' or data[0] == 'T' ): # Attack!
			user.write("T\r\n")
			if ( user.getSkillUse(3) > 0 ):
				user.updateSkillUse(3, -1)
				hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - ( thisUserDefense * 2 )
				myAttack  = ( thisUserHit + (random.randint(1,3) * random.randint((thisUserHit / 2), thisUserHit))) + thisUserHit
				if ( not thisUnderdog ): # We Hit First
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
					user.write("\r\n  \x1b[1;32mUltra Sneaky Move!\x1b[0m\r\n  \x1b[32mYou hit "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
					thisEnemyHP = thisEnemyHP - myAttack
					if ( thisEnemyHP < 1 ): # We Win!
						ctrlWin = True
						user.write("\r\n  \x1b[31m"+enemies[thisUserLevel][thisEnemy][6]+"\x1b[0m\r\n")
			else:
				user.write("\r\n  \x1b[32mYou have no Thief Skill Use Points!\x1b[0m\r\n\r\n")
		elif ( data[0] == 'r' or data[0] == 'R' ): # Run Away
			if ( random.randint(1, 10) == 4 ): # Hit in the back.
				hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
				if ( hisAttack >= user.hp ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.hp # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you in the back with it's "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\r\n")
					user.hp -= hisAttack
					ctrlRan = True
			else:
				user.write("\r\n  \x1b[32mYou narrowly escape harm.\x1b[0m\r\n")
				ctrlRan = True
		elif ( data[0] == 'q' or data[0] == 'Q' ):
			user.write("\r\n  \x1b[31mYou are in Combat!  Try Running!\x1b[0m\r\n")
		elif ( data[0] == 'h' or data[0] == 'H' ):
			user.write("\r\n  \x1b[32mYou are in combat, and they don't make house calls!\x1b[0m\r\n")
		elif ( data[0] == 'l' or data[0] == 'L' ):
			user.write("\r\n  \x1b[32mWhat?!  You want to fight two at once?\x1b[0m\r\n")
		elif ( data[0] == 'm' or data[0] == 'M' ): #Magic!
			if ( user.getSkillUse(2) < 1 ):
				user.write("\r\n  \x1b[32mYou have no Magical Use Points!\x1b[0m\r\n\r\n")
			else:
				user.write("\r\n" + func_normmenu("(N)evermind") + func_normmenu("(P)inch Real Hard (1)"))
				if ( user.getSkillUse(2) > 3 ):
					user.write(func_normmenu("(D)isappear (4)"))
					if ( user.getSkillUse(2) > 7 ):
						user.write(func_normmenu("(H)eat Wave (8)"))
						if ( user.getSkillUse(2) > 11 ):
							user.write(func_normmenu("(L)ight Shield (12)"))
							if ( user.getSkillUse(2) > 15 ):
								user.write(func_normmenu("(S)hatter (16)"))
								if ( user.getSkillUse(2) > 19 ):
									user.write(func_normmenu("(M)ind Heal (20)"))
				user.write("\r\n  \x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? [\x1b[1;35mA\x1b[0m\x1b[32m] : \x1b[0m")
				tinyQuit = False
				while ( not tinyQuit ):
					miniData = user.ntcon.recv(2)
					if not miniData: break
					elif ( miniData[0] == 'n' or miniData[0] == 'N' ): #Nothing
						user.write("N\r\n  \x1b[32mSure thing boss.\x1b[0m\r\n")
						tinyQuit = True
					elif ( miniData[0] == 'p' or miniData[0] == 'P' ): #Pinch!
						user.write("P")
						user.updateSkillUse(2, -1)
						tinyQuit = True
						hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
						myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + ( thisUserHit / 4 )
						if ( not thisUnderdog ): # We Hit First
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
							user.write("\r\n  \x1b[32mYou pinch "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
							thisEnemyHP = thisEnemyHP - myAttack
							if ( thisEnemyHP < 1 ): # We Win!
								ctrlWin = True
								user.write("\r\n  \x1b[31m"+enemies[thisUserLevel][thisEnemy][6]+"\x1b[0m\r\n")
					elif ( (miniData[0] == 'd' or miniData[0] == 'D') and ( user.getSkillUse(2) > 3 ) ): #Disappear
						user.write("D\r\n  \x1b[32mYou disapper like a ghost!\x1b[0m\r\n")
						user.updateSkillUse(2, -4)
						tinyQuit = True
						ctrlRan = True
					elif ( (miniData[0] == 'h' or miniData[0] == 'H') and ( user.getSkillUse(2) > 7 ) ): #Heat Wave
						user.write("H")
						user.updateSkillUse(2, -8)
						tinyQuit = True
						hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
						myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + (thisUserHit / 2)
						if ( not thisUnderdog ): # We Hit First
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
							user.write("\r\n  \x1b[32mYou blast "+thisEnemyName+" with Heat Wave for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
							thisEnemyHP = thisEnemyHP - myAttack
							if ( thisEnemyHP < 1 ): # We Win!
								ctrlWin = True
								user.write("\r\n  \x1b[31m"+enemies[thisUserLevel][thisEnemy][6]+"\x1b[0m\r\n")
					elif ( (miniData[0] == 'l' or miniData[0] == 'L') and ( user.getSkillUse(2) > 11 ) ): #Light Shield
						user.write("L\r\n  \x1b[32mYou feel a bit odd.  You dig in a feel better defended\x1b[0m\r\n")
						user.updateSkillUse(2, -12)
						thisUserDefense = thisUserDefense * 2
						tinyQuit = True
					elif ( (miniData[0] == 's' or miniData[0] == 'S') and ( user.getSkillUse(2) > 15 ) ): #Shatter
						user.write("S")
						user.updateSkillUse(2, -16)
						tinyQuit = True
						hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
						myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + (thisUserHit * 2)
						if ( not thisUnderdog ): # We Hit First
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
							user.write("\r\n  \x1b[32mYou Shatter "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
							thisEnemyHP = thisEnemyHP - myAttack
							if ( thisEnemyHP < 1 ): # We Win!
								ctrlWin = True
								user.write("\r\n  \x1b[31m"+enemies[thisUserLevel][thisEnemy][6]+"\x1b[0m\r\n")
					elif ( (miniData[0] == 'm' or miniData[0] == 'M') and ( user.getSkillUse(2) > 19 ) ): #Mind Heal
						user.write("M\r\n  \x1b[32mYou feel much better!\x1b[0m\r\n")
						user.updateSkillUse(2, -20)
						hptoadd = user.hpmax - user.hp
						user.hp = user.hpmax
						if ( hptoadd < 5 ):
							user.write("\r\n  \x1b[32mThough, you are likely clinicly retarded.\x1b[0m\r\n")
						tinyQuit = True
		else: #Catch non-options
			skipDisp = True

	if ( ctrlWin ) :
		user.exp += enemies[thisUserLevel][thisEnemy][5]
		user.gold += enemies[thisUserLevel][thisEnemy][4]
		user.write("\r\n  \x1b[32mYou have recieved \x1b[1m"+str(enemies[thisUserLevel][thisEnemy][4])+"\x1b[22m gold and \x1b[1m"+str(enemies[thisUserLevel][thisEnemy][5])+"\x1b[22m experience\x1b[0m\r\n")
		user.pause()
	if ( ctrlDead ) :
		if ( user.fairy == True ):
			user.hp = 1
			user.fairy = 0
			user.write(func_casebold("  Miraculously, your fairy saves you from the edge of defeat.  You escape with your life.\r\n", 2))
		else:
			user.alive = 0
			#exception handles, do it later. user.logout()
			lamentTop = len(forestdie) - 1
			lamentThis = forestdie[random.randint(0, lamentTop)]
			lamentThis = re.sub("`n", "\r\n", lamentThis)
			lamentThis = re.sub("`g", user.thisFullname, lamentThis)
			lamentThis = re.sub("`e", thisEnemyName, lamentThis)
			user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (lamentThis,))
			user.dbcon.commit()
			user.write(func_casebold("  Tragically, you died.  Returning to the mundane world for the day...\n", 1))
			raise Exception('normal', "User is DOA.  Bummer.")

def forest_menu(user, enemyHP, enemyName, special=False) : 
	""" Forest Fight Menu """
	thismenu  = "\r\n  \x1b[32mYour Hitpoints : \x1b[1m"+str(user.hp)+"\x1b[0m\r\n"
	thismenu += "  \x1b[32m"+enemyName+"'s Hitpoints : \x1b[1m"+str(enemyHP)+"\x1b[0m\r\n\r\n"
	thismenu += func_normmenu("(A)ttack")
	thismenu += func_normmenu("(S)tats")
	thismenu += func_normmenu("(R)un")
	if ( special ):
		thismenu += "\r\n"
		if ( user.getSkillUse(1) > 0 ):
			thismenu += func_normmenu("(D)eath Knight Attack ("+str(user.getSkillUse(1))+")")
		if ( user.getSkillUse(2) > 0 ):
			thismenu += func_normmenu("(M)ystical Powers ("+str(user.getSkillUse(2))+")")
		if ( user.getSkillUse(3) > 0 ):
			thismenu += func_normmenu("(T)heiving Sneak Attack ("+str(user.getSkillUse(3))+")")
	thismenu += "\r\n  \x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? [\x1b[1;35mA\x1b[0m\x1b[32m] : \x1b[0m"
	return thismenu

def forest_lesson_d(user) :
	""" Learn to be a death kniofht"""
	user.write(user.art.line())
	user.write("\r\n  \x1b[32mYou come upon a group of warriors, they carry the look of a proud people.\x1b[0m\r\n")
	user.write("\r\n   \x1b[1;32mDeath Knight #1: \x1b[0;32mWe shall teach you the ways of the death knights weakling.\x1b[0m\r\n")
	user.write("   \x1b[1;32mDeath Knight #2: \x1b[0;32mAye.  But you must prove your wisdom first.\r\n                    This man is guilty of a crime.\x1b[0m\r\n")
	user.write("   \x1b[1;32mDeath Knight #1: \x1b[0;32mYup.  Or he's completely innocent.  Decide wisely.!\x1b[0m\r\n")
	user.write(func_normmenu("(K)ill Him"))
	user.write(func_normmenu("(F)ree him as an innocent"))
	user.write("\r\n  \x1b[0m\x1b[32mYour choice, \x1b[1m"+user.thisFullname+"\x1b[22m? (K,F) \x1b[0m\x1b[32m:-: \x1b[0m")
	miniQuit = False
	while ( not miniQuit ):
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 'k' or data[0] == 'K' ):
			user.write('K')
			user.write("\r\n  \x1b[32mYou draw your weapon, and ram it as hard as you can through his midsection.\x1b[0m\r\n")
			thisChoice = 1
			miniQuit = True
		elif ( data[0] == 'f' or data[0] == 'F' ):
			user.write('F')
			user.write("\r\n  \x1b[32mYou consider a moment, and shout \"Let him live!  He's done nothing wrong!\"\x1b[0m\r\n")
			thisChoice = 2
			miniQuit = True

	user.write("\r\n  \x1b[1;37m...")
	time.sleep(1)
	user.write("\x1b[31mAND\x1b[37m")
	time.sleep(1)
	user.write("...\x1b[0m")
	
	if ( thisChoice == random.randint(1,2) ):
		user.write("\r\n   \x1b[1;32mDeath Knight #1: \x1b[0;32mWell spotted young warrior.                    We shall teach you!\x1b[0m\r\n")
		user.write("  \x1b[32mYou recieve \x1b[1m1\x1b[0;32m use point")
		user.updateSkillUse(1, 1)
		user.hp = user.hpmax
		if ( user.getSkillPoint(1) < 40 ):
			user.updateSkillPoint(1, 1)
			user.write(" and \x1b[1m1\x1b[0;32m skill point")
		user.write(".\x1b[0m\r\n")
	else:
		user.write("\r\n   \x1b[1;32mDeath Knight #3: \x1b[0;32mOh god no!  That wasn't right at all!\r\n                    Somebody get a mop and a bandaid!\x1b[0m\r\n")

def forest_lesson_t(user) :
	""" LEarn to be a thief """
	user.write(user.art.line())
	user.write("\r\n  \x1b[32mYou come upon a gathering of the theives guild, they kinda smell bad.\x1b[0m\r\n")
	user.write("\r\n   \x1b[1;32mThief #1: \x1b[0;32mWe can make you a better thief.  Just cost ya a gem.\x1b[0m\r\n")
	user.write(func_normmenu("(G)ive him the gem"))
	user.write(func_normmenu("(S)pit on him and walk away"))
	user.write(func_normmenu("(M)utter incoherantly, hoping he'll leave"))
	user.write("\r\n  \x1b[0m\x1b[32mYour choice, \x1b[1m"+user.thisFullname+"\x1b[22m? (G,S,M) \x1b[0m\x1b[32m:-: \x1b[0m")
	miniQuit = False
	while ( not miniQuit ):
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 's' or data[0] == 'S' ):
			user.write("S\r\n  \x1b[32mAs you spit on him, the thief looks at you closely.  He almost looks proud.\x1b[0m\r\n")
			miniQuit = True
		elif ( data[0] == 'm' or data[0] == 'M' ):
			user.write("M\r\n  \x1b[32mAs the thief leaves, you distincly hear the words \"nutjob\" and \"jackass\".  Oh well.\x1b[0m\r\n")
			miniQuit = True
		elif ( data[0] == 'g' or data[0] == 'G' ):
			user.write('G')
			if ( user.gems > 0 ):
				user.updateSkillUse(3, 1)
				user.write("\r\n  \x1b[32mYou recieve \x1b[1m1\x1b[0;32m use point")
				if ( user.getSkillPoint(3) < 40 ):
					user.updateSkillPoint(3, 1)
					user.write(" and \x1b[1m1\x1b[0;32m skill point")
				user.write(".\x1b[0m\n")
				user.gems -= 1
			else:
				user.write("\r\n  \x1b[1;32mThief #1: \x1b[0;32mYou don't have any gems dumbass.\x1b[0m\r\n")
			miniQuit = True

def forest_lesson_m(user) :
	""" Learn about magic """
	user.write(user.art.line())
	user.write("\r\n  \x1b[32mYou come upon an old house.  You sense an old mage might live here.\x1b[0m\r\n")
	user.write(func_normmenu("(K)nock on the door"))
	user.write(func_normmenu("(B)ang on the door"))
	user.write(unc_normmenu("(L)eave"))
	user.write("\r\n  \x1b[0m\x1b[32mYour choice, \x1b[1m"+user.thisFullname+"\x1b[22m? (K,B,L) \x1b[0m\x1b[32m:-: \x1b[0m")
	miniQuit1 = False
	miniQuit2 = False
	
	while ( not miniQuit1 ):
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 'k' or data[0] == 'K' ):
			user.write(data[0])
			user.write("\r\n  \x1b[32mYou knock polietly on the door.\x1b[0m\n")
			miniQuit1 = True
		elif ( data[0] == 'b' or data[0] == 'B' ):
			user.write(data[0])
			user.write("\r\n  \x1b[32mYou bang wildly on the door.\x1b[0m\n")
			miniQuit1 = True
		elif ( data[0] == 'l' or data[0] == 'L' ):
			user.write("\n  \x1b[32mYou leave, confident in finding better things to do.\x1b[0m\n")
			miniQuit1 = True
			miniQuit2 = True

	if ( not miniQuit2 ):
		if ( random.randint(1, 5) == 2 ):
			user.write("\r\n  \x1b[32mNothing happens, and you leave.\x1b[0m\r\n")
		else:
			user.write("\r\n  \x1b[32mThe old man rips open the door and screams \"WHAT?!?\"\x1b[0m\r\n")
			user.write("  \x1b[32mHe then gazes at you and says \"I'll teach you magic if you can guess\r\n  the number I'm thinking of.  It's between 1 and 100\x1b[0m\r\n")
			magicNumber  = random.randint(1, 100)
			magicCorrect = False
			magicGuess   = 0
			while ( magicGuess < 7 ):
				user.write("\r\n  \x1b[0m\x1b[32mYour guess, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
				try: 
					thisGuess = int(func_getLine(user.ntcon, True))
				except ValueError:
					thisGuess = 1
				if ( thisGuess == magicNumber ):
					magicGuess = 7
					magicCorrect = True
				else:
					if ( thisGuess < magicNumber ):
						user.write("\r\n  \x1b[32mHigher!\x1b[0m\r\n")
					if ( thisGuess > magicNumber ):
						user.write("\r\n  \x1b[32mLower!\x1b[0m\r\n")
				magicGuess += 1

			if ( magicCorrect ):
				user.write("\r\n  \x1b[32mWell Done young mage!\x1b[0m\r\n")
				user.updateSkillUse(2, 1)
				user.write("  \x1b[32mYou recieve \x1b[1m1\x1b[0;32m use point")
				if ( user.getSkillPoint(2) < 40 ):
					user.updateSkillPoint(2, 1)
					user.write(" and \x1b[1m1\x1b[0;32m skill point")
				user.write(".\x1b[0m\r\n")
			else:
				user.write("\r\n  \x1b[32mBetter luck next time!\x1b[0m\r\n")

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

def dht_main_menu(user):
	"""Dark Cloak Menu"""
	thismsg  = "\r\n\r\n\x1b[32m                          Dark Cloak Tavern\r\n"
	thismsg += user.art.line()
	thismsg += "  \x1b[32mA blazing fire warms your heart as well as your body in this fragrant.\x1b[0m\r\n"
	thismsg += "  \x1b[32mroadhouse.  Many a wary traveler has had the good fortune to find this\x1b[0m\r\n"
	thismsg += "  \x1b[32mcozy hostel, to escape the harsh reality of the dense forest for a few\x1b[0m\r\n"
	thismsg += "  \x1b[32mmoments.  You notice someone has etched something in the table you are\x1b[0m\r\n"
	thismsg += "  \x1b[32msitting at.\x1b[0m\r\n\r\n"
	thismsg += func_menu_2col("(C)onverse With The Patrons", "(D)aily News", 5, 5)
	thismsg += func_menu_2col("(E)xamine Etchings In Table", "(Y)our Stats", 5, 5)
	thismsg += func_menu_2col("(T)alk with Bartender", "(R)eturn to Forest", 5, 5)
	return thismsg
	
def dht_prompt(user):
	""" User Prompt"""
	ptime = func_maketime(user)
	thismenu  = "\r\n  \x1b[1;35mThe Dark Cloak Tavern\x1b[0m\x1b[1;30m (? for menu)\x1b[0m\r\n"
	thismenu += "  \x1b[1;30m(C,D,E,Y,T,R)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

def dht_converse(user):
	""" Converse with patrons (dht)"""
	output  = "\r\n\r\n  \x1b[1;37mConverse with the Patrons\x1b[22;32m....\x1b[0m\r\n"
	output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	db = user.dbcon.cursor()
	db.execute("SELECT data, nombre FROM (SELECT * FROM dhtpatrons ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id")
	for (data, nombre) in db.fetchall():
		output += "    \x1b[32m"+nombre+" \x1b[1;37msays... \x1b[0m\x1b[32m" + func_colorcode(data)
		output += "\x1b[0m\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	output += "\r\n  \x1b[32mAdd to the conversation? \x1b[1m: \x1b[0m"
	user.write(output)
	db.close()
	yesno = user.ntcon.recv(2)
	if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
		user.write(func_casebold("\r\n  What say you? :-: ", 2))
		ann = func_getLine(user.ntcon, True)
		user.dbcon.execute("INSERT INTO dhtpatrons ( `data`, `nombre` ) VALUES ( ?, ? )", (ann, user.thisFullname))
		user.dbcon.commit()
		user.write(func_casebold("\r\n  Wisdom added!\r\n", 2))
		user.pause()

def dht_logic(user):
	""" Dark Horse Tavern Logic"""
	thisQuit = False
	skipDisp = False
	while ( not thisQuit ):
		if ( not skipDisp ):
			if (  not user.expert ):
				user.write(dht_main_menu(user))
			user.write(dht_prompt(user))
		skipDisp = False
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			user.write('R')
			thisQuit = True
		elif ( data[0] == '?' ):
			user.write('?')
			user.write(dht_main_menu(user))
			skipDisp = True
		elif ( data[0] == 'y' or data[0] == 'Y' ):
			user.write('Y')
			user.write(module_viewstats(user))
			user.pause()
		elif ( data[0] == 'd' or data[0] == 'D' ):
			user.write('D')
			user.write(module_dailyhappen(True, user.dbcon, ''))
			user.pause()
		elif ( data[0] == 'c' or data[0] == 'C' ):
			user.write('C')
			dht_converse(user)
		elif ( data[0] == 'e' or data[0] == 'E' ):
			user.write('E')
			db = user.dbcon.cursor()
			db.execute("SELECT fullname, fuck FROM users u, stats s WHERE s.userid = u.userid AND s.fuck > 0 ORDER by s.fuck DESC")
			user.write("\r\n\r\n  \x1b[32mUsers who have gotten lucky:\x1b[0m\r\n")
			
			for row in db.fetchall():
				if not row:
					user.write("\r\n\r\n  \x1b[32mWhat a sad thing - there are no carvings here after all.\x1b[0m\r\n")
				else:
					for (nombre, data) in row:
						user.write("  \x1b[32m"+nombre+padnumcol(nombre, 25)+"\x1b[1m"+str(data)+"\x1b[0m\r\n")
			user.write("\r\n")
			db.close()
			user.pause()
		elif ( data[0] == 't' or data[0] == 'T' ):
			user.write('T')
			dht_chance(user)
		else:
			skipDisp = True
			
def dht_chance_menu(user):
	""" Chance's Menu"""
	ptime = func_maketime(user)
	thismenu = func_normmenu("(C)hange Profession")
	thismenu += func_normmenu("(L)earn About Your Enemies")
	thismenu += func_normmenu("(T)alk About Colors")
	thismenu += func_normmenu("(R)eturn to Tavern")
	thismenu += "\r\n  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu
	
def dht_chance(user):
	header = "\r\n\r\n  \x1b[32m              Talking To Chance\x1b[0m\r\n"
	header += "\x1b[32m-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\x1b[0m\r\n"
	header += "  \x1b[32mYou seat yourself next to the bartender,\x1b[0m\r\n"
	header += "  \x1b[32mfor some reason you like him.          \x1b[0m\r\n\r\n"
	thisQuit = False
	skipDisp = False
	while ( not thisQuit ):
		if ( not skipDisp ):
			user.write(header)
			user.write(dht_chance_menu(user))
		skipDisp = False
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			user.write('R')
			thisQuit = True
		elif ( data[0] == 't' or data[0] == 'T' ):
			user.write('T')
			user.write("\r\n\r\n  \x1b[32mColors are easy my friend!  Just enclose single ANSI codes in braces\r\n  like this {32} - that would turn the text green you can learn\r\n  more at:\r\n    http://en.wikipedia.org/wiki/ANSI_escape_code\x1b[0m\r\n")
			user.pause()
		elif ( data[0] == 'l' or data[0] == 'L' ):
			user.write('L')
			whoid = module_finduser(user, "\r\n  \x1b[32mGet information on who?")
			if ( whoid > 0 ):
				whoName = user.userGetLogin(whoid)
				whoCost = user.level * 100
				user.write("\r\n  \x1b[32mThat will be \x1b[1m"+str(whoCost)+"\x1b[0;32m gold.  Ok? ")
				yesno = user.ntcon.recv(2)
				if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
					user.write('Y')
					if ( user.gold < whoCost ):
						user.write("\r\n  \x1b[32mYou don't have enough gold jackass!\x1b[0m\r\n")
					else:
						usertoSee = sorduser(whoName, user.dbcon, user.ntcon, user.art)
						user.gold -= whoCost
						user.write(module_viewstats(usertoSee))
						user.pause()
				else:
					user.write('N')
					user.write("\r\n  \x1b[32mOk.  You got it.\x1b[0m\r\n")
			else: 
				user.write("\r\n  \x1b[32mOk.  Nevermind.\x1b[0m\r\n")
		elif ( data[0] == 'c' or data[0] == 'C' ):
			user.write('C')
			user.write(func_casebold("\r\n  Pick that which best describes your childhood.\r\n  From an early age, you remember:\r\n\r\n", 2))
			user.write(func_normmenu("(D)abbling in the mystical forces"))
			user.write(func_normmenu("(K)illing a lot of woodland creatures"))
			user.write(func_normmenu("(L)ying, cheating, and stealing from the blind"))
			thisLooper = False
			while ( not thisLooper ):
				user.write(func_casebold("\r\n  Your Choice (D/K/L) :-: ", 2))
				data = user.ntcon.recv(2)
				if not data: break
				if ( data[0] == 'k' or data[0] == 'K' ):
					user.write('K')
					newclassnum = 1
					thisLooper = True
					user.write(func_casebold("\r\n  Welcome warrior to the ranks of the Death Knights!\r\n", 2))
				if ( data[0] == 'd' or data[0] == 'D' ):
					user.write('D')
					newclassnum = 2
					thisLooper = True
					user.write(func_casebold("\r\n  Feel the force young jedi.!\r\n", 2))
				if ( data[0] == 'l' or data[0] == 'L' ):
					user.write('L')
					newclassnum = 3
					thisLooper = True
					user.write(func_casebold("\r\n  You're a real shitheel, you know that?\r\n", 2))
			user.cls = newclassnum
		else:
			skipDisp = True
	

def dragon_fight(user):
	""" Forest Fight System """
	user.write(user.art.lair())
	thisUserDefense = user.defence
	thisUserHit     = user.str / 2
	ctrlDead = False
	ctrlRan  = False
	ctrlWin  = False
	thisEnemyHit    = 2000
	thisEnemyHP     = 15000
	thisEnemyName   = "The Red Dragon"
	thisEnemyWeapon = "Set Later."
	
	user.write("\r\n\r\n  \x1b[32m**\x1b[1;37mFIGHT\x1b[0m\x1b[32m**\r\n")
	user.write("\r\n  \x1b[32mYou have encountered "+thisEnemyName+"!!\x1b[0m\r\n")

	user.write("\r\n  \x1b[32mYour skill allows you to get the first strike.\x1b[0m\r\n")

	skipDisp = False
	while ( user.hp > 0 and thisEnemyHP > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
		if ( not skipDisp ):
			user.write(forest_menu(user, thisEnemyHP, thisEnemyName, True))
		hisType = random.randint(1, 7)
		if ( hisType == 1 or hisType == 2 ):
			thisEnemyWeapon = "Huge Fucking Claws"
			thisEnemyHit = 2100
		elif ( hisType == 3 or hisType == 4 ):
			thisEnemyWeapon = "Swishing Tail"
			thisEnemyHit = 1800
		elif ( hisType == 5 or hisType == 6 ):
			thisEnemyWeapon = "Stomping the Ground"
			thisEnemyHit = 1500
		else:
			thisEnemyWeapon = "Flaming Breath"
			thisEnemyHit = 3000
		skipDisp = False
		data = user.ntcon.recv(2)
		if not data: break
		elif ( data[0] == 's' or data[0] == 'S' ):
			user.write('S')
			user.write(module_viewstats(user))
		elif ( data[0] == 'a' or data[0] == 'A' ): # Attack!
			user.write("A\r\n")
			hisAttack = ( thisEnemyHit + random.randint(500, thisEnemyHit)) - thisUserDefense
			myAttack  = ( thisUserHit + random.randint(0, thisUserHit))
			if ( True ): # We Hit First
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
		elif ( data[0] == 'd' or data[0] == 'D' ): # Attack!
			user.write("D\r\n")
			if ( user.getSkillUse(1) > 0 ):
				user.updateSkillUse(1, -1)
				hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
				myAttack  = ( thisUserHit + (random.randint(2,5) * random.randint((thisUserHit / 2), thisUserHit))) + thisUserHit
				if ( True ): # We Hit First
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
					user.write("\r\n  \x1b[1;32mUltra Powerful Move!\x1b[0m\r\n  \x1b[32mYou hit "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
					thisEnemyHP = thisEnemyHP - myAttack
					if ( thisEnemyHP < 1 ): # We Win!
						ctrlWin = True
			else:
				user.write("\r\n  \x1b[32mYou have no Death Knight Skill Use Points!\x1b[0m\r\n\r\n")
		elif ( data[0] == 't' or data[0] == 'T' ): # Attack!
			user.write("T\r\n")
			if ( user.getSkillUse(3) > 0 ):
				user.updateSkillUse(3, -1)
				hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - ( thisUserDefense * 2 )
				myAttack  = ( thisUserHit + (random.randint(1,3) * random.randint((thisUserHit / 2), thisUserHit))) + thisUserHit
				if ( True ): # We Hit First
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
					user.write("\r\n  \x1b[1;32mUltra Sneaky Move!\x1b[0m\r\n  \x1b[32mYou hit "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
					thisEnemyHP = thisEnemyHP - myAttack
					if ( thisEnemyHP < 1 ): # We Win!
						ctrlWin = True
			else:
				user.write("\r\n  \x1b[32mYou have no Thief Skill Use Points!\x1b[0m\r\n\r\n")
		elif ( data[0] == 'r' or data[0] == 'R' ): # Run Away
			if ( random.randint(1, 10) == 4 ): # Hit in the back.
				hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
				if ( hisAttack >= user.hp ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.hp # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you in the back with it's "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\r\n")
					user.hp -= hisAttack
					ctrlRan = True
			else:
				user.write("\r\n  \x1b[32mYou narrowly escape harm.\x1b[0m\r\n")
				ctrlRan = True
		elif ( data[0] == 'q' or data[0] == 'Q' ):
			user.write("\r\n  \x1b[31mYou are in Combat!  Try Running!\x1b[0m\r\n")
		elif ( data[0] == 'h' or data[0] == 'H' ):
			user.write("\r\n  \x1b[32mYou are in combat, and they don't make house calls!\x1b[0m\r\n")
		elif ( data[0] == 'l' or data[0] == 'L' ):
			user.write("\r\n  \x1b[32mWhat?!  You want to fight two at once?\x1b[0m\r\n")
		elif ( data[0] == 'm' or data[0] == 'M' ): #Magic!
			if ( user.getSkillUse(2) < 1 ):
				user.write("\r\n  \x1b[32mYou have no Magical Use Points!\x1b[0m\r\n\r\n")
			else:
				user.write("\r\n" + func_normmenu("(N)evermind") + func_normmenu("(P)inch Real Hard (1)"))
				if ( user.getSkillUse(2) > 3 ):
					user.write(func_normmenu("(D)isappear (4)"))
					if ( user.getSkillUse(2) > 7 ):
						user.write(func_normmenu("(H)eat Wave (8)"))
						if ( user.getSkillUse(2) > 11 ):
							user.write(func_normmenu("(L)ight Shield (12)"))
							if ( user.getSkillUse(2) > 15 ):
								user.write(func_normmenu("(S)hatter (16)"))
								if ( user.getSkillUse(2) > 19 ):
									user.write(func_normmenu("(M)ind Heal (20)"))
				user.write("\r\n  \x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? [\x1b[1;35mA\x1b[0m\x1b[32m] : \x1b[0m")
				tinyQuit = False
				while ( not tinyQuit ):
					miniData = user.ntcon.recv(2)
					if not miniData: break
					elif ( miniData[0] == 'n' or miniData[0] == 'N' ): #Nothing
						user.write("N\r\n  \x1b[32mSure thing boss.\x1b[0m\r\n")
						tinyQuit = True
					elif ( miniData[0] == 'p' or miniData[0] == 'P' ): #Pinch!
						user.write("P")
						user.updateSkillUse(2, -1)
						tinyQuit = True
						hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
						myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + ( thisUserHit / 4 )
						if ( True ): # We Hit First
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
							user.write("\r\n  \x1b[32mYou pinch "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
							thisEnemyHP = thisEnemyHP - myAttack
							if ( thisEnemyHP < 1 ): # We Win!
								ctrlWin = True
					elif ( (miniData[0] == 'd' or miniData[0] == 'D') and ( user.getSkillUse(2) > 3 ) ): #Disappear
						user.write("D\r\n  \x1b[32mYou disapper like a ghost!\x1b[0m\r\n")
						user.updateSkillUse(2, -4)
						tinyQuit = True
						ctrlRan = True
					elif ( (miniData[0] == 'h' or miniData[0] == 'H') and ( user.getSkillUse(2) > 7 ) ): #Heat Wave
						user.write("H")
						user.updateSkillUse(2, -8)
						tinyQuit = True
						hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
						myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + (thisUserHit / 2)
						if ( True ): # We Hit First
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
							user.write("\r\n  \x1b[32mYou blast "+thisEnemyName+" with Heat Wave for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
							thisEnemyHP = thisEnemyHP - myAttack
							if ( thisEnemyHP < 1 ): # We Win!
								ctrlWin = True
					elif ( (miniData[0] == 'l' or miniData[0] == 'L') and ( user.getSkillUse(2) > 11 ) ): #Light Shield
						user.write("L\r\n  \x1b[32mYou feel a bit odd.  You dig in a feel better defended\x1b[0m\r\n")
						user.updateSkillUse(2, -12)
						thisUserDefense = thisUserDefense * 2
						tinyQuit = True
					elif ( (miniData[0] == 's' or miniData[0] == 'S') and ( user.getSkillUse(2) > 15 ) ): #Shatter
						user.write("S")
						user.updateSkillUse(2, -16)
						tinyQuit = True
						hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
						myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + (thisUserHit * 2)
						if ( not thisUnderdog ): # We Hit First
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
							user.write("\r\n  \x1b[32mYou Shatter "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
							thisEnemyHP = thisEnemyHP - myAttack
							if ( thisEnemyHP < 1 ): # We Win!
								ctrlWin = True
					elif ( (miniData[0] == 'm' or miniData[0] == 'M') and ( user.getSkillUse(2) > 19 ) ): #Mind Heal
						user.write("M\r\n  \x1b[32mYou feel much better!\x1b[0m\r\n")
						user.updateSkillUse(2, -20)
						hptoadd = user.hpmax - user.hp
						user.hp = user.hpmax
						if ( hptoadd < 5 ):
							user.write("\r\n  \x1b[32mEven though you are clearly a fuck-tard...\x1b[0m\r\n")
						tinyQuit = True
		else: #Catch non-options
			skipDisp = True

	if ( ctrlWin ) :
		user.gold = 500
		user.bank = 0
		user.str = 10
		user.defence = 1
		user.level = 1
		user.exp = 1
		user.dragon += 1
		user.ffight = user.thisSord.forestFights()
		user.pfight = user.thisSord.playerFights()
		user.hp = 20
		user.hpmax = 20
		user.gems = 10
		user.weapon = 1
		user.armor = 1
		
		lamentThis = "{32}{1}"+user.thisFullname+" {0}{32}Decimated {0}{31}{1}The Red Dragon!!! {0}{32}Rejoice!!!{0}"
		user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (lamentThis,))
		user.dbcon.commit()
		user.write(func_casebold("\r\n\r\n  You have defeated the Dragon, and saved the town.  Your stomach\r\n", 2))
		user.write(func_casebold("\x1b[32m  churns at the site of stacks of clean white bones - Bones of small\r\n", 2))
		user.write(func_casebold("\x1b[32m  children.\r\n\r\n", 2))
		user.write(func_casebold("  THANKS TO YOU, THE HORROR HAS ENDED!\r\n\r\n", 2))
		user.pause()
		for myline in endstory[user.cls]:
			user.write("\x1b[32m"+myline+"\x1b[0m\r\n")
		user.pause()
		user.write(func_casebold("                  ** YOUR QUEST IS NOT OVER **\r\n\r\n", 2))
		user.write(func_casebold("  You are a hero.  Bards will sing of your deeds, but that doesn't\r\n", 2))
		user.write(func_casebold("\x1b[32m  mean your life doesn't go on.\r\n", 2))
		user.write(func_casebold("  YOUR CHARACTER WILL NOW BE RESET.  But you will keep a few things\r\n", 2))
		user.write(func_casebold("\x1b[32m  you have earned.  Like the following.\r\n", 2))
		user.write(func_casebold("  ALL SPECIAL SKILLS.\r\n  CHARM.\r\n  A FEW OTHER THINGS.\r\n", 2))			
		user.pause()
		
	if ( ctrlDead ) :
		if ( user.fairy == True ):
			user.hp = 1
			user.fairy = 0
			user.write(func_casebold("  Miraculously, your fairy saves you from the edge of defeat.  You escape with your life.\r\n", 2))
		else:
			user.alive = 0
			#exception handles, do it later. user.logout()
			lamentThis = "{31}{1}The Red Dragon{0}{32} Decimated "+user.thisFullname+"{0}"
			user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (lamentThis,))
			user.dbcon.commit()
			user.write(func_casebold("\r\n\r\n  The Dragon pauses to look at you, then snorts in a Dragon laugh, and\r\n", 1))
			user.write(func_casebold("\x1b[31m  delicately rips your head off, with the finess only a Dragon well\r\n", 1))
			user.write(func_casebold("\x1b[31m  practiced in the art could do.\r\n", 1))
			raise Exception('normal', "User is DOA.  Bummer.")
