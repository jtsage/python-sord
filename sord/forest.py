#!/usr/bin/python
"""
 * Fighting Subsystem.
 * Contains forest fights, events, player fights, leveling up
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage
 * @todo Player fight subsystem, horses. """
import random, re, time
from functions import *
from data import *

def forest_special(user):
	""" Forest Special Events
	* @todo Add all elements as needed.
	* 	- fairies forest_fairies()
	* 	- dark horse tavern  darkhorse_login()  (new file) 
	* finish the flowers """
	happening = random.randint(1, 12)
	if ( happening == 1 ):   # Find Gems
		thisfind = random.randint(1, 4)
		user.write(user.art.line())
		user.write("  \x1b[32mFortune Smiles Upon You.  You find \x1b[1;37m"+str(thisfind)+"\x1b[0m\x1b[32m gems!\x1b[0m\r\n")
		user.write(user.art.line())
		user.pause()
		user.updateGems(thisfind)
	elif ( happening == 2 ): # Find Gold
		thisfind = random.randint(1, 4) * 200 * user.getLevel()
		user.write(user.art.line())
		user.write("  \x1b[32mFortune Smiles Upon You.  You find a sack full of \x1b[1;37m"+str(thisfind)+"\x1b[0m\x1b[32m gold!\x1b[0m\r\n")
		user.write(user.art.line())
		user.pause()
		user.updateGold(thisfind)
	elif ( happening == 3 ): # Hammerstone (attack str++)
		user.write(user.art.line())
		user.write("  \x1b[32mYou find a hammer stone.  You quickly hit it as hard as possible.\r\n \x1b[1mYour attack strength is raised by 1!\x1b[0m\r\n")
		user.write(user.art.line())
		user.pause()
		user.updateStrength(1)
	elif ( happening == 4 ): # Merry Men (hp = hpmax)
		user.write(user.art.line())
		user.write("  \x1b[32mYou stumble across a group of merry men.  They offer you ale you can't resist.\r\n \x1b[1mYou feel refreshed!\x1b[0m\r\n")
		user.write(user.art.line())
		user.pause()
		hptoadd = user.getHPMax - user.getHP
		if ( hptoadd > 0 ):
			user.updateHP(hptoadd)
	elif ( happening == 5 ): # Old Man (gold + (lvl * 500) && charm +1 on help) (costs 1 fight)
		user.write(user.art.line())
		user.write("  \x1b[32mYou come upon an old man wandering around.\r\n  He asks you for help back to town.\x1b[0m\r\n")
		user.wrtie(func_normmenu("(H)elp the old man"))
		user.write(func_normmenu("(I)gnore him"))
		user.write("  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
		miniQuit = False
		while ( not miniQuit ):
			data = user.connection.recv(2)
			if ( data[0] == 'h' or data[0] == 'H' ):
				user.write('H')
				goldtoadd = user.getGold() * 500
				user.write("\r\n  \x1b[32mYou help the old gentleman home.\x1b[1mHe gives you "+str(goldtoadd)+" gold and 1 charm!.\x1b[0m\r\n")
				user.updateGold(goldtoadd)
				user.updateCharm(1)
				user.updateForestFight(-1)
				miniQuit = True
			elif ( data[0] == 'i' or data[0] == 'I' ):
				user.write('I')
				user.write("\r\n  \x1b[31mYou just really \x1b[1mSUCK\x1b[0;31m, don't you?\x1b[0m\r\n")
				miniQuit = True
			else:
				pass
		user.pause()
	elif ( happening == 6 ): # Ugly (33%) and Pretty (66%) stick
		user.write(user.art.line())
		user.write("  \x1b[32mA demented penguin jumps from the bushes and whacks you with a")
		sticktype = random.randint(1, 3)
		if ( sticktype == 2 ):
			user.write("\x1b[1,31mugly\x1b[0,32m")
		else:
			user.write("\x1b[1mpretty\x1b[0,32m")
		user.write("stick!  Your charm is ")
		if ( sticktype == 2 ):
			user.write("lowered")
			if ( user.getCharm() > 0 ):
				user.updateCharm(-1)
		else:
			user.write("raised")
			user.updateCharm(1)
		user.write("by 1!!\x1b[0m\r\n")
		user.pause()
	elif ( happening == 7 ): # Old Hag
		user.write(user.art.line())
		user.write("  \x1b[32mYou come across an old hag.\r\n\r\n  \x1b[1m\"Give me a gem my pretty, and I will completely heal you!\"\x1b[0,32m\r\n  She screeches!\x1b[0m\r\n\r\n")
		user.write(func_normmenu("(G)ive her a gem"))
		user.write(func_normmenu("(K)ick her and run"))
		user.write(func_normmenu("(L)eave polietly"))
		user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
		miniQuit = False
		while ( not miniQuit ):
			data = user.connection.recv(2)
			if ( data[0] == 'l' or data[0] == 'L' ):
				user.write("L\r\n\r\n  \x1b[32mThe old hag begins following you like a lost puppy.\x1b[0m\r\n")
			elif ( data[0] == 'k' or data[0] == 'K' ):
				user.write("K\r\n\r\n  \x1b[32mYou hate to be rude to your elders, but sometimes deperate times call for\r\n  deperate measures.  You which the old hag in the shin and run for it.\x1b[0m\r\n")
				miniQuit = True
			elif ( data[0] == 'g' or data[0] == 'G' ):
				user.write('G')
				if ( user.getGems() > 0 ):
					user.write("\r\n\r\n  \x1b[1;32m\"Thank you\"\x1b[0;32m she cackles.\r\n  \x1b[1mYou feel refreshed and renewed\x1b[0m\r\n")
					user.updateHPMax(1)
					hptoadd = user.getHPMax() - user.getHP()
					user.updateHP(hptoadd)
					user.updateGems(-1)
					miniQuit = True
				else:
					user.write("\r\n\r\n  \x1b[1,32m\"You don't have any gems you stinky cow-pox pustule!\"\[33[0,32m she yells.\r\n  \x1b[1mCome to think of it, you feel rather like a cow-pie.\x1b[0m\r\n")
					hptoremove = user.getHP() - 1
					user.updateHP(hptoremove * -1)
					miniQuit = True
			else: 
				pass
		user.pause()
	elif ( happening == 8 ): # Flowers in the forest.
		user.write(user.art.line())
		user.write("  \x1b[32mYou come across a grove of flowers, and decide to inspect them closer...\r\n  \x1b[1mThere is something written here!\x1b[0m\r\n")
		user.pause()
		# do this! module_flowers(user)
	elif ( happening == 9 ): # rescue man/maiden
		user.write(user.art.line())
		user.write("  \x1b[32mYou come upon a dead bird.  While gross, you begin to put it out of your\r\n  mind when you notice a scroll attached to it's leg\r\n\r\n")
		user.write("  \x1b[1mTo Whome It May Concern:\r\n    I have been locked in this terrible tower for many cycles.\r\n    Please save me soon!\n        ~ Elora\r\n\r\n")
		user.write(func_normmenu("(S)eek the maiden"))
		user.write(func_normmenu("(I)gnore her plight"))
		user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
		miniQuit = False
		while ( not miniQuit ):
			data = user.connection.recv(2)
			if ( data[0] == 'i' or data[0] == 'I' ):
				user.write('I')
				miniQuit = True
			elif ( data[0] == 's' or data[0] == 'S' ):
				user.write('S')
				user.updateForestFight(-1)
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
					miniData = user.connection.recv(2)
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
					user.updateGems(5)
					user.updateGold(user.getLevel() * 500)
				else: # WRONG
					if ( random.randint(1, 2) == 1 ): # REALLY, REALLY WRONG
						user.write("\r\n  \x1b[32mYou have choosen \x1b[1mpoorly.  really poorly.\x1b[0m\r\n\r\n")
						user.write("  \x1b[32mYou hear a strange groan and out pops Ken the Magnificent,\r\n the disfigured midget (er, 'little person').\r\n  Sadly, 'little person' doesn't refer to all of him.\r\n  \x1b[1mYou feel terrible, both physically and mentally\x1b[0m\r\n")
						thistakeHP = user.getHP() - 1
						user.updateHP(thistakeHP * -1)
					else: # NOT SO BAD
						user.write("\r\n  \x1b[32mYou have choosen \x1b[1mpoorly.\x1b[0m\r\n")
						user.write("  \x1b[32mYou run like hell before anything bad happens.\x1b[0m\r\n")
				miniQuit = True
		user.pause()
	elif ( happening == 10 ): # lessons
		if ( user.getClass() == 1 ):
			forest_lesson_d(user)
		elif ( user.getClass() == 2 ):
			forest_lesson_m(user)
		else:
			forest_lesson_t(user)
	elif ( happening == 11 ): # horse tavern
		if ( not user.didHorse() ) :
			pass #darkhorse_logic()
			user.pause()
	elif ( happening == 12 ): # fairies
		pass #forest_fairies(user)
		user.pause()
	else:
		pass
		

def forest_fight(user):
	""" Forest Fight System """
	user.updateForestFight(-1)
	thisUserLevel = user.getLevel()
	thisTopEnemy  = len(enemies[thisUserLevel]) - 1
	thisEnemy     = random.randint(0, thisTopEnemy)
	if ( random.randint(1, 10) == 8 ):
		thisUnderdog = True
	else:
		thisUnderdog = False
	thisUserDefense = user.getDefense()
	thisUserHit     = user.getStrength() / 2
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
		hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
		if ( hisAttack > 0 ):
			if ( hisAttack > user.getHP() ):
				ctrlDead = True
				hisAttack = user.getHP()
			user.write("\r\n  \x1b[32m"+thisEnemyName+" executes a sneak attach for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage!\x1b[0m\r\n")
			user.updateHP(hisAttack * -1)
		else:
		 user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely!\x1b[0m\r\n")
	else:
		user.write("\r\n  \x1b[32mYour skill allows you to get the first strike.\x1b[0m\r\n")

	while ( user.getHP() > 0 and thisEnemyHP > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
		user.write(forest_menu(user, thisEnemyHP, thisEnemyName))
		data = user.connection.recv(2)
		if ( data[0] == 's' or data[0] == 'S' ):
			user.write('S')
			user.write(forest_viewstats(user))
		elif ( data[0] == 'a' or data[0] == 'A' ): # Attack!
			user.write("A\r\n")
			hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
			myAttack  = ( thisUserHit + random.randint(0, thisUserHit))
			if ( not thisUnderdog ): # We Hit First
				if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
					hisAttack = 0
			if ( hisAttack >= user.getHP() ): # We are dead.  Bummer.
				ctrlDead = True
				hisAttack = user.getHP() # No insult to injury
			if ( hisAttack > 0 ): # He hit us
				user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
				user.updateHP(hisAttack * -1)
			else: 
				user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely\x1b[0m\r\n")
			if ( myAttack > 0 and not ctrlDead ): # We hit him!
				user.write("\r\n  \x1b[32mYou hit "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
				thisEnemyHP = thisEnemyHP - myAttack
				if ( thisEnemyHP < 1 ): # We Win!
					ctrlWin = True
					user.write("\r\n  \x1b[31m"+enemies[thisUserLevel][thisEnemy][6]+"\x1b[0m\r\n")
		elif ( data[0] == 'r' or data[0] == 'R' ): # Run Away
			if ( random.randint(1, 10) == 4 ): # Hit in the back.
				hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
				if ( hisAttack >= user.getHP() ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.getHP() # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you in the back with it's "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\r\n")
					user.updateHP(hisAttack)
			else:
				user.write("\r\n  \x1b[32mYou narrowly escape harm.\x1b[0m\r\n")
				ctrlRan = True
		elif ( data[0] == 'q' or data[0] == 'Q' ):
			user.write("\r\n  \x1b[31mYou are in Combat!  Try Running!\x1b[0m\r\n")
		elif ( data[0] == 'h' or data[0] == 'H' ):
			user.write("\r\n  \x1b[32mYou are in combat, and they don't make house calls!\x1b[0m\r\n")
		elif ( data[0] == 'l' or data[0] == 'L' ):
			user.write("\r\n  \x1b[32mWhat?!  You want to fight two at once?\x1b[0m\r\n")

	if ( ctrlWin ) :
		user.updateExperience(enemies[thisUserLevel][thisEnemy][5])
		user.updateGold(enemies[thisUserLevel][thisEnemy][4])
		user.write("\r\n  \x1b[32mYou have recieved \x1b[1m"+str(enemies[thisUserLevel][thisEnemy][4])+"\x1b[22m gold and \x1b[1m"+str(enemies[thisUserLevel][thisEnemy][5])+"\x1b[22m experience\x1b[0m\r\n")
		user.pause()
	if ( ctrlDead ) :
		user.setDead()
		user.logout()
		lamentTop = len(forestdie) - 1
		lamentThis = forestdie[random.randint(0, lamentTop)]
		lamentThis = re.sub("`n", "\r\n", lamentThis)
		lamentThis = re.sub("`g", user.thisFullname, lamentThis)
		lamentThis = re.sub("`e", thisEnemyName, lamentThis)
		lamentThis = user.dbc.escape_string(lamentThis)
		thisSQL = "INSERT INTO "+user.thisSord.sqlPrefix()+"daily ( `data` ) VALUES ('"+lamentThis+"')"
		user.db.execute(thisSQL)
		user.write(func_casebold("  Tragically, you died.  Returning to the mundane world for the day...\n", 1))
		user.connection.close()

def forest_menu(user, enemyHP, enemyName) : 
	""" Forest Fight Menu
	@ todo Special Skills Section """
	thismenu  = "\r\n  \x1b[32mYour Hitpoints : \x1b[1m"+str(user.getHP())+"\x1b[0m\r\n"
	thismenu += "  \x1b[32m"+enemyName+"'s Hitpoints : \x1b[1m"+str(enemyHP)+"\x1b[0m\r\n\r\n"
	thismenu += func_normmenu("(A)ttack")
	thismenu += func_normmenu("(S)tats")
	thismenu += func_normmenu("(R)un")
	thismenu += "\r\n  \x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? [\x1b[1;35mA\x1b[0m\x1b[32m] : \x1b[0m"
	return thismenu

def forest_viewstats(user):
	""" View Player Stats
	* @param int $userid User ID
	* @return string Formatted output for display"""
	output  = "\r\n\r\n\x1b[1m\x1b[37m"+user.thisFullname+"\x1b[0m\x1b[32m's Stats...\r\n"
	output += user.art.line()
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
"""
function master_fight() {
    "" Master Fight System ""
	GLOBAL $userid, $masters, $masterwin, $db, $MYSQL_PREFIX;
	$userlevel = user_getlevel($userid);
	$thisunderdog = 0;
	$userstr = user_getstr($userid);
	$userdef = user_getdef($userid);
	$userhstr = ($userstr - ($userstr % 2)) / 2;
	$userhp = user_gethp($userid);
	$dead = 0; $ran = 0; $win = 0;

	$enemystr = $masters[$userlevel][7];
	$enemydef = $masters[$userlevel][8];
	$enemyhstr = ($enemystr - ($enemystr % 2)) / 2;
	$enemyhp = $masters[$userlevel][6];
	$enemyname = $masters[$userlevel][0];
	$enemywep = $masters[$userlevel][1];
	
	slowecho("\n\n  \x1b[32m**\x1b[1;37mFIGHT\x1b[0m\x1b[32m**\n");
	slowecho("\n  \x1b[32mYour skill allows you to get the first strike.\x1b[0m\n"); 
	
	while( $userhp > 0 && $enemyhp > 0 && !$dead && !$ran) {  ## FIGHT LOOP ##
		$userhp = user_gethp($userid);
		slowecho(forest_menu($userhp, $enemyhp, $enemyname));
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'S':
				module_viewstats($userid);
				break;
			case 'A':
				$eattack =  (( $enemyhstr ) + rand(0, $enemyhstr) ) - $userdef;
				$uattack =  (( $userhstr ) + rand(0, $userhstr)) - $enemydef;
				if ( !$thisunderdog ) { if ( $uattack > $enemyhp ) { $eattack = 0; } }
				if ( $eattack > $userhp ) { $eattack = $userhp; $dead = 1;}
				if ( $eattack > 0 ) {
					slowecho("\n  \x1b[32m{$enemyname} hits you with {$enemywep} for \x1b[1;31m{$eattack}\x1b[0m\x1b[32m damage\x1b[0m\n"); 
					user_takehp($userid, $eattack);
				}
				if ( $uattack > 0 && !$dead) { 
					slowecho("\n  \x1b[32mYou hit {$enemyname} for \x1b[1;31m{$uattack}\x1b[0m\x1b[32m damage\n"); 
					$enemyhp = $enemyhp - $uattack;
					if ( $enemyhp < 1 ) { 
						slowecho("  \x1b[31m{$masters[$userlevel][5]}\n"); 
						$win = 1; }
				}
				break;
			case 'R':
				slowecho("\n  \x1b[32mYou retire from the field before getting yourself killed.\x1b[0m\n"); 
				$resethp = "UPDATE {$MYSQL_PREFIX}stats set hp = hpmax WHERE userid = {$userid}";
				$masterql = "UPDATE {$MYSQL_PREFIX}stats SET master = 1 WHERE userid = {$userid}"; 
				$result = mysql_query($resethp, $db);
				$result = mysql_query($masterql, $db);
				$ran = 1; 
				break;
		}
	}
	if ( $win ) {
		$addexp = $masters[$userlevel][2] * .1;
		user_giveexp($userid, $addexp);
		user_givedef($userid, $masterwin[$userlevel][2]);
		user_givestr($userid, $masterwin[$userlevel][1]);
		user_givehpmax($userid, $masterwin[$userlevel][0]);
		slowecho("\n  \x1b[32mYou have receieved \x1b[1m+{$masterwin[$userlevel][2]}\x1b[22m vitality, \x1b[1m+{$masterwin[$userlevel][1]}\x1b[22m strength, and \x1b[1m+{$masterwin[$userlevel][0]}\x1b[22m hitpoints.\x1b[0m\n");
		$newlevel = user_getlevel($userid) + 1;
		slowecho("  \x1b[32mYou have gained \x1b[1m{$addexp}\x1b[22m experience, and are now level \x1b[1m{$newlevel}\x1b[22m.\x1b[0m\n");
		user_setlevel($userid, $newlevel);
		$resethp = "UPDATE {$MYSQL_PREFIX}stats set hp = hpmax WHERE userid = {$userid}";
		$result = mysql_query($resethp, $db);
		pauser();
	}
	if ( $dead ) {
		slowecho("\n  \x1b[31mTragically, you are horribly disfigured....  oh wait...\x1b[0m\n");
		slowecho("  \x1b[31mYou always looked like that you say?...  That's unfortunate...\x1b[0m\n");
		slowecho("  \x1b[32mAnyway, you lost.  Being the gracious master {$enemyname} is, he heals you and sends you away for the day.\x1b[0m\n");
		$resethp = "UPDATE {$MYSQL_PREFIX}stats set hp = hpmax WHERE userid = {$userid}";
		$masterql = "UPDATE {$MYSQL_PREFIX}stats SET master = 1 WHERE userid = {$userid}"; 
		$result = mysql_query($resethp, $db);
		$result = mysql_query($masterql, $db);
		pauser();
	}
}"""

def forest_lesson_d(user) :
	""" Learn to be a death kniofht"""
	user.write(user.art.line())
	user.write("\r\n  \x1b[32mYou come upon a group of warriors, they carry the look of a proud people.\x1b[0m\r\n")
	user.write("\r\n   \x1b[1,32mDeath Knight #1: \x1b[0,32mWe shall teach you the ways of the death knights weakling.\x1b[0m\r\n")
	user.write("   \x1b[1,32mDeath Knight #2: \x1b[0,32mAye.  But you must prove your wisdom first.  This man is guilty of a crime.\x1b[0m\r\n")
	user.write("   \x1b[1,32mDeath Knight #1: \x1b[0,32mYup.  Or he's completely innocent.  Decide wisely.!\x1b[0m\r\n")
	user.write(func_normmenu("(K)ill Him"))
	user.write(func_normmenu("(F)ree him as an innocent"))
	user.write("\r\n  \x1b[0m\x1b[32mYour choice, \x1b[1m"+user.thisFullname+"\x1b[22m? (K,F) \x1b[0m\x1b[32m:-: \x1b[0m")
	miniQuit = False
	while ( miniQuit ):
		data = user.connection.recv(2)
		if ( data[0] == 'k' or data[0] == 'K' ):
			user.write('K')
			user.write("\r\n  \x1b[32mYou draw your weapon, and ram it as hard as you can through his midsection.\x1b[0m\r\n")
			thisChoice = 1
			miniQuit = True
		elif ( data[0] == 'f' or data[0] == 'F' ):
			user.write('F')
			user.write("\r\n  \x1b[32mYou consider a moment, and shout \"Let him live!  He's done nothing wrong!\"\x1b[0m\r\n")
			thisChoice = 2
			miniQuit = True
		else:
			pass
	
	user.write("\r\n  \x1b[1;37m...")
	time.sleep(1)
	user.write("\x1b[31mAND\x1b[37m")
	time.sleep(1)
	user.write("...\x1b[0m")
	
	if ( thisChoice == random.randint(1,2) ):
		user.write("\r\n   \x1b[1,32mDeath Knight #1: \x1b[0,32mWell spotted young warrior.  We shall teach you!\x1b[0m\r\n")
		user.write("  \x1b[32mYou recieve \x1b[1m1\x1b[0,32m use point")
		user.updateSkillUse(1, 1)
		addtohp = user.getHPMax() - user.getHP()
		if ( addtohp > 0 ):
			user.updateHP(addtohp)
		if ( user.getSkillPoint(1) < 40 ):
			user.updateSkillPoint(1, 1)
			user.write(" and \x1b[1m1\x1b[0,32m skill point")
		user.write(".\x1b[0m\r\n")
	else:
		user.write("\r\n   \x1b[1,32mDeath Knight #3: \x1b[0,32mOh god no!  That wasn't right at all!  Somebody get a mop and a bandaid!\x1b[0m\r\n")

def forest_lesson_t(user) :
	""" LEarn to be a thief """
	user.write(user.art.line())
	user.write("\r\n  \x1b[32mYou come upon a gathering of the theives guild, they kinda smell bad.\x1b[0m\r\n")
	user.write("\r\n   \x1b[1,32mThief #1: \x1b[0,32mWe can make you a better thief.  Just cost ya a gem.\x1b[0m\r\n")
	user.write(func_normmenu("(G)ive him the gem"))
	user.write(func_normmenu("(S)pit on him and walk away"))
	user.write(func_normmenu("(M)utter incoherantly, hoping he'll leave"))
	user.write("\r\n  \x1b[0m\x1b[32mYour choice, \x1b[1m"+user.thisFullname+"\x1b[22m? (G,S,M) \x1b[0m\x1b[32m:-: \x1b[0m")
	miniQuit = False
	while ( not miniQuit ):
		data = user.connection.recv(2)
		if ( data[0] == 's' or data[0] == 'S' ):
			user.write("S\r\n  \x1b[32mAs you spit on him, the thief looks at you closely.  He almost looks proud.\x1b[0m\r\n")
			miniQuit = True
		elif ( data[0] == 'm' or data[0] == 'M' ):
			user.write("M\r\n  \x1b[32mAs the thief leaves, you distincly hear the words \"nutjob\" and \"jackass\".  Oh well.\x1b[0m\r\n")
			miniQuit = True
		elif ( data[0] == 'g' or data[0] == 'G' ):
			user.write('G')
			if ( user.getGems() > 0 ):
				user.updateSkillUse(3, 1)
				user.write("\r\n  \x1b[32mYou recieve \x1b[1m1\x1b[0,32m use point")
				if ( user.getSkillPoint(3) < 40 ):
					user.updateSkillPoint(3, 1)
					user.write(" and \x1b[1m1\x1b[0,32m skill point")
				user.write(".\x1b[0m\n")
				user.updateGems(-1)
			else:
				user.write("\r\n  \x1b[1,32mThief #1: \x1b[0,32mYou don't have any gems dumbass.\x1b[0m\r\n")
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
		data = user.connection.recv(2)
		if ( data[0] == 'k' or data[0] == 'K' or data[0] == 'b' or data[0] == 'B' ):
			user.write(data[0])
			user.write("\r\n  \x1b[32mYou knock polietly on the door.\x1b[0m\n")
			miniQuit1 = True
		if ( data[0] == 'l' or data[0] == 'L' ):
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
					thisGuess = int(func_getLine(user.connection, True))
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
				user.write("  \x1b[32mYou recieve \x1b[1m1\x1b[0,32m use point")
				if ( user.getSkillPoint(2) < 40 ):
					user.updateSkillPoint(2, 1)
					user.write(" and \x1b[1m1\x1b[0,32m skill point")
				user.write(".\x1b[0m\r\n")
			else:
				user.write("\r\n  \x1b[32mBetter luck next time!\x1b[0m\r\n")
